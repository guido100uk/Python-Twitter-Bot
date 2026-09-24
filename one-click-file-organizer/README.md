# One-Click File Organizer

Messy folder? Organize your files automatically with a simple one-click Windows file organizer.

Inspired by short-form “PC Tweaks Lab” style demos: point at a cluttered Downloads (or any) folder and sort files into clear category folders in one confirmation.

## What it does

| Before | After |
| --- | --- |
| Loose mix of photos, PDFs, videos, zips… | `Images/`, `Documents/`, `Videos/`, `Audio/`, `Archives/`, `Code/`, `Spreadsheets/`, `Presentations/`, `Executables/`, `Fonts/`, `Others/` |

- **Preview first** — see exactly what will move
- **One confirmation** — then organize
- **Safe duplicates** — never overwrites (`photo (1).jpg`)
- **Undo** — restore from `organizer_undo.json`

## Windows (one-click)

1. Install [Python 3](https://www.python.org/downloads/) and check **Add python.exe to PATH**.
2. Copy this folder anywhere (or clone the repo and open `one-click-file-organizer/`).
3. Double-click **`Organize.bat`**, *or* drag a messy folder onto `Organize.bat`.
4. Review the preview → press **Y** to organize.

Undo later (Command Prompt in that folder):

```bat
set PYTHONPATH=path\to\one-click-file-organizer\src
python -m file_organizer "C:\path\to\messy\folder" --undo
```

## Any OS (CLI)

```bash
cd one-click-file-organizer
export PYTHONPATH=src   # Windows CMD: set PYTHONPATH=src

# Preview (default)
python -m file_organizer /path/to/messy/folder

# Organize
python -m file_organizer /path/to/messy/folder --organize

# Undo last run
python -m file_organizer /path/to/messy/folder --undo

# Include nested files (still skips category folders)
python -m file_organizer /path/to/messy/folder --organize --recursive
```

Optional install:

```bash
pip install -e ".[dev]"
file-organizer ~/Downloads --organize
```

## Verify

```bash
cd one-click-file-organizer
pip install -e ".[dev]"
pytest -q
```

## Layout

```text
one-click-file-organizer/
  Organize.bat              # Windows one-click launcher
  pyproject.toml
  README.md
  src/file_organizer/       # Python package (stdlib only)
  scripts/Organize.bat      # Same launcher (copy)
  tests/
```

This product is standalone. It does not depend on the Twitter bot scripts in the parent repository.
