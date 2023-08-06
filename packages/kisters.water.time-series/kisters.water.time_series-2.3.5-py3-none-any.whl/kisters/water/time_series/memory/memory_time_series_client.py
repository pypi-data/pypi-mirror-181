from __future__ import annotations

import re
import uuid
from datetime import datetime
from sys import getsizeof
from typing import Any, AsyncIterator

import pandas as pd

from kisters.water.time_series.core import (
    TimeSeries,
    TimeSeriesClient,
    TimeSeriesComment,
    TimeSeriesEnsembleMemberNotFoundError,
    TimeSeriesMetadata,
    TimeSeriesNotFoundError,
    TimeSeriesUserError,
)
from kisters.water.time_series.core.schema import CommentSupport, EnsembleMember


class MemoryTimeSeriesClient(TimeSeriesClient[TimeSeries, TimeSeriesMetadata]):
    comment_support = CommentSupport.READ | CommentSupport.WRITE | CommentSupport.DELETE

    def __init__(self) -> None:
        self._ts_metadata: dict[str, TimeSeriesMetadata] = {}
        self._ts_data: dict[str, dict[EnsembleMember, pd.DataFrame]] = {}
        self._ts_comments: dict[str, dict[EnsembleMember, dict[str, TimeSeriesComment]]] = {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """"""

    async def create_time_series(
        self, *, path: str, metadata: dict | TimeSeriesMetadata = None, **kwargs
    ) -> TimeSeries:
        metadata = self.sanitize_metadata(path=path, metadata=metadata)
        self._ts_metadata[path] = metadata
        self._ts_data[path] = {}
        self._ts_comments[path] = {}
        return TimeSeries(self, metadata=metadata)

    async def read_time_series(
        self, *, path: str, metadata_keys: list[str] | None = None, **kwargs
    ) -> TimeSeries:
        try:
            return TimeSeries(self, metadata=self._ts_metadata[path])
        except KeyError as e:
            raise TimeSeriesNotFoundError(path) from e

    async def filter_time_series(
        self, *, ts_filter: str | None, metadata_keys: list[str] | None = None, **kwargs
    ) -> AsyncIterator[TimeSeries]:
        if ts_filter is None:
            for metadata in self._ts_metadata.values():
                yield TimeSeries(self, metadata=metadata)
        else:
            exp = re.compile(
                "^"
                + ts_filter.replace(".", "\\.").replace("/", "\\/").replace("?", "\\?").replace("*", ".*")
                + "$"
            )
            for path, metadata in self._ts_metadata.copy().items():
                if exp.match(path):
                    yield TimeSeries(self, metadata=metadata)

    async def update_time_series(self, *, path: str, metadata: dict | TimeSeriesMetadata, **kwargs) -> None:
        await self.create_time_series(path=path, metadata=metadata)

    async def delete_time_series(self, *, path: str, **kwargs) -> None:
        try:
            del self._ts_metadata[path]
            del self._ts_data[path]
            del self._ts_comments[path]
        except KeyError as e:
            raise TimeSeriesNotFoundError(path) from e

    def _get_data_frame(self, path: str, ensemble_member: EnsembleMember) -> pd.DataFrame:
        try:
            ts_data = self._ts_data[path]
        except KeyError as e:
            raise TimeSeriesNotFoundError(path) from e
        return ts_data[ensemble_member]

    async def read_coverage(
        self,
        *,
        path: str,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs,
    ) -> tuple[datetime, datetime]:
        ensemble_member = EnsembleMember(t0=t0, dispatch_info=dispatch_info, member=member)
        try:
            ensemble_df = self._get_data_frame(path, ensemble_member)
        except KeyError as e:
            if ensemble_member:
                raise TimeSeriesNotFoundError(path) from e
            else:
                raise TimeSeriesEnsembleMemberNotFoundError(
                    path, t0=t0, dispatch_info=dispatch_info, member=member
                ) from e
        return (
            ensemble_df.index[0].to_pydatetime(),
            ensemble_df.index[-1].to_pydatetime(),
        )

    async def read_ensemble_members(
        self,
        *,
        path: str,
        t0_start: datetime | None = None,
        t0_end: datetime | None = None,
        **kwargs,
    ) -> AsyncIterator[EnsembleMember]:
        try:
            ts_data = self._ts_data[path]
        except KeyError as err:
            raise TimeSeriesNotFoundError(path) from err
        for ensemble in ts_data:
            if (t0_start is None or t0_start <= ensemble.t0) and (t0_end is None or ensemble.t0 <= t0_end):
                yield ensemble

    async def read_data_frame(
        self,
        *,
        path: str,
        start: datetime | None = None,
        end: datetime | None = None,
        columns: list[str] | None = None,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs,
    ):
        try:
            ensemble_df = self._get_data_frame(
                path, EnsembleMember(t0=t0, dispatch_info=dispatch_info, member=member)
            )
        except KeyError:
            return pd.DataFrame()

        columns_loc = columns if columns else slice(None)
        if start is not None and end is not None:
            return ensemble_df.loc[
                (ensemble_df.index >= start) & (ensemble_df.index <= end), columns_loc
            ].copy()
        elif start is not None:
            return ensemble_df.loc[ensemble_df.index >= start, columns_loc].copy()
        elif end is not None:
            return ensemble_df.loc[ensemble_df.index <= end, columns_loc].copy()
        else:
            return ensemble_df.loc[:, columns_loc].copy()

    async def write_data_frame(
        self,
        *,
        path: str,
        data_frame: pd.DataFrame,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs,
    ):
        if data_frame.shape[0] == 0:
            return
        self._ts_data.setdefault(path, {})
        ensemble_member = EnsembleMember(t0=t0, dispatch_info=dispatch_info, member=member)
        try:
            ensemble_df = self._get_data_frame(path, ensemble_member)
        except KeyError:
            ensemble_df = None

        if data_frame.index.tz is None:
            raise TimeSeriesUserError("The data_frame time index doesn't have timezone", path)

        if ensemble_df is None:
            ensemble_df = data_frame
        else:
            is_in = data_frame.index.isin(ensemble_df.index)
            ensemble_df.loc[ensemble_df.index.isin(data_frame.index), data_frame.columns] = data_frame.loc[
                is_in
            ]
            ensemble_df = pd.concat([ensemble_df, data_frame.loc[~is_in]])
            ensemble_df = ensemble_df.reindex(ensemble_df.index.sort_values())
        self._ts_data[path][ensemble_member] = ensemble_df

    async def delete_data_range(
        self,
        *,
        path: str,
        start: datetime | None = None,
        end: datetime | None = None,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs,
    ):
        self._ts_data.setdefault(path, {})
        ensemble_member = EnsembleMember(t0=t0, dispatch_info=dispatch_info, member=member)
        try:
            ts_data = self._ts_data[path]
        except KeyError as e:
            raise TimeSeriesNotFoundError(path) from e

        if start is None and end is None:
            del ts_data[ensemble_member]
        else:
            try:
                ensemble_df = ts_data[ensemble_member]
                if start is not None and end is not None:
                    ts_data[ensemble_member] = ensemble_df.loc[
                        (ensemble_df.index < start) | (end < ensemble_df.index)
                    ]
                elif start is not None:
                    ts_data[ensemble_member] = ensemble_df.loc[ensemble_df.index < start]
                elif end is not None:
                    ts_data[ensemble_member] = ensemble_df.loc[end < ensemble_df.index]
            except KeyError:
                pass

    def _get_comments(self, path: str, ensemble_member: EnsembleMember):
        try:
            ts_comments = self._ts_comments[path]
        except KeyError as e:
            raise TimeSeriesNotFoundError(path) from e
        try:
            return ts_comments[ensemble_member]
        except KeyError:
            return {}

    async def read_comments(
        self,
        *,
        path: str,
        start: datetime | None = None,
        end: datetime | None = None,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs,
    ) -> AsyncIterator[TimeSeriesComment]:
        ensemble_member = EnsembleMember(t0=t0, dispatch_info=dispatch_info, member=member)
        ts_comments = self._get_comments(path, ensemble_member)

        for comment in ts_comments.values():
            if (start is None or start <= comment.end) and (end is None or end >= comment.start):
                yield comment

    async def write_comments(
        self,
        *,
        path: str,
        comments: list[TimeSeriesComment],
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs,
    ) -> None:
        ensemble_member = EnsembleMember(t0=t0, dispatch_info=dispatch_info, member=member)
        ts_comments = self._get_comments(path, ensemble_member)

        for new_comment in comments:
            written = False
            if new_comment.id is not None:
                if new_comment.id in ts_comments:
                    ts_comments[new_comment.id] = new_comment.copy()
                    written = True
            else:
                new_comment.id = str(uuid.uuid4())
            if not written:
                comment_ids_to_remove = []
                for comment in ts_comments.values():
                    if (
                        comment.comment == new_comment.comment
                        and new_comment.start <= comment.end
                        and new_comment.end >= comment.start
                    ):
                        new_comment.start = min(new_comment.start, comment.start)
                        new_comment.end = max(new_comment.end, comment.end)
                        if new_comment.start == comment.start and new_comment.end == comment.end:
                            continue
                        else:
                            comment_ids_to_remove.append(comment.id)
                for id in comment_ids_to_remove:
                    del ts_comments[id]
                ts_comments[new_comment.id] = new_comment.copy()
        self._ts_comments[path][ensemble_member] = ts_comments

    async def delete_comments(
        self,
        path: str,
        comments: list[TimeSeriesComment],
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs,
    ) -> None:
        ensemble_member = EnsembleMember(t0=t0, dispatch_info=dispatch_info, member=member)
        ts_comments = self._get_comments(path, ensemble_member)
        if ts_comments and comments:
            comment_ids = [c.id for c in comments if c.id]
            if comment_ids:
                for id in comment_ids:
                    del ts_comments[id]
            comments_without_id = [c for c in comments if not c.id]
            for remove_c in comments_without_id:
                if remove_c.comment:
                    exp = re.compile(
                        "^"
                        + remove_c.comment.replace(".", "\\.")
                        .replace("/", "\\/")
                        .replace("?", "\\?")
                        .replace("*", ".*")
                        + "$"
                    )
                    comment_ids_to_remove = []
                    new_comments = []
                    start, end = remove_c.start, remove_c.end
                    for comment in ts_comments.values():
                        if exp.match(comment.comment):
                            if (start_is_none := start is None or start < comment.end) and (
                                end_is_none := end is None or end > comment.start
                            ):
                                if (
                                    not start_is_none
                                    and start > comment.start
                                    and not end_is_none
                                    and end < comment.end
                                ):
                                    comment_ids_to_remove.append(comment.id)
                                    new_comments.extend(
                                        [
                                            TimeSeriesComment(
                                                id=str(uuid.uuid4()),
                                                start=comment.start,
                                                end=start,
                                            ),
                                            TimeSeriesComment(
                                                id=str(uuid.uuid4()),
                                                start=end,
                                                end=comment.end,
                                            ),
                                        ]
                                    )
                                elif (end_is_in_between := start_is_none or start <= comment.start) and (
                                    end_is_none or end <= comment.end
                                ):
                                    comment_ids_to_remove.append(comment.id)
                                elif end_is_in_between:
                                    comment.start = end
                                elif end_is_none or end <= comment.end:
                                    comment.end = start

                            if (start is None or start < comment.start) and (
                                end is None or end > comment.end
                            ):
                                comment_ids_to_remove.append(comment.id)
                            elif start is not None and start < comment.end:
                                comment.start = start

    async def info(self) -> dict[str, Any]:
        """This is just a close approximation to the memory consumed by the store"""
        overhead_dict_size = getsizeof(self._ts_data)
        df_size = 0
        for ensemble_dict in self._ts_data.values():
            overhead_dict_size += getsizeof(ensemble_dict)
            for df in ensemble_dict.values():
                df_size += df.values.size * df.values.itemsize
        metadata_size = sum(getsizeof(k) + getsizeof(v.dict()) for k, v in self._ts_metadata.items())
        overhead_dict_size += getsizeof(self._ts_comments)
        comment_size = 0
        for ensemble_dict in self._ts_comments.values():
            overhead_dict_size += getsizeof(ensemble_dict)
            for comments in ensemble_dict.values():
                overhead_dict_size += getsizeof(comments)
                for c in comments.values():
                    comment_size += getsizeof(c.dict())
        return {"memory-used (bytes)": overhead_dict_size + df_size + metadata_size + comment_size}
