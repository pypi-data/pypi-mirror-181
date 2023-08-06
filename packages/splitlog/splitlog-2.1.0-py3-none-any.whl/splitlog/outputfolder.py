import abc
import contextlib
import os
import stat
import types
import typing as t
from pathlib import Path


class BinWriter(contextlib.AbstractContextManager, metaclass=abc.ABCMeta):
    """Abstract base class for writing binary data into an output file."""

    @abc.abstractmethod
    def write(self, b: bytes) -> int:
        """Writes bytes into a file and returns how many bytes were written successfully.

        :returns: number of bytes written successfully
        """
        raise NotImplementedError()


class OutputFolder(contextlib.AbstractContextManager, metaclass=abc.ABCMeta):
    """Abstract base class for output folder IO."""

    @property
    @abc.abstractmethod
    def root(self) -> Path:
        """Root path of the output folder to construct paths inside the output folder.

        :returns: root path
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def mkdir(self, path: Path) -> None:
        """Creates a subdirectory."""
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, path: Path) -> BinWriter:
        """Creates a new file and returns a writer to write to it.

        :returns: writer to write binary data into the file
        """
        raise NotImplementedError()


class FileWrapper(BinWriter):
    def __init__(self, file: t.BinaryIO):
        self._file = file

    def write(self, b: bytes) -> int:
        return self._file.write(b)

    def __enter__(self) -> "FileWrapper":
        return self

    def __exit__(
        self,
        exc: t.Union[t.Type[BaseException], None],
        value: t.Union[BaseException, None],
        tb: t.Union[types.TracebackType, None],
    ) -> t.Union[bool, None]:
        return self._file.__exit__(exc, value, tb)


class LocalFilesystemOutputFolder(OutputFolder):
    """Encapsulates filesystem IO on output folders"""

    DIR_MODE = (
        stat.S_IRUSR
        | stat.S_IWUSR
        | stat.S_IXUSR
        | stat.S_IRGRP
        | stat.S_IXGRP
        | stat.S_IROTH
        | stat.S_IXOTH
    )
    FILE_MODE = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH

    def __init__(self: "LocalFilesystemOutputFolder", path: Path):
        self._path: Path = path
        self._dir_fd: t.Union[int, None] = None

    def __enter__(self: "LocalFilesystemOutputFolder") -> "LocalFilesystemOutputFolder":
        if self._path.exists():
            raise FileExistsError(f"Output folder {self._path} already exists.")

        parent = self._path.parent
        name = self._path.name
        parent_dir_fd = os.open(
            parent, os.O_PATH | os.O_NOFOLLOW | os.O_DIRECTORY | os.O_CLOEXEC
        )
        try:
            os.mkdir(name, mode=self.DIR_MODE, dir_fd=parent_dir_fd)
            self._dir_fd = os.open(
                name,
                os.O_PATH | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=parent_dir_fd,
            )
            return self
        finally:
            os.close(parent_dir_fd)

    def __exit__(
        self: "LocalFilesystemOutputFolder",
        exc: t.Union[t.Type[BaseException], None],
        value: t.Union[BaseException, None],
        tb: t.Union[types.TracebackType, None],
    ) -> t.Union[bool, None]:
        if self._dir_fd is not None:
            saved, self._dir_fd = self._dir_fd, None
            os.close(saved)
        return None

    @property
    def root(self: "LocalFilesystemOutputFolder") -> Path:
        return Path()

    def mkdir(self: "LocalFilesystemOutputFolder", path: Path) -> None:
        assert not path.is_absolute(), f"Path {path} must be relative"
        os.mkdir(path, mode=self.DIR_MODE, dir_fd=self._dir_fd)

    def _opener(self: "LocalFilesystemOutputFolder", path: str, flags: int) -> int:
        return os.open(
            path, flags | os.O_NOFOLLOW, mode=self.FILE_MODE, dir_fd=self._dir_fd
        )

    def create(self: "LocalFilesystemOutputFolder", path: Path) -> BinWriter:
        assert not path.is_absolute(), f"Path {path} must be relative"
        return FileWrapper(open(path, "xb", opener=self._opener))
