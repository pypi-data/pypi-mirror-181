from datetime import datetime, timezone
from enum import Enum, Flag, auto
from typing import Any, List, Optional

import numpy as np
from pydantic import BaseModel, Extra, Field, validator


class Model(BaseModel):
    class Config:
        # Forbid by default to avoid common errors such as misnamed fields
        extra = Extra.forbid
        # Makes serialization clearer
        use_enum_values = True


class TimeSeriesColumn(Model):
    key: str
    dtype: str

    class Config:
        extra = Extra.allow

    @validator("dtype", pre=True, always=True)
    def check_dtype(cls, value: Any) -> str:
        return str(np.dtype(value))


# Column conventions
VALUE_COLUMN_KEY = "value"
QUALITY_COLUMN_KEY = "quality"
COMMENT_COLUMN_KEY = "comment"

DEFAULT_VALUE_COLUMN = TimeSeriesColumn(key=VALUE_COLUMN_KEY, dtype="float32")
DEFAULT_QUALITY_COLUMN = TimeSeriesColumn(key=QUALITY_COLUMN_KEY, dtype="uint8")
DEFAULT_COMMENT_COLUMN = TimeSeriesColumn(key=COMMENT_COLUMN_KEY, dtype="str")

DEFAULT_TIME_SERIES_COLUMNS = [DEFAULT_VALUE_COLUMN]


class EnsembleMember(Model):
    t0: Optional[datetime] = None
    dispatch_info: Optional[str] = None
    member: Optional[str] = None

    @validator("t0", pre=True, always=True)
    def check_t0(cls, value: Any) -> Any:
        if isinstance(value, np.datetime64):
            return value.astype("datetime64[ms]").astype(object).replace(tzinfo=timezone.utc)
        return value

    def __bool__(self) -> bool:
        return self.t0 is not None or self.member is not None or self.dispatch_info is not None

    def __hash__(self) -> int:
        return hash(
            f"{self.t0.isoformat() if self.t0 is not None else None}/{self.dispatch_info}/{self.member}"
        )


class EnsembleComponent(str, Enum):
    T0 = "t0"
    DISPATCH_INFO = "dispatch_info"
    MEMBER = "member"


class TimeSeriesMetadata(Model):
    path: str
    columns: List[TimeSeriesColumn] = Field(default_factory=lambda: [DEFAULT_VALUE_COLUMN])
    name: Optional[str] = None
    short_name: Optional[str] = None
    is_forecast: bool = False
    timezone: str = "UTC"

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True
        extra = Extra.allow

    @validator("columns")
    def check_columns(cls, v: List[TimeSeriesColumn]) -> List[TimeSeriesColumn]:
        """Ensure value column exists and its the first"""
        if v[0].key != "value":
            value_column = DEFAULT_VALUE_COLUMN
            non_value_columns = []
            for col in v:
                if col.key == "value":
                    value_column = col
                else:
                    non_value_columns.append(col)
            return [value_column] + non_value_columns
        else:
            return v


class TimeSeriesComment(Model):
    comment: str
    start: datetime
    end: datetime
    id: Optional[str] = None

    class Config:
        extra = Extra.allow


class CommentSupport(Flag):
    UNSUPPORTED = 0
    READ = auto()
    WRITE = auto()
    DELETE = auto()
