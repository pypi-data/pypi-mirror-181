from __future__ import annotations

import filecmp
import os
import stat
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console

from ._strings import diff_strings

_UNIX_EPOCH = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)


def read(path: Path | str) -> Node:
    path = Path(path)

    try:
        # Python 3.10+
        stat = path.stat(follow_symlinks=False)
    except TypeError:
        # Python 3.9 and before
        stat = path.stat()

    mode = stat.st_mode
    ctime = datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc)
    mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)

    if path.is_dir():
        try:
            children = [read(node) for node in path.iterdir()]
        except PermissionError:
            children = []

        return Directory(
            name=path.name,
            children=children,
            mode=mode,
            ctime=ctime,
            mtime=mtime,
        )

    elif path.is_file():
        return File(
            name=path.name,
            content=path,
            mode=mode,
            ctime=ctime,
            mtime=mtime,
        )

    elif path.is_symlink():
        return SymLink(
            name=path.name,
            target=path.readlink(),
            mode=mode,
            ctime=ctime,
            mtime=mtime,
        )

    # Default behavior for is_socket(), is_fifo() etc.
    return Node(
        name=path.name,
        mode=mode,
        ctime=ctime,
        mtime=mtime,
    )


def diff(
    a: Node,
    b: Node,
    fmt: str = "unified",
    num_context_lines: int = 3,
) -> str:
    if isinstance(a, File) and isinstance(b, File):
        return diff_strings(
            a.content.decode(),
            b.content.decode(),
            fromfile=a.name,
            tofile=b.name,
            fromdate=a.mtime.isoformat(),
            todate=b.mtime.isoformat(),
            fmt=fmt,
            num_context_lines=num_context_lines,
        )
    else:
        exit(1)
    return


class Node:
    def __init__(
        self,
        name: str,
        mode: int,
        ctime: datetime | None = None,
        mtime: datetime | None = None,
    ):
        assert _is_legal_name(name)

        assert isinstance(mode, int)

        if ctime is None:
            ctime = _UNIX_EPOCH
        if mtime is None:
            mtime = _UNIX_EPOCH
        assert isinstance(ctime, datetime)
        assert isinstance(mtime, datetime)

        self.name = name
        self.mode = mode
        self.ctime = ctime
        self.mtime = mtime

    def __str__(self) -> str:
        return self.get_string(with_icons=True)

    def get_string(self, with_icons: bool = False) -> str:
        if with_icons:
            return f" {self.name}"
        return self.name

    def populate(self) -> None:
        pass


def _indent(string: str, indent: int = 4) -> str:
    c = " " * indent
    return c + ("\n" + c).join(string.split("\n"))


class Directory(Node):
    def __init__(
        self,
        name: str,
        children: list[Directory | File] | None = None,
        mode: int | None = 0o40775,
        ctime: datetime | None = None,
        mtime: datetime | None = None,
    ):
        if children is None:
            children = []

        if len(set(c.name for c in children)) != len(children):
            raise ValueError("Input list must have unique names")

        # Force alphabetic order. This simplifies __eq__ comparison.
        self.children = sorted(children, key=lambda d: d.name)

        super().__init__(name, mode, ctime, mtime)

    def __str__(self) -> str:
        return self.get_string(with_icons=True)

    def get_string(self, with_icons: bool = False) -> str:
        if with_icons:
            if self.name == "node_modules":
                icon = ""
            elif self.name == "Music":
                icon = ""
            elif self.name == "Videos":
                icon = ""
            elif self.name == "Downloads":
                icon = ""
            elif self.name == "Documents":
                icon = ""
            elif self.name == "Desktop":
                icon = ""
            else:
                icon = ""
            return "\n".join(
                [f"[blue]{icon} [b]{self.name}[/b][/blue]"]
                + [_indent(str(child)) for child in self.children]
            )

        return "\n".join(
            [f"[blue][b]{self.name}[/b][/blue]"]
            + [_indent(str(child)) for child in self.children]
        )

    def show(self) -> None:
        Console().print(str(self), highlight=False)

    def populate(self) -> None:
        for c in self.children:
            c.populate()

    def write(self, path: Path | str, exist_ok: bool = False) -> None:
        path = Path(path) / self.name

        path.mkdir(mode=self.mode, exist_ok=exist_ok, parents=True)

        for c in self.children:
            c.write(path, exist_ok=exist_ok)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Directory):
            return False

        # ignore ctime, mtime, and mode for __eq__ comparison
        return self.name == other.name and self.children == other.children


