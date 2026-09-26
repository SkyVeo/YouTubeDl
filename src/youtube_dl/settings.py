import json
from pathlib import Path

from youtube_dl.paths import DEFAULT_VIDEOS_DIR

APP_DATA_DIR = Path.home() / "AppData" / "Local" / "YouTubeDl"
SETTINGS_FILE = APP_DATA_DIR / "settings.json"


def load_download_dir() -> Path:
    if not SETTINGS_FILE.exists():
        return DEFAULT_VIDEOS_DIR

    try:
        with SETTINGS_FILE.open("r", encoding="utf-8") as file:
            settings = json.load(file)

        path = Path(settings["download_dir"])

        if path.exists() and path.is_dir():
            return path
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        pass

    return DEFAULT_VIDEOS_DIR


def save_download_dir(path: Path) -> None:
    APP_DATA_DIR.mkdir(parents=True, exist_ok=True)

    settings = {
        "download_dir": str(path),
    }

    with SETTINGS_FILE.open("w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)
