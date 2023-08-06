from __future__ import annotations

from collections.abc import Iterable, Iterator
from datetime import datetime
from typing import Any, Generic

import pandas as pd  # type: ignore

from .schema import CommentSupport, TimeSeriesMetadata
from .time_series import TimeSeriesT
from .time_series_client import TimeSeriesClientT


class TimeSeriesStore(Generic[TimeSeriesClientT, TimeSeriesT]):
    """This abstract class defines the API of the TimeSeriesStore."""

    client: TimeSeriesClientT

    @property
    def comment_support(self) -> CommentSupport:
        return self.client.comment_support

    def get_by_path(
        self,
        *path: str,
        metadata_keys: list[str] | None = None,
        **kwargs: Any,
    ) -> TimeSeriesT | Iterator[TimeSeriesT]:
        """
        Get the TimeSeries by path.

        Args:
            *path: The full qualified TimeSeries path.
            metadata_keys: list of metadata keys to read.  Set to None to request all metadata.
            **kwargs: The additional keyword arguments which are passed to the backend.

        Returns:
            The TimeSeries object.

        Examples:
            .. code-block:: python

                ts = store.get_by_path("W7AgentTest/20003/S/cmd")
                ts1, ts2 = store.get_by_path("example_path_1", "example_path_2")
        """
        time_series = (
            self.client.run_sync(
                self.client.read_time_series,
                path=p,
                metadata_keys=metadata_keys,
                **kwargs,
            )
            for p in path
        )
        if len(path) == 1:
            return next(time_series)  # type: ignore
        else:
            return iter(time_series)  # type: ignore

    def get_by_filter(
        self,
        *ts_filter: str | None,
        metadata_keys: list[str] | None = None,
        **kwargs: Any,
    ) -> Iterable[TimeSeriesT]:
        """
        Get the TimeSeries list by filter.

        Args:
            *ts_filter: An iterable of TimeSeries paths or filters.
            metadata_keys: list of metadata keys to read.  Set to None to request all metadata.
            **kwargs: The additional keyword arguments, which are passed to the backend.

        Returns:
            The list of the found TimeSeries objects.

        Examples:
            .. code-block:: python

                store.get_by_filter("W7AgentTest/20004/S/*")
                store.get_by_filter("*Test", "*Ensemble")
        """
        time_series = (
            self.client.iter_over_async(
                self.client.filter_time_series,
                ts_filter=f,
                metadata_keys=metadata_keys,
                **kwargs,
            )
            for f in ts_filter
        )
        return (ts for ts_iter in time_series for ts in ts_iter)  # type: ignore

    def create_time_series(
        self,
        *,
        path: str,
        metadata: dict[str, Any] | TimeSeriesMetadata | None = None,
        **kwargs: Any,
    ) -> TimeSeriesT:
        """
        Create an empty TimeSeries.

        Args:
            path: The TimeSeries path.
            metadata: The metadata of the TimeSeries.
            **kwargs: Additional keyword arguments supported by the backend.
        """
        return self.client.run_sync(  # type: ignore
            self.client.create_time_series, path=path, metadata=metadata, **kwargs
        )

    def delete_time_series(self, *, path: str, **kwargs: Any) -> None:
        """
        Delete a TimeSeries.

        Args:
            path: The TimeSeries path.
            **kwargs: Additional keyword arguments supported by the backend.

        """
        self.client.run_sync(self.client.delete_time_series, path=path, **kwargs)

    def read_data_frames(
        self,
        *,
        paths: Iterable[str],
        start: datetime | Iterable[datetime | None] | None = None,
        end: datetime | Iterable[datetime | None] | None = None,
        t0: datetime | Iterable[datetime | None] | None = None,
        dispatch_info: str | Iterable[str | None] | None = None,
        member: str | Iterable[str | None] | None = None,
        **kwargs: Any,
    ) -> dict[str, pd.DataFrame]:
        """
        Read multiple TimeSeries as data frames.

        Args:
            paths: An iterable of time series paths.
            start: An optional iterable of datetimes representing the date from which data will be written,
                if a single datetime is passed it is used for all the TimeSeries.
            end: An optional iterable of datetimes representing the date until (included) which data will be
                written, if a single datetime is passed it is used for all the TimeSeries.
            t0: An optional iterable of datetimes used to select the t0 in an ensemble TimeSeries, if a
                single datetime is passed it is used for all the TimeSeries.
            dispatch_info: An optional iterable of str used to select the dispatch info in an ensemble
                TimeSeries, if a single str is passed it is used for all the TimeSeries.
            member: An optional iterable of str used to select the member in an ensemble TimeSeries,
                if a single str is passed it is used for all the TimeSeries.
            **kwargs: The additional keyword arguments which are passed to the backend.
        """
        return self.client.run_sync(
            self.client.read_data_frames,
            paths=paths,
            start=start,
            end=end,
            t0=t0,
            dispatch_info=dispatch_info,
            member=member,
            **kwargs,
        )

    def write_data_frames(
        self,
        *,
        paths: Iterable[str],
        data_frames: Iterable[pd.DataFrame],
        t0: datetime | Iterable[datetime | None] | None = None,
        dispatch_info: str | Iterable[str | None] | None = None,
        member: str | Iterable[str | None] | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Write multiple data frames to TimeSeries

        Args:
            paths: An iterable of time series paths.
            data_frames: An iterable of DataFrames
            t0: An optional iterable of datetimes used to select the t0 in an ensemble TimeSeries,
                if a single datetime is passed it is used for all the TimeSeries.
            dispatch_info: An optional iterable of str used to select the dispatch info in an ensemble
                TimeSeries, if a single str is passed it is used for all the TimeSeries.
            member: An optional iterable of str used to select the member in an ensemble TimeSeries,
                if a single str is passed it is used for all the TimeSeries.
            **kwargs: The additional keyword arguments which are passed to the backend.

        """
        return self.client.run_sync(
            self.client.write_data_frames,
            paths=paths,
            data_frames=data_frames,
            t0=t0,
            dispatch_info=dispatch_info,
            member=member,
            **kwargs,
        )
