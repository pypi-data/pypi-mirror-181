from kisters.water.time_series.core import TimeSeries, TimeSeriesStore

from .parquet_time_series_client import ParquetTimeSeriesClient


class ParquetStore(TimeSeriesStore[ParquetTimeSeriesClient, TimeSeries]):
    """ParquetStore provides a TimeSeriesStore for time series stored in Parquet files.

    Args:
        filename: The path to the Parquet file used for storage.

    Examples:
        .. code-block:: python

            from kisters.water.time_series.parquet import ParquetStore

            ts_store = ParquetStore("test.pq")
            ts = ts_store.get_by_path("validation/inner_consistency1/station1/H")
    """

    def __init__(self, filename: str):
        self.client = ParquetTimeSeriesClient(filename)
