from __future__ import annotations

import filecmp
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console

from ._diff_strings import diff_strings


def have_same_content(a: Path, b: Path) -> bool:
    a = Path(a)
    b = Path(b)

    if not a.exists():
        raise ValueError(f"{a} does not exist")

    if not b.exists():
        raise ValueError(f"{b} does not exist")

    if a.is_file() and b.is_file():
        return filecmp.cmp(a, b, shallow=False)

    if a.is_dir() and b.is_dir():
        return _are_dirs_equal(a, b)

    return False


def _are_dirs_equal(dir1: str | Path, dir2: str | Path) -> bool:
    dir1 = Path(dir1)
    dir2 = Path(dir2)

    dirs_cmp = filecmp.dircmp(str(dir1), str(dir2))

    if (
        dirs_cmp.left_only
        or dirs_cmp.right_only
        or dirs_cmp.funny_files
        or dirs_cmp.diff_files
    ):
        return False

    for common_dir in dirs_cmp.common_dirs:
        if not _are_dirs_equal(dir1 / common_dir, dir2 / common_dir):
            return False

    return True


def diff_paths(
    a: str | Path,
    b: str | Path,
    *args,
    **kwargs,
):
    a = Path(a)
    b = Path(b)

    if not a.exists():
        raise ValueError(f"{a} does not exist")

    if not b.exists():
        raise ValueError(f"{b} does not exist")

    if a.is_file() and b.is_file():
        return [diff_files(a, b, *args, **kwargs)]

    if a.is_dir() and b.is_dir():
        return diff_dirs(a, b, *args, **kwargs)

    raise ValueError("Cannot diff file and path")


def diff_files(
    a: str | Path,
    b: str | Path,
    fmt: str = "unified",
    num_context_lines: int = 3,
):
    a = Path(a)
    b = Path(b)

    assert a.is_file()
    assert b.is_file()

    with open(a) as f:
        a_lines = f.readlines()
    with open(b) as f:
        b_lines = f.readlines()

    return diff_strings(
        a_lines,
        b_lines,
        fromfile=str(a),
        tofile=str(b),
        fromdate=_file_mtime(a),
        todate=_file_mtime(b),
        fmt=fmt,
        num_context_lines=num_context_lines,
    )


def diff_dirs(
    dir1: str | Path,
    dir2: str | Path,
    fmt: str = "unified",
    num_context_lines: int = 3,
):
    dir1 = Path(dir1)
    dir2 = Path(dir2)

    assert dir1.is_dir()
    assert dir2.is_dir()

    out = []

    dirs_cmp = filecmp.dircmp(str(dir1), str(dir2))

    for item in dirs_cmp.left_only:
        name = "File" if Path(item).is_file() else "Directory"
        out.append(ColorLine(f"--- {name} {item} is not present in {dir2}", "red"))

    for item in dirs_cmp.right_only:
        name = "File" if Path(item).is_file() else "Directory"
        out.append(ColorLine(f"+++ {name} {item} is not present in {dir1}", "green"))

    for item in dirs_cmp.common_funny:
        item1 = dir1 / item
        item2 = dir2 / item

        if item1.is_file() and item2.is_dir():
            message = f"{item1} is a file, {item2} is a directory"
        elif item1.is_directory() and item2.is_file():
            message = f"{item1} is a directory, {item2} is a file"
        else:
            message = f"{item1} and {item2} both exist, but something is funny"

        out.append(ColorLine(f"??? {message}", "cyan"))

    for item in dirs_cmp.funny_files:
        item1 = dir1 / item
        item2 = dir2 / item
        message = f"{item1} and {item2} are both files, but something is funny"
        out.append(ColorLine(f"??? {message}", "cyan"))

    out += [
        diff_files(dir1 / item, dir2 / item, fmt, num_context_lines)
        for item in dirs_cmp.diff_files
    ]

    for common_dir in dirs_cmp.common_dirs:
        out += diff_dirs(
            dir1 / common_dir,
            dir2 / common_dir,
            fmt,
            num_context_lines,
        )

    return out


def _file_mtime(path):
    ts = path.stat().st_mtime
    return datetime.fromtimestamp(ts, timezone.utc).astimezone().isoformat()


class ColorLine:
    def __init__(self, string: str, color: str):
        self.string = string
        self.color = color

    def __str__(self):
        return self.string

    def print(self, color: bool = True) -> None:
        if color:
            console = Console()
            console.print(self.string, style=self.color, highlight=False)
        else:
            print(self.string)
