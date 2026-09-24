from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from file_organizer.categories import category_for  # noqa: E402
from file_organizer.cli import main  # noqa: E402
from file_organizer.organizer import organize, undo  # noqa: E402


def test_category_for_images_and_unknown():
    assert category_for(".PNG") == "Images"
    assert category_for("pdf") == "Documents"
    assert category_for(".xyz") == "Others"
    assert category_for("") == "Others"


def test_preview_does_not_move(tmp_path: Path):
    (tmp_path / "photo.jpg").write_bytes(b"img")
    (tmp_path / "notes.pdf").write_bytes(b"pdf")
    (tmp_path / "song.mp3").write_bytes(b"audio")

    result = organize(tmp_path, dry_run=True)
    assert result.dry_run is True
    assert len(result.planned) == 3
    assert (tmp_path / "photo.jpg").is_file()
    assert not (tmp_path / "Images").exists()


def test_organize_and_undo(tmp_path: Path):
    (tmp_path / "photo.jpg").write_bytes(b"img")
    (tmp_path / "notes.pdf").write_bytes(b"pdf")
    (tmp_path / "readme.xyz").write_bytes(b"misc")

    result = organize(tmp_path, dry_run=False)
    assert len(result.moved) == 3
    assert (tmp_path / "Images" / "photo.jpg").is_file()
    assert (tmp_path / "Documents" / "notes.pdf").is_file()
    assert (tmp_path / "Others" / "readme.xyz").is_file()
    assert not (tmp_path / "photo.jpg").exists()
    assert (tmp_path / "organizer_undo.json").is_file()

    undone = undo(tmp_path)
    assert len(undone.moved) == 3
    assert (tmp_path / "photo.jpg").is_file()
    assert (tmp_path / "notes.pdf").is_file()
    assert (tmp_path / "readme.xyz").is_file()
    assert not (tmp_path / "organizer_undo.json").exists()
    # Empty category folders removed
    assert not (tmp_path / "Images").exists()


def test_duplicate_names_renamed(tmp_path: Path):
    images = tmp_path / "Images"
    images.mkdir()
    (images / "photo.jpg").write_bytes(b"old")
    (tmp_path / "photo.jpg").write_bytes(b"new")

    result = organize(tmp_path, dry_run=False)
    assert len(result.moved) == 1
    assert (images / "photo.jpg").read_bytes() == b"old"
    assert (images / "photo (1).jpg").read_bytes() == b"new"


def test_skips_organize_bat_and_undo_log(tmp_path: Path):
    (tmp_path / "Organize.bat").write_text("@echo off\n", encoding="utf-8")
    (tmp_path / "organizer_undo.json").write_text("{}", encoding="utf-8")
    (tmp_path / "a.txt").write_text("hi", encoding="utf-8")

    result = organize(tmp_path, dry_run=True)
    names = {m.source.name for m in result.planned}
    assert names == {"a.txt"}


def test_cli_preview_and_organize(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    (tmp_path / "clip.mp4").write_bytes(b"vid")
    assert main([str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "Preview: 1" in out
    assert (tmp_path / "clip.mp4").is_file()

    assert main([str(tmp_path), "--organize"]) == 0
    assert (tmp_path / "Videos" / "clip.mp4").is_file()
    undo_data = json.loads((tmp_path / "organizer_undo.json").read_text(encoding="utf-8"))
    assert len(undo_data["moves"]) == 1
