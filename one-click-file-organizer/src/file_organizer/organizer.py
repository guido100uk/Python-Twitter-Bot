"""Core organize / preview / undo logic."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .categories import RESERVED_DIR_NAMES, SKIP_FILENAMES, category_for
from .paths import unique_destination

UNDO_LOG_NAME = "organizer_undo.json"


@dataclass(frozen=True)
class PlannedMove:
    source: Path
    destination: Path
    category: str


@dataclass
class OrganizeResult:
    planned: list[PlannedMove] = field(default_factory=list)
    moved: list[PlannedMove] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    dry_run: bool = True
    undo_log: Path | None = None


def iter_loose_files(target: Path, recursive: bool = False) -> Iterable[Path]:
    """Yield files sitting in the target folder (optionally nested)."""
    target = target.resolve()
    if recursive:
        for path in sorted(target.rglob("*")):
            if not path.is_file():
                continue
            if path.name in SKIP_FILENAMES or path.name == UNDO_LOG_NAME:
                continue
            try:
                rel = path.relative_to(target)
            except ValueError:
                continue
            if rel.parts and rel.parts[0] in RESERVED_DIR_NAMES:
                continue
            yield path
        return

    for path in sorted(target.iterdir()):
        if not path.is_file():
            continue
        if path.name in SKIP_FILENAMES or path.name == UNDO_LOG_NAME:
            continue
        yield path


def plan_moves(target: Path, recursive: bool = False) -> list[PlannedMove]:
    """Build the list of moves without applying them."""
    target = target.resolve()
    if not target.is_dir():
        raise NotADirectoryError(f"Not a directory: {target}")

    planned: list[PlannedMove] = []
    claimed: set[Path] = set()

    for src in iter_loose_files(target, recursive=recursive):
        category = category_for(src.suffix)
        dest_dir = target / category
        dest = unique_destination(dest_dir / src.name, claimed)
        claimed.add(dest)
        planned.append(PlannedMove(source=src, destination=dest, category=category))

    return planned


def organize(
    target: Path,
    *,
    dry_run: bool = True,
    recursive: bool = False,
) -> OrganizeResult:
    """Preview or execute organization of *target*."""
    target = target.resolve()
    planned = plan_moves(target, recursive=recursive)
    result = OrganizeResult(planned=planned, dry_run=dry_run)

    if dry_run or not planned:
        return result

    undo_entries: list[dict[str, str]] = []
    claimed: set[Path] = set()
    for move in planned:
        move.destination.parent.mkdir(parents=True, exist_ok=True)
        final_dest = unique_destination(move.destination, claimed)
        claimed.add(final_dest)
        shutil.move(str(move.source), str(final_dest))
        applied = PlannedMove(
            source=move.source, destination=final_dest, category=move.category
        )
        result.moved.append(applied)
        undo_entries.append(
            {
                "from": str(final_dest),
                "to": str(move.source),
                "category": move.category,
            }
        )

    undo_path = target / UNDO_LOG_NAME
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "target": str(target),
        "moves": undo_entries,
    }
    undo_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    result.undo_log = undo_path
    return result


def undo(target: Path) -> OrganizeResult:
    """Restore files from organizer_undo.json in *target*."""
    target = target.resolve()
    undo_path = target / UNDO_LOG_NAME
    result = OrganizeResult(dry_run=False, undo_log=undo_path)

    if not undo_path.is_file():
        result.skipped.append(f"No undo log found at {undo_path}")
        return result

    data = json.loads(undo_path.read_text(encoding="utf-8"))
    for entry in reversed(data.get("moves", [])):
        src = Path(entry["from"])
        dest = Path(entry["to"])
        if not src.is_file():
            result.skipped.append(f"Missing: {src}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        final_dest = unique_destination(dest)
        shutil.move(str(src), str(final_dest))
        result.moved.append(
            PlannedMove(
                source=src,
                destination=final_dest,
                category=entry.get("category", ""),
            )
        )

    for name in RESERVED_DIR_NAMES:
        folder = target / name
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()

    undo_path.unlink(missing_ok=True)
    result.undo_log = None
    return result


def summarize(result: OrganizeResult) -> str:
    """Human-readable summary for CLI / batch output."""
    lines: list[str] = []
    moves = result.planned if result.dry_run else result.moved
    if result.dry_run:
        lines.append(f"Preview: {len(result.planned)} file(s) would be organized")
    else:
        lines.append(f"Organized: {len(result.moved)} file(s) moved")

    by_cat: dict[str, int] = {}
    for m in moves:
        by_cat[m.category] = by_cat.get(m.category, 0) + 1
    for cat in sorted(by_cat):
        lines.append(f"  {cat}: {by_cat[cat]}")

    if result.dry_run and result.planned:
        lines.append("")
        lines.append("Planned moves:")
        for m in result.planned:
            lines.append(f"  {m.source.name} → {m.category}/{m.destination.name}")

    if result.undo_log:
        lines.append(f"Undo log: {result.undo_log}")
    for s in result.skipped:
        lines.append(f"Skipped: {s}")
    return "\n".join(lines)
