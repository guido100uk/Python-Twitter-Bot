"""Unique destination helper used by plan + execute."""

from __future__ import annotations

from pathlib import Path


def unique_destination(dest: Path, claimed: set[Path] | None = None) -> Path:
    """Return a path that does not exist on disk and is not in *claimed*."""
    claimed = claimed or set()
    if not dest.exists() and dest not in claimed:
        return dest
    stem, suffix, parent = dest.stem, dest.suffix, dest.parent
    # If stem already ends with " (n)", still append a fresh counter from 1
    # based on the original intended name pattern used by callers.
    n = 1
    while True:
        candidate = parent / f"{stem} ({n}){suffix}"
        if not candidate.exists() and candidate not in claimed:
            return candidate
        n += 1
