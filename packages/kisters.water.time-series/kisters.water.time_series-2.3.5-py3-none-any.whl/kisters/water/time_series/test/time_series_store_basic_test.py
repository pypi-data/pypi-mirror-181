from __future__ import annotations

import itertools
import uuid
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pytest

from kisters.water.time_series.core import EnsembleMember, TimeSeries, TimeSeriesStore


class TimeSeriesStoreBasicTest:
    STORE: TimeSeriesStore
    TS_PATH = f"{str(uuid.uuid4())}"
    TIME_SERIES_MAP: dict[str, TimeSeries | None] = {}
    TS_METADATA = {}
    ENSEMBLE_TS_PATH = f"{str(uuid.uuid4())}"
    ENSEMBLE_MEMBERS = [
        EnsembleMember(
            t0=datetime(year=2020, month=1, day=1, tzinfo=timezone.utc),
            dispatch_info="info1",
            member="0",
        ),
        EnsembleMember(
            t0=datetime(year=2020, month=1, day=1, tzinfo=timezone.utc),
            dispatch_info="info1",
            member="1",
        ),
        EnsembleMember(
            t0=datetime(year=2020, month=1, day=1, tzinfo=timezone.utc),
            dispatch_info="info2",
            member="0",
        ),
        EnsembleMember(
            t0=datetime(year=2020, month=1, day=1, tzinfo=timezone.utc),
            dispatch_info="info2",
            member="1",
        ),
        EnsembleMember(
            t0=datetime(year=2020, month=1, day=1, hour=12, tzinfo=timezone.utc),
            dispatch_info="info1",
            member="0",
        ),
        EnsembleMember(
            t0=datetime(year=2020, month=1, day=1, hour=12, tzinfo=timezone.utc),
            dispatch_info="info1",
            member="1",
        ),
        EnsembleMember(
            t0=datetime(year=2020, month=1, day=1, hour=12, tzinfo=timezone.utc),
            dispatch_info="info2",
            member="0",
        ),
        EnsembleMember(
            t0=datetime(year=2020, month=1, day=1, hour=12, tzinfo=timezone.utc),
            dispatch_info="info2",
            member="1",
        ),
    ]
    TS_ENSEMBLE_METADATA = {"is_forecast": True}
    WRITE_KWARGS = {}

    @pytest.mark.parametrize("path", [TS_PATH, ENSEMBLE_TS_PATH])
    def test_01_create_time_series(self, path: str):
        if path == self.TS_PATH:
            metadata = self.TS_METADATA
        else:
            metadata = self.TS_ENSEMBLE_METADATA
        ts = self.STORE.create_time_series(path=path, metadata=metadata)
        self.TIME_SERIES_MAP[path] = ts
        assert ts is not None
        assert ts.path in path
        assert ts.metadata is not None
        assert ts.columns is not None

    @pytest.mark.parametrize("path", [TS_PATH, ENSEMBLE_TS_PATH])
    def test_02_get_by_path(self, path: str):
        ts = self.STORE.get_by_path(path)
        assert ts.path == self.TIME_SERIES_MAP[path].path
        assert ts.metadata == self.TIME_SERIES_MAP[path].metadata
        assert ts.columns == self.TIME_SERIES_MAP[path].columns

    def test_03_get_by_path_multiple(self):
        ts_path = f"{str(uuid.uuid4())}"
        ts_path2 = f"{ts_path}/sub"
        self.STORE.create_time_series(path=ts_path, metadata=self.TS_METADATA)
        self.STORE.create_time_series(path=ts_path2, metadata=self.TS_METADATA)
        paths = [self.TS_PATH, ts_path, ts_path2]
        ts_list = self.STORE.get_by_path(*paths)
        for i, ts in enumerate(ts_list):
            assert ts.path == paths[i]

    def test_04_filter_time_series(self):
        ts_list = list(self.STORE.get_by_filter(self.TS_PATH))
        assert len(ts_list) == 1
        assert ts_list[0].path == self.TS_PATH
        ts_list = list(self.STORE.get_by_filter("*"))
        assert len(ts_list) == 4
        ts_list = list(self.STORE.get_by_filter(self.TS_PATH, "*"))
        assert len(ts_list) == 5

    def test_05_update_ts_metadata(self):
        ts = self.TIME_SERIES_MAP[self.TS_PATH]
        metadata = ts.metadata
        metadata["attr1"] = 1234
        metadata["attr2"] = "value"
        metadata["attr3"] = True
        metadata["attr4"] = 288.5
        ts.update_metadata(metadata)
        assert ts.metadata["attr1"] == 1234
        assert ts.metadata["attr2"] == "value"
        assert ts.metadata["attr3"]
        assert ts.metadata["attr4"] == 288.5

    def test_06_delete_ts_metadata(self):
        ts = self.TIME_SERIES_MAP[self.TS_PATH]
        assert "attr1" in ts.metadata
        assert "attr2" in ts.metadata
        assert "attr3" in ts.metadata
        assert "attr4" in ts.metadata
        metadata = ts.metadata
        del metadata["attr1"]
        del metadata["attr2"]
        del metadata["attr3"]
        del metadata["attr4"]
        ts.update_metadata(metadata)
        assert "attr1" not in ts.metadata
        assert "attr2" not in ts.metadata
        assert "attr3" not in ts.metadata
        assert "attr4" not in ts.metadata

    def test_07_write_data_frame(self):
        index = pd.date_range("2020-01-01", "2020-03-01", freq="5min", tz="utc")
        df = pd.DataFrame({"value": np.linspace(0, 100, index.shape[0])}, index=index)
        ts = self.TIME_SERIES_MAP[self.TS_PATH]
        ts.write_data_frame(data_frame=df, **self.WRITE_KWARGS)
        read_df = ts.read_data_frame()
        assert np.allclose(df.values, read_df.loc[:, ["value"]].values)

    def test_08_read_coverage(self):
        coverage = self.TIME_SERIES_MAP[self.TS_PATH].coverage()
        coverage_from = self.TIME_SERIES_MAP[self.TS_PATH].coverage_from()
        coverage_until = self.TIME_SERIES_MAP[self.TS_PATH].coverage_until()
        date_from = datetime(year=2020, month=1, day=1, tzinfo=timezone.utc)
        date_until = datetime(year=2020, month=3, day=1, tzinfo=timezone.utc)
        assert coverage[0].replace(tzinfo=None) == date_from.replace(tzinfo=None)
        assert coverage[0].utcoffset() == date_from.utcoffset()
        assert coverage[1].replace(tzinfo=None) == date_until.replace(tzinfo=None)
        assert coverage[1].utcoffset() == date_until.utcoffset()
        assert coverage_from.replace(tzinfo=None) == date_from.replace(tzinfo=None)
        assert coverage_from.utcoffset() == date_from.utcoffset()
        assert coverage_until.replace(tzinfo=None) == date_until.replace(tzinfo=None)
        assert coverage_until.utcoffset() == date_until.utcoffset()

    def test_09_read_data_frame(self):
        start = pd.to_datetime("2020-02-01", utc=True)
        end = pd.to_datetime("2020-02-15", utc=True)
        ts = self.TIME_SERIES_MAP[self.TS_PATH]
        df = ts.read_data_frame(start=start, end=end)
        assert df.index[0] == start
        assert df.index[-1] == end

    def test_10_bulk_write(self):
        ts_list = [self.TIME_SERIES_MAP[self.ENSEMBLE_TS_PATH]] * len(self.ENSEMBLE_MEMBERS)
        t0s, dispatch_infos, members = [], [], []
        for ensemble in self.ENSEMBLE_MEMBERS:
            t0s.append(ensemble.t0)
            dispatch_infos.append(ensemble.dispatch_info)
            members.append(ensemble.member)
        index = pd.date_range("2020-03-01", "2020-04-01", freq="5min", tz="utc")
        df = pd.DataFrame({"value": np.linspace(0, 100, index.shape[0])}, index=index)
        self.STORE.write_data_frames(
            paths=[self.ENSEMBLE_TS_PATH] * len(self.ENSEMBLE_MEMBERS),
            data_frames=itertools.repeat(df),
            t0=t0s,
            dispatch_info=dispatch_infos,
            member=members,
            **self.WRITE_KWARGS,
        )
        ts = ts_list[0]
        for ensemble in self.ENSEMBLE_MEMBERS:
            assert ts.coverage_until(**ensemble.dict()) == index[-1].to_pydatetime()

    def test_11_bulk_read(self):
        paths = [self.TS_PATH] + [self.ENSEMBLE_TS_PATH] * len(self.ENSEMBLE_MEMBERS)
        t0s, dispatch_infos, members = [None], [None], [None]
        start = datetime(year=2020, month=2, day=1, tzinfo=timezone.utc)
        end = datetime(year=2020, month=3, day=15, tzinfo=timezone.utc)
        for ensemble in self.ENSEMBLE_MEMBERS:
            t0s.append(ensemble.t0)
            dispatch_infos.append(ensemble.dispatch_info)
            members.append(ensemble.member)
        bulk_map = self.STORE.read_data_frames(
            paths=paths,
            start=start,
            end=end,
            t0=t0s,
            dispatch_info=dispatch_infos,
            member=members,
        )
        for df in bulk_map.values():
            assert df.loc[df.index < start].shape[0] == 0
            assert df.loc[df.index > end].shape[0] == 0

    def test_12_read_ensembles(self):
        ts = self.TIME_SERIES_MAP[self.ENSEMBLE_TS_PATH]
        start_00 = datetime(year=2020, month=1, day=1, tzinfo=timezone.utc)
        start_12 = datetime(year=2020, month=1, day=1, hour=12, tzinfo=timezone.utc)
        ensembles = list(ts.ensemble_members())
        assert len(ensembles) == 8
        for i in range(len(ensembles)):
            if i // 4 % 2 == 0:
                date = start_00
            else:
                date = start_12
            assert ensembles[i].t0.isoformat() == date.isoformat()
            if i // 2 % 2 == 0:
                info = "info1"
            else:
                info = "info2"
            assert ensembles[i].dispatch_info == info
            if i % 2 == 0:
                member = "0"
            else:
                member = "1"
            assert ensembles[i].member == member

    def test_13_filter_ensembles(self):
        ts = self.TIME_SERIES_MAP[self.ENSEMBLE_TS_PATH]
        start_00 = datetime(year=2020, month=1, day=1, tzinfo=timezone.utc)
        ensembles = list(ts.ensemble_members(t0_start=start_00, t0_end=start_00))
        assert len(ensembles) == 4
        for i in range(len(ensembles)):
            assert ensembles[i].t0.isoformat() == start_00.isoformat()
            if i // 2 == 0:
                info = "info1"
            else:
                info = "info2"
            assert ensembles[i].dispatch_info == info
            if i % 2 == 0:
                member = "0"
            else:
                member = "1"
            assert ensembles[i].member == member

    def test_14_delete_time_series(self):
        for ts in self.STORE.get_by_filter("*"):
            self.STORE.delete_time_series(path=ts.path)
        assert len(list(self.STORE.get_by_filter("*"))) == 0
