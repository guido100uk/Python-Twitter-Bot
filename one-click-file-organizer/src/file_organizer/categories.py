"""Extension → category mapping for one-click organization."""

from __future__ import annotations

# Folder names used on disk (Windows-friendly, no special chars).
CATEGORIES: dict[str, set[str]] = {
    "Images": {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp",
        ".tif",
        ".tiff",
        ".ico",
        ".svg",
        ".heic",
        ".raw",
        ".cr2",
        ".nef",
    },
    "Documents": {
        ".pdf",
        ".doc",
        ".docx",
        ".txt",
        ".rtf",
        ".odt",
        ".md",
        ".epub",
        ".pages",
    },
    "Spreadsheets": {
        ".xls",
        ".xlsx",
        ".csv",
        ".ods",
        ".tsv",
    },
    "Presentations": {
        ".ppt",
        ".pptx",
        ".odp",
        ".key",
        ".pps",
        ".ppsx",
    },
    "Videos": {
        ".mp4",
        ".mkv",
        ".avi",
        ".mov",
        ".wmv",
        ".flv",
        ".webm",
        ".m4v",
        ".mpeg",
        ".mpg",
    },
    "Audio": {
        ".mp3",
        ".wav",
        ".flac",
        ".aac",
        ".ogg",
        ".wma",
        ".m4a",
        ".aiff",
    },
    "Archives": {
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz",
        ".bz2",
        ".xz",
        ".iso",
    },
    "Code": {
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".cs",
        ".go",
        ".rs",
        ".rb",
        ".php",
        ".html",
        ".css",
        ".scss",
        ".json",
        ".xml",
        ".yml",
        ".yaml",
        ".sql",
        ".sh",
        ".bat",
        ".ps1",
        ".swift",
        ".kt",
    },
    "Executables": {
        ".exe",
        ".msi",
        ".app",
        ".dmg",
        ".apk",
        ".deb",
        ".rpm",
        ".cmd",
    },
    "Fonts": {
        ".ttf",
        ".otf",
        ".woff",
        ".woff2",
        ".eot",
    },
}

OTHERS = "Others"

# Reserved names we never treat as loose files to move into themselves.
RESERVED_DIR_NAMES = frozenset(CATEGORIES) | {OTHERS}

# Files this tool writes / Windows launcher — leave in place.
SKIP_FILENAMES = frozenset(
    {
        "organizer_undo.json",
        "Organize.bat",
        "organize.bat",
    }
)


def category_for(extension: str) -> str:
    """Return category folder name for a file extension (with or without dot)."""
    ext = extension.lower()
    if ext and not ext.startswith("."):
        ext = f".{ext}"
    for name, exts in CATEGORIES.items():
        if ext in exts:
            return name
    return OTHERS
