from __future__ import annotations

import asyncio
import inspect
import itertools
from abc import abstractmethod
from collections.abc import AsyncIterator, Awaitable, Callable, Coroutine, Iterable, Iterator, Sequence
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime
from typing import Any, Generic, Literal, Type, TypeVar

import pandas as pd  # type: ignore
from pydantic import ValidationError

from . import TimeSeriesUserError
from .schema import CommentSupport, EnsembleMember, TimeSeriesComment, TimeSeriesMetadata
from .time_series import TimeSeries, TimeSeriesMetadataT, TimeSeriesT


def make_iterable(value: Any) -> Iterable[Any]:
    """Make an infinite iterable if it's not iterable or it's string."""
    if not isinstance(value, Iterable) or isinstance(value, str):
        return itertools.repeat(value)
    return value


T = TypeVar("T")


class TimeSeriesClient(Generic[TimeSeriesT, TimeSeriesMetadataT]):
    comment_support: CommentSupport = CommentSupport.UNSUPPORTED
    time_series_schema: Type[TimeSeriesMetadataT] = TimeSeriesMetadata  # type: ignore

    @classmethod
    def sanitize_metadata(
        cls,
        *,
        path: str | None = None,
        metadata: dict[str, Any] | TimeSeriesMetadata | None = None,
    ) -> TimeSeriesMetadataT:
        if not metadata and not path:
            raise TimeSeriesUserError("Invalid arguments: path and metadata cannot be both None", str(path))
        elif not metadata:
            metadata = cls.time_series_schema(path=path)
        else:
            if isinstance(metadata, TimeSeriesMetadata):
                metadata = metadata.dict()
            try:
                metadata = cls.time_series_schema.parse_obj({**metadata, "path": path})
            except ValidationError as e:
                raise TimeSeriesUserError(
                    f"Invalid metadata {metadata} for time series {path}", str(path)
                ) from e
        return metadata  # type: ignore

    @abstractmethod
    async def __aenter__(self) -> TimeSeriesClient[TimeSeriesT, TimeSeriesMetadataT]:
        """Enter the async context"""

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the async context"""

    def run_sync(
        self,
        coroutine: Callable[..., Coroutine[Any, Any, T]],
        *args: Any,
        **kwargs: Any,
    ) -> T:
        """This method safely calls async methods from a sync context."""
        if not inspect.iscoroutinefunction(coroutine):
            raise ValueError(f"Method: {coroutine}, is not a coroutine")
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            # No event loop is running. Using asyncio.run() is not safe,
            # because it cleans up event loops.
            try:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.__aenter__())
                result = loop.run_until_complete(coroutine(*args, **kwargs))
                loop.run_until_complete(self.__aexit__(None, None, None))
                return result
            except RuntimeError:
                # No event loop is running and we are not in the main thread.
                # This means we are in a threaded application not using event loop.
                # I think in this case asyncio.run() might be safe but lets keep it safe.
                with ThreadPoolExecutor(max_workers=1) as executor:
                    executor.submit(asyncio.run, self.__aenter__())  # type: ignore
                    future = executor.submit(asyncio.run, coroutine(*args, **kwargs))
                    wait([executor.submit(asyncio.run, self.__aexit__(None, None, None))])  # type: ignore
                    return future.result()

        # There is an event loop already running, but are in a sync context.
        # Calling the async methods from this method/thread is not possible, so
        # we spawn a new loop in a temporary thread. While not optimal from a
        # performance perspective, it ensures that both sync and async contexts
        # can share the OIDC client. As tokens are cached, sharing the client
        # is still much cheaper than the overhead of spawning a thread once in
        # a while. In performance-critical contexts, the overhead can be avoided
        # completely by using the async API
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(asyncio.run, self.__aenter__())  # type: ignore
            future = executor.submit(asyncio.run, coroutine(*args, **kwargs))
            wait([executor.submit(asyncio.run, self.__aexit__(None, None, None))])  # type: ignore
            return future.result()

    def iter_over_async(
        self, coroutine: Callable[..., AsyncIterator[T]], *args: Any, **kwargs: Any
    ) -> Iterator[T]:
        if not inspect.isasyncgenfunction(coroutine):
            raise ValueError(f"Method: {coroutine}, is not an async generator")
        ait = coroutine(*args, **kwargs)

        async def get_next() -> tuple[bool, T | None]:
            try:
                obj = await ait.__anext__()
                return False, obj
            except StopAsyncIteration:
                return True, None

        executor_context = None
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()
            run = loop.run_until_complete
        else:
            executor_context = ThreadPoolExecutor(max_workers=1).__enter__()

            def run(next_coroutine: Coroutine[Any, Any, Any]) -> Any:  # type: ignore
                return executor_context.submit(asyncio.run, next_coroutine).result()  # type: ignore

        run(self.__aenter__())
        done, obj = run(get_next())
        while not done:
            yield obj  # type: ignore
            done, obj = run(get_next())
        run(self.__aexit__(None, None, None))
        if executor_context:
            executor_context.__exit__(None, None, None)

    async def _bulk_concurrent(
        self,
        awaitables: list[Awaitable[Any]],
        concurrency_limit: int = 32,
        error_handling: Literal["default", "return", "raise"] = "default",
        default_value: Any = None,
        default_factory: Callable[Any] = None,
    ) -> list[Any]:
        """
        Utility method to asyncio gather awaitables without exceeding the concurrency_limit.

        Args:
            awaitables: The list of awaitables.
            concurrency_limit: The maximum concurrency tolerated.
            error_handling: If "default" return a default value, if "return" will return error objects
              and if "raise" will raise on first encountered error.
            default_value: The default value.
            default_factory: The default factory provider.

        Returns:
            The list of results.
        """
        sem = asyncio.Semaphore(concurrency_limit)

        async def task_wrapper(task: Awaitable[Any]) -> Any:
            try:
                result = await task
            except Exception as e:
                if error_handling == "raise":
                    raise  # Python catches here this raise, then executes finally then raises this
                elif error_handling == "return":
                    result = e
                elif default_factory is not None:
                    result = default_factory()
                else:
                    result = default_value
            finally:
                sem.release()
            return result

        tasks = []
        for awaitable in awaitables:
            await sem.acquire()
            tasks.append(asyncio.create_task(task_wrapper(awaitable)))

        for _ in range(concurrency_limit):
            await sem.acquire()
        return [t.result() for t in tasks]

    @abstractmethod
    async def create_time_series(
        self,
        *,
        path: str,
        metadata: dict[str, Any] | TimeSeriesMetadata | None = None,
        **kwargs: Any,
    ) -> TimeSeriesT:
        """
        Create a time series.

        Args:
            path: The time series path.
            metadata: The time series metadata.
            **kwargs: Additional backend specific keyword arguments.

        Returns:
            The TimeSeries object.
        """

    async def create_time_series_bulk(
        self,
        *,
        paths: list[str],
        metadatas: list[dict[str, Any] | TimeSeriesMetadata | None] = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = None,
        default_factory: Callable[Any] = None,
        **kwargs: Any,
    ) -> list[TimeSeriesT]:
        """
        Create all time series.

        Args:
            paths: The time series paths.
            metadatas: The time series metadatas.
            concurrency_limit: The maximum concurrency tolerated.
            error_handling: If "default" return a default value, if "return" will return error objects
              and if "raise" will raise on first encountered error.
            default_value: The default value.
            default_factory: The default factory provider.
            **kwargs: Additional backend specific keword arguments.

        Returns:
            The list of TimeSeries objects.
        """
        bulk_kwargs = {}
        if concurrency_limit:
            bulk_kwargs["concurrency_limit"] = concurrency_limit
        if error_handling:
            bulk_kwargs["error_handling"] = error_handling
        if default_value:
            bulk_kwargs["default_value"] = default_value
        if default_factory:
            bulk_kwargs["default_factory"] = default_factory
        return await self._bulk_concurrent(
            awaitables=[
                self.create_time_series(path=path, metadata=metadata, **kwargs)
                for path, metadata in zip(paths, metadatas)
            ],
            **bulk_kwargs,
        )

    @abstractmethod
    async def read_time_series(
        self, *, path: str, metadata_keys: list[str] | None = None, **kwargs: Any
    ) -> TimeSeriesT:
        """
        Get the TimeSeries by path.

        Args:
            path: The full qualified TimeSeries path.
            metadata_keys: list of metadata keys to read.  Set to None to request all metadata.
            **kwargs: Additional backend specific keyword arguments.

        Returns:
            The TimeSeries object.

        Examples:
            .. code-block:: python
                ts = await client.get_by_path("W7AgentTest/20003/S/cmd")
        """

    @abstractmethod
    def filter_time_series(
        self,
        *,
        ts_filter: str | None,
        metadata_keys: list[str] | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[TimeSeriesT]:
        """
        Get time series based on filter strings.

        Args:
            ts_filter: A time series filter.
            metadata_keys: list of metadata keys to read.  Set to None to request all metadata.
            **kwargs: Additional backend specific keyword arguments.

        Returns:
            An AsyncIterator over the returned TimeSeries objects.

        Examples:
            .. code-block:: python
                async for ts in client.filter_time_series(ts_filter="W7AgentTest/20004/S/*"):
                    print(ts.metadata)
        """

    async def read_time_series_bulk(
        self,
        *,
        paths: list[str] | None = None,
        ts_filters: list[str] | None = None,
        metadata_keys: list[str] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = None,
        default_factory: Callable[Any] = None,
        **kwargs,
    ) -> AsyncIterator[TimeSeriesT]:
        """
        Read time series in bulk, from either paths, time series filters or both.

        Args:
            paths: A list of time series paths.
            metadata_keys: A list of metadata keys to read. Set to None to request all metadata.
            ts_filters: A list of time series filters.
            concurrency_limit: The maximum concurrency tolerated.
            error_handling: If "default" return a default value, if "return" will return error objects
              and if "raise" will raise on first encountered error.
            default_value: The default value.
            default_factory: The default factory provider.
            **kwargs: Additional keyword arguments to be passed to the backend.

        Returns:
            An AsyncIterator over the resulting TimeSeries objects.
        """
        bulk_kwargs = {}
        if concurrency_limit:
            bulk_kwargs["concurrency_limit"] = concurrency_limit
        if error_handling:
            bulk_kwargs["error_handling"] = error_handling
        if default_value:
            bulk_kwargs["default_value"] = default_value
        if default_factory:
            bulk_kwargs["default_factory"] = default_factory
        if paths:
            for ts in await self._bulk_concurrent(
                awaitables=[
                    self.read_time_series(path=path, metadata_keys=metadata_keys, **kwargs)
                    for path in paths
                ],
                **bulk_kwargs,
            ):
                if ts is not None:
                    yield ts
        ts_a_iters = (
            [
                self.filter_time_series(ts_filter=ts_filter, metadata_keys=metadata_keys, **kwargs)
                for ts_filter in ts_filters
            ]
            if ts_filters
            else []
        )
        while len(ts_a_iters) > 0:
            ts_list = await self._bulk_concurrent(
                awaitables=[i.__anext__() for i in ts_a_iters], **bulk_kwargs
            )
            index_shift = 0
            for i, ts in enumerate(ts_list):
                if ts is not None:
                    yield ts
                else:
                    ts_a_iters.pop(i - index_shift)
                    index_shift += 1

    @abstractmethod
    async def update_time_series(
        self, *, path: str, metadata: dict[str, Any] | TimeSeriesMetadata, **kwargs: Any
    ) -> None:
        """
        Update the time series metadata.

        Args:
            path: The time series path.
            metadata: The time series metadata.
            **kwargs: Additional backend specific keyword arguments.
        """

    async def update_time_series_bulk(
        self,
        *,
        paths: list[str],
        metadatas: list[dict[str, Any] | TimeSeriesMetadata],
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[Any] = None,
        **kwargs: Any,
    ) -> None | list[Exception]:
        """
        Update time series metadata in bulk.

        Args:
            paths: A list of time series paths.
            metadatas: A list of time series metadatas.
            concurrency_limit: The maximum concurrency tolerated.
            error_handling: If "default" return a default value, if "return" will return error objects
              and if "raise" will raise on first encountered error.
            default_value: The default value.
            default_factory: The default factory provider.
            **kwargs: Additional backend specific keyword arguments.
        """
        bulk_kwargs = {}
        if concurrency_limit:
            bulk_kwargs["concurrency_limit"] = concurrency_limit
        if error_handling:
            bulk_kwargs["error_handling"] = error_handling
        if default_value:
            bulk_kwargs["default_value"] = default_value
        if default_factory:
            bulk_kwargs["default_factory"] = default_factory
        return [
            r
            for r in await self._bulk_concurrent(
                awaitables=[
                    self.update_time_series(path=path, metadata=metadata, **kwargs)
                    for path, metadata in zip(paths, metadatas)
                ],
                **bulk_kwargs,
            )
            if isinstance(r, Exception)
        ]

    @abstractmethod
    async def delete_time_series(self, *, path: str, **kwargs: Any) -> None:
        """
        Delete the time series.

        Args:
            path: The time series path.
            **kwargs: Additional backend specific keyword arguments.
        """

    async def delete_time_series_bulk(
        self,
        *,
        paths: list[str],
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[Any] = None,
        **kwargs: Any,
    ) -> None | list[Exception]:
        """
        Delete time series in bulk.

        Args:
            paths: A list of time series paths.
            concurrency_limit: The maximum concurrency tolerated.
            error_handling: If "default" return a default value, if "return" will return error objects
              and if "raise" will raise on first encountered error.
            default_value: The default value.
            default_factory: The default factory provider.
            **kwargs: Additional backend specific keyword arguments.
        """
        bulk_kwargs = {}
        if concurrency_limit:
            bulk_kwargs["concurrency_limit"] = concurrency_limit
        if error_handling:
            bulk_kwargs["error_handling"] = error_handling
        if default_value:
            bulk_kwargs["default_value"] = default_value
        if default_factory:
            bulk_kwargs["default_factory"] = default_factory
        return [
            r
            for r in await self._bulk_concurrent(
                awaitables=[self.delete_time_series(path=path, **kwargs) for path in paths],
                **bulk_kwargs,
            )
            if isinstance(r, Exception)
        ]

    @abstractmethod
    async def read_coverage(
        self,
        *,
        path: str,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs,
    ) -> tuple[datetime, datetime]:
        """
        Get the time series coverage.

        Args:
            path: The time series path.
            t0: The t0 of the ensemble member.
            dispatch_info: The dispatch info of the ensemble member.
            member: The member info of the ensemble member.

        Returns:
            A tuple of datetimes.
        """

    async def read_coverage_bulk(
        self,
        *,
        paths: Iterable[str],
        t0: datetime | Iterable[datetime | None] | None = None,
        dispatch_info: str | Iterable[str | None] | None = None,
        member: str | Iterable[str | None] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = (None, None),
        default_factory: Callable[Any] = None,
        **kwargs,
    ) -> Sequence[tuple[datetime, datetime]]:
        """
        Get the time series coverages.

        Args:
            paths: The time series paths.
            t0: An optional iterable of datetimes used to select the t0 in an ensemble TimeSeries, if a
                single datetime is passed it is used for all the TimeSeries.
            dispatch_info: An optional iterable of str used to select the dispatch info in an ensemble
                TimeSeries, if a single str is passed it is used for all the TimeSeries.
            member: An optional iterable of str used to select the member in an ensemble TimeSeries,
                if a single str is passed it is used for all the TimeSeries.
            concurrency_limit: The maximum concurrency tolerated.
            error_handling: If "default" return a default value, if "return" will return error objects
              and if "raise" will raise on first encountered error.
            default_value: The default value.
            default_factory: The default factory provider.

        Returns:
            A list of coverages.
        """
        bulk_kwargs = {}
        if concurrency_limit:
            bulk_kwargs["concurrency_limit"] = concurrency_limit
        if error_handling:
            bulk_kwargs["error_handling"] = error_handling
        if default_value:
            bulk_kwargs["default_value"] = default_value
        if default_factory:
            bulk_kwargs["default_factory"] = default_factory
        return await self._bulk_concurrent(
            awaitables=[
                self.read_coverage(
                    path=path, t0=t0_i, dispatch_info=dispatch_info_i, member=member_i, **kwargs
                )
                for path, t0_i, dispatch_info_i, member_i in zip(
                    paths,
                    make_iterable(t0),
                    make_iterable(dispatch_info),
                    make_iterable(member),
                )
            ],
            **bulk_kwargs,
        )

    @abstractmethod
    def read_ensemble_members(
        self,
        *,
        path: str,
        t0_start: datetime | None = None,
        t0_end: datetime | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[EnsembleMember]:
        """
        Read the ensemble members of a forecast time series.

        Args:
            path: The time series path.
            t0_start: The starting date from which to look for ensembles.
            t0_end: The ending date until which to look for ensembles.
            **kwargs: Additional backend specific keyword arguments.

        Returns:
            An AsyncIterator of EnsembleMember objects.
        """

    async def read_ensemble_members_bulk(
        self,
        *,
        paths: list[str],
        t0_start: list[datetime] | datetime | None = None,
        t0_end: list[datetime] | datetime | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = None,
        default_factory: Callable[Any] = None,
        **kwargs: Any,
    ) -> list[list[EnsembleMember]]:
        """
        read the ensemble members for multiple time series.

        Args:
            paths: A list of time series paths.
            t0_start: A list of t0 start times to filter for.
            t0_end: A listr of t0 end time to filter for.
            concurrency_limit: The maximum concurrency tolerated.
            error_handling: If "default" return a default value, if "return" will return error objects
              and if "raise" will raise on first encountered error.
            default_value: The default value.
            default_factory: The default factory provider.
            **kwargs: Additional backend specific keyword arguments.

        Returns:
            A list with the list of ensembles per each time series path.
        """
        bulk_kwargs = {}
        if concurrency_limit:
            bulk_kwargs["concurrency_limit"] = concurrency_limit
        if error_handling:
            bulk_kwargs["error_handling"] = error_handling
        if default_value:
            bulk_kwargs["default_value"] = default_value
        if default_factory:
            bulk_kwargs["default_factory"] = default_factory
        results = [[]] * len(paths)
        ensemble_a_iters = [
            self.read_ensemble_members(path=path, t0_start=t0_start_i, t0_end=t0_end_i, **kwargs)
            for path, t0_start_i, t0_end_i in zip(paths, make_iterable(t0_start), make_iterable(t0_end))
        ]
        unfinished_iters = len(ensemble_a_iters)
        while unfinished_iters > 0:
            ensemble_list = await self._bulk_concurrent(
                awaitables=[i.__anext__() for i in ensemble_a_iters], **bulk_kwargs
            )
            for i, ensemble in enumerate(ensemble_list):
                if ensemble is not None:
                    results[i].append(ensemble)
                else:
                    unfinished_iters -= 1
        return results

    @abstractmethod
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
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        This method returns the TimeSeries data between the start and end dates (both dates included)
        structured as a pandas DataFrame, the DataFrame index is localized in the TimeSeries timezone.

        Args:
            path: The time series path.
            start: The starting date from which the data will be returned.
            end: The ending date until which the data will be covered (end date included).
            columns: The list of column keys to read.
            t0: The t0 timestamp of the ensemble member.
            dispatch_info: Ensemble dispatch_info identifier.
            member: Ensemble member identifier.
            **kwargs: Additional backend specific keyword arguments.

        Returns:
            The DataFrame containing the TimeSeries data
        """

    @abstractmethod
    async def write_data_frame(
        self,
        *,
        path: str,
        data_frame: pd.DataFrame,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        This method writes the TimeSeries data from the data_frame into this TimeSeries.

        Args:
            path: The time series path.
            data_frame: The TimeSeries data to be written in the form of a pandas DataFrame.
            t0: The t0 time stamp of the ensemble member.
            dispatch_info: Ensemble dispatch_info identifier.
            member: Ensemble member identifier
            **kwargs: Additional backend specific keyword arguments.
        """

    @abstractmethod
    async def delete_data_range(
        self,
        *,
        path: str,
        start: datetime | None = None,
        end: datetime | None = None,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        This method deletes a range of data and/or an ensemble member from a time series.

        Args:
            path: The time series path.
            start: The starting date from which the data will be returned.
            end: The ending date until which the data will be covered.
            t0: The t0 time stamp of the ensemble member.
            dispatch_info: Ensemble dispatch_info identifier.
            member: Ensemble member identifier
            **kwargs: Additional backend specific keyword arguments.
        """

    async def read_data_frame_bulk(
        self,
        *,
        paths: Iterable[str],
        start: datetime | Iterable[datetime | None] | None = None,
        end: datetime | Iterable[datetime | None] | None = None,
        t0: datetime | Iterable[datetime | None] | None = None,
        dispatch_info: str | Iterable[str | None] | None = None,
        member: str | Iterable[str | None] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = None,
        default_factory: Callable[Any] = lambda: pd.DataFrame(index=pd.DatetimeIndex([])),
        **kwargs: Any,
    ) -> dict[str, pd.DataFrame]:
        """
        Read multiple TimeSeries as data frames.

        Notes:
            This method can be overwritten on backends which support bulk operations.

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
            concurrency_limit: The maximum concurrency tolerated.
            error_handling: If "default" return a default value, if "return" will return error objects
              and if "raise" will raise on first encountered error.
            default_value: The default value.
            default_factory: The default factory provider.
            **kwargs: Additional backend specific keyword arguments.
        """
        bulk_kwargs = {}
        if concurrency_limit:
            bulk_kwargs["concurrency_limit"] = concurrency_limit
        if error_handling:
            bulk_kwargs["error_handling"] = error_handling
        if default_value:
            bulk_kwargs["default_value"] = default_value
        if default_factory:
            bulk_kwargs["default_factory"] = default_factory
        return {
            path: df
            for path, df in zip(
                paths,
                await self._bulk_concurrent(
                    awaitables=[
                        self.read_data_frame(
                            path=path,
                            start=start_i,
                            end=end_i,
                            t0=t0_i,
                            dispatch_info=dispatch_info_i,
                            member=member_i,
                            **kwargs,
                        )
                        for path, start_i, end_i, t0_i, dispatch_info_i, member_i in zip(
                            paths,
                            make_iterable(start),
                            make_iterable(end),
                            make_iterable(t0),
                            make_iterable(dispatch_info),
                            make_iterable(member),
                        )
                    ],
                    **bulk_kwargs,
                ),
            )
        }

    async def read_data_frames(
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

        TODO: deprecate in favor of the convention name.

        Notes:
            This method can be overwritten on backends which support bulk operations.

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
            concurrency_limit: The maximum concurrency tolerated.
            error_handling: If "default" return a default value, if "return" will return error objects
              and if "raise" will raise on first encountered error.
            default_value: The default value.
            default_factory: The default factory provider.
            **kwargs: Additional backend specific keyword arguments.
        """
        return await self.read_data_frame_bulk(
            paths=paths, start=start, end=end, t0=t0, dispatch_info=dispatch_info, member=member, **kwargs
        )

    async def write_data_frame_bulk(
        self,
        *,
        paths: Iterable[str],
        data_frames: Iterable[pd.DataFrame],
        t0: datetime | Iterable[datetime | None] | None = None,
        dispatch_info: str | Iterable[str | None] | None = None,
        member: str | Iterable[str | None] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[Any] = None,
        **kwargs: Any,
    ) -> None | list[Exception]:
        """
        Write multiple data frames to TimeSeries

        Notes:
            This method can be overwritten on backends which support bulk operations.

        Args:
            paths: An iterable of time series paths.
            data_frames: An iterable of DataFrames
            t0: An optional iterable of datetimes used to select the t0 in an ensemble TimeSeries,
                if a single datetime is passed it is used for all the TimeSeries.
            dispatch_info: An optional iterable of str used to select the dispatch info in an ensemble
                TimeSeries, if a single str is passed it is used for all the TimeSeries.
            member: An optional iterable of str used to select the member in an ensemble TimeSeries,
                if a single str is passed it is used for all the TimeSeries.
            concurrency_limit: The maximum concurrency tolerated.
            error_handling: If "default" return a default value, if "return" will return error objects
              and if "raise" will raise on first encountered error.
            default_value: The default value.
            default_factory: The default factory provider.
            **kwargs: Additional backend specific keyword arguments.
        """
        bulk_kwargs = {}
        if concurrency_limit:
            bulk_kwargs["concurrency_limit"] = concurrency_limit
        if error_handling:
            bulk_kwargs["error_handling"] = error_handling
        if default_value:
            bulk_kwargs["default_value"] = default_value
        if default_factory:
            bulk_kwargs["default_factory"] = default_factory
        return [
            r
            for r in await self._bulk_concurrent(
                awaitables=[
                    self.write_data_frame(
                        path=path,
                        data_frame=df,
                        t0=t0_i,
                        dispatch_info=dispatch_info_i,
                        member=member_i,
                        **kwargs,
                    )
                    for path, df, t0_i, dispatch_info_i, member_i in zip(
                        paths,
                        data_frames,
                        make_iterable(t0),
                        make_iterable(dispatch_info),
                        make_iterable(member),
                    )
                ],
                **bulk_kwargs,
            )
            if isinstance(r, Exception)
        ]

    async def write_data_frames(
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

        TODO: deprecate in favor of the convention name.

        Notes:
            This method can be overwritten on backends which support bulk operations.

        Args:
            paths: An iterable of time series paths.
            data_frames: An iterable of DataFrames
            t0: An optional iterable of datetimes used to select the t0 in an ensemble TimeSeries,
                if a single datetime is passed it is used for all the TimeSeries.
            dispatch_info: An optional iterable of str used to select the dispatch info in an ensemble
                TimeSeries, if a single str is passed it is used for all the TimeSeries.
            member: An optional iterable of str used to select the member in an ensemble TimeSeries,
                if a single str is passed it is used for all the TimeSeries.
            **kwargs: Additional backend specific keyword arguments.
        """
        await self.write_data_frame_bulk(
            paths=paths, data_frames=data_frames, t0=t0, dispatch_info=dispatch_info, member=member
        )

    async def delete_data_range_bulk(
        self,
        *,
        paths: list[str],
        start: datetime | Iterable[datetime | None] | None = None,
        end: datetime | Iterable[datetime | None] | None = None,
        t0: datetime | Iterable[datetime | None] | None = None,
        dispatch_info: str | Iterable[str | None] | None = None,
        member: str | Iterable[str | None] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[Any] = None,
        **kwargs: Any,
    ) -> None | list[Exception]:
        """
        Delete time series data in a bulk

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
            concurrency_limit: The maximum concurrency tolerated.
            error_handling: If "default" return a default value, if "return" will return error objects
              and if "raise" will raise on first encountered error.
            default_value: The default value.
            default_factory: The default factory provider.
            **kwargs: Additional backend specific keyword arguments.
        """
        bulk_kwargs = {}
        if concurrency_limit:
            bulk_kwargs["concurrency_limit"] = concurrency_limit
        if error_handling:
            bulk_kwargs["error_handling"] = error_handling
        if default_value:
            bulk_kwargs["default_value"] = default_value
        if default_factory:
            bulk_kwargs["default_factory"] = default_factory
        return [
            r
            for r in await self._bulk_concurrent(
                awaitables=[
                    self.delete_data_range(
                        path=path,
                        start=start_i,
                        end=end_i,
                        t0=t0_i,
                        dispatch_info=dispatch_info_i,
                        member=member_i,
                        **kwargs,
                    )
                    for path, start_i, end_i, t0_i, dispatch_info_i, member_i in zip(
                        paths,
                        make_iterable(start),
                        make_iterable(end),
                        make_iterable(t0),
                        make_iterable(dispatch_info),
                        make_iterable(member),
                    )
                ],
                **bulk_kwargs,
            )
            if isinstance(r, Exception)
        ]

    def read_comments(
        self,
        *,
        path: str,
        start: datetime | None = None,
        end: datetime | None = None,
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[TimeSeriesComment]:
        """
        Read the time series comments.

        Args:
            path: The time series path.
            start: The datetime from which to retrieve comments.
            end: The datetime until which to retrieve comments.
            t0: The t0 timestamp of the ensemble member.
            dispatch_info: Ensemble dispatch_info identifier.
            member: Ensemble member identifier
            **kwargs: Additional backend specific keyword arguments.

        Returns:
            An iterable of TimeSeriesComment objects.
        """
        raise NotImplementedError

    async def write_comments(
        self,
        *,
        path: str,
        comments: list[TimeSeriesComment],
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Write a list of time series comments.

        Args:
            path: The time series path.
            comments: The time series comments.
            t0: The t0 timestamp of the ensemble member.
            dispatch_info: Ensemble dispatch_info identifier.
            member: Ensemble member identifier
            **kwargs: Additional backend specific keyword arguments.
        """
        raise NotImplementedError

    async def delete_comments(
        self,
        path: str,
        comments: list[TimeSeriesComment],
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Delete time series comments.

        Args:
            path: The time series path.
            comments: The time series comments to delete.
            t0: The t0 timestamp of the ensemble member.
            dispatch_info: Ensemble dispatch_info identifier.
            member: Ensemble member identifier
            **kwargs: Additional backend specific keyword arguments.
        """
        raise NotImplementedError

    async def read_comments_bulk(
        self,
        *,
        paths: list[str],
        start: datetime | Iterable[datetime | None] | None = None,
        end: datetime | Iterable[datetime | None] | None = None,
        t0: datetime | Iterable[datetime | None] | None = None,
        dispatch_info: str | Iterable[str | None] | None = None,
        member: str | Iterable[str | None] | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = None,
        default_value: Any = None,
        default_factory: Callable[Any] = None,
        **kwargs: Any,
    ):
        """
        Read time series comments in bulk

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
            concurrency_limit: The maximum concurrency tolerated.
            error_handling: If "default" return a default value, if "return" will return error objects
              and if "raise" will raise on first encountered error.
            default_value: The default value.
            default_factory: The default factory provider.
            **kwargs: Additional backend specific keyword arguments.

        Returns:
            A list per each path with a list of comments.
        """
        bulk_kwargs = {}
        if concurrency_limit:
            bulk_kwargs["concurrency_limit"] = concurrency_limit
        if error_handling:
            bulk_kwargs["error_handling"] = error_handling
        if default_value:
            bulk_kwargs["default_value"] = default_value
        if default_factory:
            bulk_kwargs["default_factory"] = default_factory
        results = [[]] * len(paths)
        comments_a_iters = [
            self.read_comments(path=path, start=start_i, end=end_i, **kwargs)
            for path, start_i, end_i, t0_i, dispatch_info_i, member_i in zip(
                paths,
                make_iterable(start),
                make_iterable(end),
                make_iterable(t0),
                make_iterable(dispatch_info),
                make_iterable(member),
            )
        ]
        unfinished_iters = len(comments_a_iters)
        while unfinished_iters > 0:
            comments_list = await self._bulk_concurrent(
                awaitables=[i.__anext__() for i in comments_a_iters], **bulk_kwargs
            )
            for i, comment in enumerate(comments_list):
                if comment is not None:
                    results[i].append(comment)
                else:
                    unfinished_iters -= 1
        return results

    async def write_comments_bulk(
        self,
        *,
        paths: list[str],
        comments: list[list[TimeSeriesComment]],
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[Any] = None,
        **kwargs: Any,
    ) -> None | list[Exception]:
        """
        Write time series comments in bulk

        Args:
            paths: An iterable of time series paths.
            comments: A list containing a list of comment per each time series path.
            t0: An optional iterable of datetimes used to select the t0 in an ensemble TimeSeries, if a
                single datetime is passed it is used for all the TimeSeries.
            dispatch_info: An optional iterable of str used to select the dispatch info in an ensemble
                TimeSeries, if a single str is passed it is used for all the TimeSeries.
            member: An optional iterable of str used to select the member in an ensemble TimeSeries,
                if a single str is passed it is used for all the TimeSeries.
            concurrency_limit: The maximum concurrency tolerated.
            error_handling: If "default" return a default value, if "return" will return error objects
              and if "raise" will raise on first encountered error.
            default_value: The default value.
            default_factory: The default factory provider.
            **kwargs: Additional backend specific keyword arguments.
        """
        bulk_kwargs = {}
        if concurrency_limit:
            bulk_kwargs["concurrency_limit"] = concurrency_limit
        if error_handling:
            bulk_kwargs["error_handling"] = error_handling
        if default_value:
            bulk_kwargs["default_value"] = default_value
        if default_factory:
            bulk_kwargs["default_factory"] = default_factory
        return [
            r
            for r in await self._bulk_concurrent(
                awaitables=[
                    self.write_comments(
                        path=path,
                        comments=comments_i,
                        t0=t0_i,
                        dispatch_info=dispatch_info_i,
                        member=member_i,
                        **kwargs,
                    )
                    for path, comments_i, t0_i, dispatch_info_i, member_i in zip(
                        paths,
                        comments,
                        make_iterable(t0),
                        make_iterable(dispatch_info),
                        make_iterable(member),
                    )
                ],
                **bulk_kwargs,
            )
            if isinstance(r, Exception)
        ]

    async def delete_comments_bulk(
        self,
        *,
        paths: list[str],
        comments: list[list[TimeSeriesComment]],
        t0: datetime | None = None,
        dispatch_info: str | None = None,
        member: str | None = None,
        concurrency_limit: int | None = None,
        error_handling: Literal["default", "return", "raise"] | None = "return",
        default_value: Any = None,
        default_factory: Callable[Any] = None,
        **kwargs: Any,
    ) -> None | list[Exception]:
        """
        Delete time series comments in bulk

        Args:
            paths: An iterable of time series paths.
            comments: A list containing a list of comment per each time series path.
            t0: An optional iterable of datetimes used to select the t0 in an ensemble TimeSeries, if a
                single datetime is passed it is used for all the TimeSeries.
            dispatch_info: An optional iterable of str used to select the dispatch info in an ensemble
                TimeSeries, if a single str is passed it is used for all the TimeSeries.
            member: An optional iterable of str used to select the member in an ensemble TimeSeries,
                if a single str is passed it is used for all the TimeSeries.
            concurrency_limit: The maximum concurrency tolerated.
            error_handling: If "default" return a default value, if "return" will return error objects
              and if "raise" will raise on first encountered error.
            default_value: The default value.
            default_factory: The default factory provider.
            **kwargs: Additional backend specific keyword arguments.
        """
        bulk_kwargs = {}
        if concurrency_limit:
            bulk_kwargs["concurrency_limit"] = concurrency_limit
        if error_handling:
            bulk_kwargs["error_handling"] = error_handling
        if default_value:
            bulk_kwargs["default_value"] = default_value
        if default_factory:
            bulk_kwargs["default_factory"] = default_factory
        return [
            r
            for r in await self._bulk_concurrent(
                awaitables=[
                    self.delete_comments(
                        path=path,
                        comments=comments_i,
                        t0=t0_i,
                        dispatch_info=dispatch_info_i,
                        member=member_i,
                        **kwargs,
                    )
                    for path, comments_i, t0_i, dispatch_info_i, member_i in zip(
                        paths,
                        comments,
                        make_iterable(t0),
                        make_iterable(dispatch_info),
                        make_iterable(member),
                    )
                ],
                **bulk_kwargs,
            )
            if isinstance(r, Exception)
        ]

    async def info(self) -> dict[str, Any]:
        """
        Return information of the store or fail if the store has any problem.

        NOTE: this default implementation should be overwritten on each implementation.
        """
        return {}


TimeSeriesClientT = TypeVar("TimeSeriesClientT", bound=TimeSeriesClient[TimeSeries, TimeSeriesMetadata])
