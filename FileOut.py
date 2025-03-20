import io
import sys

from enum import Enum, StrEnum
from types import TracebackType
from typing import Union, Optional, Self


class FileOutModes(StrEnum):
    APPEND = "a"
    REWRITE = "w"


class FileOut:
    _mode: Union[str, FileOutModes]
    _prev_stdout: Optional[io.TextIOWrapper]
    _opened_file: Optional[io.TextIOWrapper]
    path_to_file: str

    def __init__(
            self,
            path_to_file: str,
            mode: Union[str, FileOutModes] = FileOutModes.REWRITE,
    ) -> None:
        mode = FileOutModes(mode)

        self._mode = mode
        self.path_to_file = path_to_file
        self._opened_file = None
        self._prev_stdout = None

    @property
    def mode(self) -> FileOutModes:
        return FileOutModes(self._mode)

    @mode.setter
    def mode(self, mode_new: Union[str, FileOutModes]) -> None:
        self._mode = FileOutModes(mode_new)

    def __enter__(self):
        self._prev_stdout = sys.stdout
        self._opened_file = open(self.path_to_file, self._mode)
        sys.stdout = self._opened_file

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._opened_file.close()
        self._opened_file = None
        sys.stdout = self._prev_stdout
        self._prev_stdout = None
