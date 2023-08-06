# In order to use broader scopes for asynchronous fixtures e.g. "class"
# the pytest-asyncio event_loop fixture needs to have a broader scope
# More info: https://github.com/pytest-dev/pytest-asyncio/issues/171
import asyncio

import pytest

from kisters.water.time_series.memory import MemoryStore
from kisters.water.time_series.parquet import ParquetStore


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def memory_store():
    store = MemoryStore()
    yield store
    for ts in store.get_by_filter("*"):
        store.delete_time_series(path=ts.path)


@pytest.fixture(scope="class")
def memory_store_cls(request, memory_store):
    request.cls.STORE = memory_store


@pytest.fixture(scope="session")
def parquet_store():
    store = ParquetStore("test.pq")
    yield store
    store.client._filename.unlink()


@pytest.fixture(scope="class")
def parquet_store_cls(request, parquet_store):
    request.cls.STORE = parquet_store
