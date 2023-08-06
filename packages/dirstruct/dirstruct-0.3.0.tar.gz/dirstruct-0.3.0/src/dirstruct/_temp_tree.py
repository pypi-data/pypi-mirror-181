from __future__ import annotations

import tempfile
from pathlib import Path


class TemporaryTree:
    def __init__(self, tree: dict):
        self._tmp = None
        assert isinstance(tree, dict)
        self._tree = tree

    def __enter__(self) -> Path:
        self._tmp = tempfile.TemporaryDirectory()
        path = Path(self._tmp.name)
        write(self._tree, path)
        return path

    def __exit__(self, *_):
        self._tmp.cleanup()


def write(
    dirstruct: dict[str, str | bytes | dict],
    parent: Path,
) -> None:
    for name, value in dirstruct.items():
        if isinstance(value, str):
            with open(parent / name, "w") as f:
                f.write(value)

        elif isinstance(value, bytes):
            with open(parent / name, "wb") as f:
                f.write(value)

        elif isinstance(value, dict):
            (parent / name).mkdir()
            write(value, parent=parent / name)

        else:
            raise ValueError(f"Don't know how to deal with {value}")
