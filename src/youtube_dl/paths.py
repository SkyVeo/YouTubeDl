from pathlib import Path
import sys


def get_app_dir() -> Path:
    # Check if the application is running in a frozen state (e.g., packaged with PyInstaller)
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    # If not frozen, return the parent directory of the script's location
    return Path(__file__).resolve().parents[2]


APP_DIR = get_app_dir()

RESOURCES_DIR = APP_DIR / "resources"

FFMPEG_DIR = RESOURCES_DIR / "ffmpeg" / "bin"
DENO_EXE = RESOURCES_DIR / "deno" / "deno.exe"

DEFAULT_VIDEOS_DIR = Path.home() / "Videos"
