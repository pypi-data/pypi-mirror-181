from __future__ import annotations

import os
from pathlib import Path

from rich.console import Console

console = Console(highlight=False)


_directory_icons = {
    "node_modules": "",
    "Music": "",
    "Videos": "",
    "Downloads": "",
    "Documents": "",
    "Desktop": "",
}

_filename_icons = {
    "LICENSE": "",
    "LICENSE.txt": "",
    "package.json": "",
    "package-lock.json": "",
    "Makefile": "",
    "Dockerfile": "",
    "docker-compose.yml": "",
}

_file_suffix_icons = {
    ".py": "",
    ".pyc": "",
    ".log": "",
    ".cpp": "",
    ".cxx": "",
    ".c": "",
    ".h": "",
    ".js": "",
    ".ts": "",
    ".tex": "",
    ".o": "",
    ".ls": "",
    ".out": "",
    ".sh": "",
    ".bak": "",
    ".backup": "",
    ".txt": "",
    ".pdf": "",
    ".json": "",
    ".yml": "",
    ".yaml": "",
    ".toml": "",
    ".lua": "",
    ".xml": "",
    ".bat": "",
    ".ttf": "",
    ".otf": "",
    ".woff": "",
    ".woff2": "",
    ".tar": "",
    ".zip": "",
    ".7z": "",
    ".asc": "",
    ".lock": "",
    ".jpg": "",
    ".jpeg": "",
    ".png": "",
    ".svg": "",
    ".gif": "",
    ".wav": "",
    ".mp3": "",
    ".md": "",
    ".ini": "",
    ".cfg": "",
    ".xlsx": "",
    ".docx": "",
    ".pptx": "",
    ".nix": "",
    ".deb": "",
    ".rb": "",
    ".html": "",
    ".mkv": "",
    ".avi": "",
    ".mp4": "",
    ".flv": "",
    ".webm": "",
}

_file_suffix_colors = {
    ".tar": "red",
    ".zip": "red",
    ".7z": "red",
    #
    ".jpg": "magenta",
    ".png": "magenta",
    ".svg": "magenta",
    ".gif": "magenta",
}


def show_tree(
    path: Path | str,
    with_icons: bool = True,
    indent: int = 0,
) -> None:
    path = Path(path)

    if path.is_dir():
        icon = ""
        if with_icons:
            try:
                icon = _directory_icons[path.name] + " "
            except KeyError:
                icon = " "

        console.print(" " * indent + f"[blue][b]{icon}{path.name}[/b][/blue]")

        for file in path.iterdir():
            show_tree(file, with_icons, indent + 4)

    elif path.is_file():
        icon = ""
        color = None
        if with_icons:
            if path.name in _filename_icons:
                icon = _filename_icons[path.name]
            elif path.suffix in _file_suffix_icons:
                icon = _file_suffix_icons[path.suffix]
            else:
                icon = ""

            # executable?
            if os.access(path, os.X_OK):
                color = "green"

            elif path.suffix in _file_suffix_colors:
                color = _file_suffix_colors[path.suffix]

        out = path.name
        if icon:
            out = f"{icon} {out}"

        if color:
            out = f"[{color}][b]{out}[/b][/{color}]"

        console.print(" " * indent + out)

    elif path.is_symlink():
        target = path.readlink()
        color = "teal" if target.exists() else "red"
        console.print(
            " " * indent
            + f"[{color}] [b]{path.name}[/b][/{color}]"
            + " ⇒ "
            + f"[{color}][b]{target}[/b][/{color}]",
        )
    else:
        console.print(f"Don't know how to print {path}")
