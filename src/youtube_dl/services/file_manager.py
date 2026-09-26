import os
from pathlib import Path


def open_folder(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    os.startfile(folder)
