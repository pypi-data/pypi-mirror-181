from datetime import datetime


class TimeSeriesException(Exception):
    def __init__(self, message: str, path: str):
        super().__init__(message)
        self._path = path

    @property
    def path(self) -> str:
        return self._path


class TimeSeriesNotFoundError(TimeSeriesException):
    """Exception raised when accessing non existent time series."""

    def __init__(self, path: str):
        super().__init__(f"Time series not found with path {path}", path)


class TimeSeriesEnsembleMemberNotFoundError(TimeSeriesException):
    """Exception raised when accessing non existent ensemble members of a forecast time series."""

    def __init__(self, path: str, t0: datetime, member: str, dispatch_info: str):
        super().__init__(
            f"Time series ensemble member not found with path {path}, "
            f"t0={t0}, member{member} and dispatch_info={dispatch_info}",
            path,
        )
        self._t0 = t0
        self._member = member
        self._dispatch_info = dispatch_info

    @property
    def t0(self) -> datetime:
        return self._t0

    @property
    def member(self) -> str:
        return self._member

    @property
    def dispatch_info(self) -> str:
        return self._dispatch_info


class TimeSeriesUserError(TimeSeriesException):
    """This exception is raised when the user provides invalid data or arguments"""
