"""Command-line entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .organizer import organize, summarize, undo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="file-organizer",
        description=(
            "One-click file organizer: sort a messy folder into "
            "Images, Documents, Videos, and more."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Folder to organize (default: current directory)",
    )
    parser.add_argument(
        "--organize",
        action="store_true",
        help="Apply moves (default is preview / dry-run only)",
    )
    parser.add_argument(
        "--undo",
        action="store_true",
        help="Undo the last organize run in this folder",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Include files in subfolders (skips category folders)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    target = Path(args.path).expanduser()

    try:
        if args.undo:
            result = undo(target)
        else:
            result = organize(
                target,
                dry_run=not args.organize,
                recursive=args.recursive,
            )
    except (NotADirectoryError, FileNotFoundError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(summarize(result))
    if args.undo and result.skipped and not result.moved:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