class File(Node):
    def __init__(
        self,
        name: str,
        content: str | bytes | Path,
        mode: int | None = 0o100664,
        ctime: datetime | None = None,
        mtime: datetime | None = None,
    ):
        if isinstance(content, Path):
            assert content.exists()
            self._path = content
            self._content = None

        elif isinstance(content, str):
            self._path = None
            self._content = content.encode()

        else:
            assert isinstance(content, bytes)
            self._path = None
            self._content = content

        super().__init__(name, mode, ctime, mtime)

    def populate(self) -> None:
        if self._content is None:
            assert self._path is not None
            try:
                with open(self._path, "rb") as f:
                    self._content = f.read()
            except UnicodeDecodeError:
                print(f"Read error in file {self._path}")
                raise

    @property
    def content(self):
        """
        Lazy reading of file contents.
        """
        self.populate()
        return self._content

    def __eq__(self, other) -> bool:
        if not isinstance(other, File):
            return False

        if self._path is not None and other._path is not None:
            return filecmp.cmp(self._path, other._path, shallow=False)

        # ignore ctime, mtime, and mode (except the executable bit) for __eq__
        # comparison
        return (
            self.name == other.name
            and self.content == other.content
            and (self.mode & stat.S_IXUSR) == (other.mode & stat.S_IXUSR)
        )

    def __str__(self) -> str:
        return self.get_string(with_icons=True)

    def get_string(self, with_icons: bool = False) -> str:
        suffix = Path(self.name).suffix

        color = None
        if with_icons:
            if self.name in ["LICENSE", "LICENSE.txt"]:
                icon = ""
            elif self.name in ["package.json", "package-lock.json"]:
                icon = ""
            elif self.name in ["Makefile"]:
                icon = ""
            elif self.name in ["Dockerfile", "docker-compose.yml"]:
                icon = ""
            elif suffix in [".py", ".pyc"]:
                icon = ""
            elif suffix == ".log":
                icon = ""
            elif suffix in [".cpp", ".cxx"]:
                icon = ""
            elif suffix == ".c":
                icon = ""
            elif suffix == ".h":
                icon = ""
            elif suffix == ".js":
                icon = ""
            elif suffix == ".ts":
                icon = ""
            elif suffix == ".tex":
                icon = ""
            elif suffix in [".o", ".ld"]:
                icon = ""
            elif suffix in [".out", ".sh", ".bak", ".backup"]:
                icon = ""
            elif suffix == ".txt":
                icon = ""
            elif suffix == ".pdf":
                icon = ""
            elif suffix in [".json", ".yml", ".yaml", ".toml"]:
                icon = ""
            elif suffix == ".lua":
                icon = ""
            elif suffix == ".xml":
                icon = ""
            elif suffix == ".bat":
                icon = ""
            elif suffix in [".ttf", ".otf", ".woff", ".woff2"]:
                icon = ""
            elif suffix in [".tar", ".zip", ".7z"]:
                icon = ""
                color = "red"
            elif suffix in [".asc", ".lock"]:
                icon = ""
            elif suffix in [".jpg", ".png", ".svg", ".gif"]:
                icon = ""
                color = "magenta"
            elif suffix in [".jpg", ".png", ".svg", ".gif", ".ico"]:
                icon = ""
            elif suffix in [".wav", ".mp3"]:
                icon = ""
            elif suffix == ".md":
                icon = ""
            elif suffix in [".ini", ".cfg"]:
                icon = ""
            elif suffix == ".xlsx":
                icon = ""
            elif suffix == ".docx":
                icon = ""
            elif suffix == ".pptx":
                icon = ""
            elif suffix == ".nix":
                icon = ""
            elif suffix == ".deb":
                icon = ""
            elif suffix == ".rb":
                icon = ""
            elif suffix == ".html":
                icon = ""
            elif suffix in [".mkv", ".avi", ".mp4", ".flv", ".webm"]:
                icon = ""
            else:
                icon = ""

            if self.mode & stat.S_IXUSR:
                color = "green"

            if color is None:
                return f"{icon} {self.name}"
            else:
                return f"[{color}]{icon} [b]{self.name}[/b][/{color}]"

        return self.name

    def write(self, path: Path | str, exist_ok: bool = False) -> None:
        path = Path(path) / self.name

        if not exist_ok and path.exists():
            raise ValueError(f"Path {path} already exists")

        with open(path, "wb") as f:
            f.write(self.content)

        os.chmod(path, self.mode)


class SymLink(Node):
    def __init__(
        self,
        name: str,
        target: Path | str,
        mode: int | None = 0o100664,
        ctime: datetime | None = None,
        mtime: datetime | None = None,
    ):
        self.target = Path(target)
        super().__init__(name, mode, ctime, mtime)

    def __str__(self) -> str:
        color = "teal" if self.target.exists() else "red"
        return (
            f"[{color}] [b]{self.name}[/b][/{color}]"
            + " ⇒ "
            + f"[{color}][b]{self.target}[/b][/{color}]"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, SymLink):
            return False
        # ignore ctime and mtime for __eq__ comparison
        return self.name == other.name and self.content == other.content

    def write(self, path: Path | str, exist_ok: bool = False) -> None:
        if not exist_ok and path.exists():
            raise ValueError(f"Path {path} already exists")

        path = Path(path) / self.name

        path.symlink_to(self.target)


def _is_legal_name(string: str) -> bool:
    if not isinstance(string, str) or len(string) == 0:
        return False

    if os.name == "posix":
        if "/" in string:
            return False

    else:
        # windows
        for char in r'<>:"/\|?*':
            if char in string:
                return False

    return True
