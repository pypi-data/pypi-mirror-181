from __future__ import annotations

import difflib
import sys

from rich.console import Console
from rich.syntax import Syntax


def diff_strings(
    fromlines: str | list[str],
    tolines: str | list[str],
    fmt: str = "unified",
    num_context_lines: int = 3,
    fromfile: str = "",
    tofile: str = "",
    fromdate: str = "",
    todate: str = "",
):
    assert isinstance(fromlines, str)
    assert isinstance(tolines, str)

    fmt = fmt.lower()
    assert fmt in [
        "c",
        "context",
        "m",
        "html",
        "n",
        "ndiff",
        "u",
        "unified",
    ]

    if isinstance(fromlines, str):
        fromlines = fromlines.split("\n")

    if isinstance(tolines, str):
        tolines = tolines.split("\n")

    if fmt in ["u", "unified"]:
        return UnifiedDiff(
            fromlines,
            tolines,
            fromfile,
            tofile,
            fromdate,
            todate,
            num_context_lines=num_context_lines,
        )

    elif fmt in ["n", "ndiff"]:
        return NDiff(fromlines, tolines)

    elif fmt in ["m", "html"]:
        return HtmlDiff(
            fromlines=fromlines,
            tolines=tolines,
            fromfile=fromfile,
            tofile=tofile,
            num_context_lines=num_context_lines,
        )

    return ContextDiff(
        fromlines=fromlines,
        tolines=tolines,
        fromfile=fromfile,
        tofile=tofile,
        fromdate=fromdate,
        todate=todate,
        num_context_lines=num_context_lines,
    )


class UnifiedDiff:
    def __init__(
        self,
        fromlines: str | list[str],
        tolines: str | list[str],
        fromfile: str = "",
        tofile: str = "",
        fromdate: str = "",
        todate: str = "",
        num_context_lines: int = 3,
    ):
        self.lines = list(
            difflib.unified_diff(
                fromlines,
                tolines,
                fromfile,
                tofile,
                fromdate,
                todate,
                n=num_context_lines,
                lineterm="",
            )
        )

    def __str__(self) -> str:
        return "\n".join(self.lines)

    def print(self, color: bool = True) -> None:
        if color:
            console = Console()
            for k, line in enumerate(self.lines):
                style = None
                if line[:3] in ["---", "+++"]:
                    style = "yellow"

                elif line[:2] == "@@":
                    style = "cyan"

                elif line[0] == "-":
                    style = "red"

                elif line[0] == "+":
                    style = "green"

                if line[-1] == "\n":
                    line = line[:-1]

                console.print(line, style=style, highlight=False)

        else:
            sys.stdout.writelines(self.lines)


class NDiff:
    def __init__(
        self,
        fromlines: str | list[str],
        tolines: str | list[str],
    ):
        self.lines = list(
            difflib.ndiff(
                fromlines,
                tolines,
            )
        )

    def __str__(self) -> str:
        return "\n".join(self.lines)

    def print(self, color: bool = True) -> None:
        if color:
            console = Console()
            for k, line in enumerate(self.lines):
                style = None
                if line[:2] == "- ":
                    style = "red"

                elif line[:2] == "+ ":
                    style = "green"

                elif line[:2] == "? ":
                    style = "blue"

                if line[-1] == "\n":
                    line = line[:-1]

                console.print(line, style=style, highlight=False)

        else:
            sys.stdout.writelines(self.lines)


class HtmlDiff:
    def __init__(
        self,
        fromlines: str | list[str],
        tolines: str | list[str],
        num_context_lines: int = 3,
        fromfile: str = "",
        tofile: str = "",
        fromdate: str = "",
        todate: str = "",
    ):
        self.lines = list(
            difflib.HtmlDiff().make_file(
                fromlines,
                tolines,
                fromfile,
                tofile,
                context=True,
                numlines=num_context_lines,
            )
        )

    def __str__(self) -> str:
        return "\n".join(self.lines)

    def print(self, color: bool = True) -> None:
        if color:
            console = Console()
            syntax = Syntax("".join(self.lines), "html")
            console.print(syntax)

        else:
            sys.stdout.writelines(self.lines)


class ContextDiff:
    def __init__(
        self,
        fromlines: str | list[str],
        tolines: str | list[str],
        num_context_lines: int = 3,
        fromfile: str = "",
        tofile: str = "",
        fromdate: str = "",
        todate: str = "",
    ):
        self.lines = list(
            difflib.context_diff(
                fromlines,
                tolines,
                fromfile,
                tofile,
                fromdate,
                todate,
                n=num_context_lines,
                lineterm="",
            )
        )

    def __str__(self) -> str:
        return "\n".join(self.lines)

    def print(self, color: bool = True) -> None:
        if color:
            console = Console()
            for k, line in enumerate(self.lines):
                style = None
                if k < 2:
                    style = "yellow"

                elif line[:2] == "! ":
                    style = "yellow"

                elif line[:3] in ["---", "***"]:
                    style = "cyan"

                if line[-1] == "\n":
                    line = line[:-1]

                console.print(line, style=style, highlight=False)
        else:
            sys.stdout.writelines(self.lines)


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
