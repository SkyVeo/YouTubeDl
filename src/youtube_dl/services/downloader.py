import yt_dlp
from pathlib import Path


class Downloader:
    def __init__(self, ffmpeg_dir: Path, deno_exe: Path) -> None:
        self.ffmpeg_dir = ffmpeg_dir
        self.deno_exe = deno_exe

    def options(self, output_dir: Path, progress_callback: callable = None) -> dict:
        options = {
            "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
            "merge_output_format": "mp4",
            "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
            "ffmpeg_location": str(self.ffmpeg_dir),
            "js_runtimes": {
                "deno": {
                    "path": str(self.deno_exe),
                },
            },
        }

        if progress_callback:
            options["progress_hooks"] = [progress_callback]

        return options

    def download(
        self, url: str, output_dir: Path, progress_callback: callable = None
    ) -> None:
        with yt_dlp.YoutubeDL(self.options(output_dir, progress_callback)) as ydl:
            ydl.download([url])

    def get_video_info(self, url: str) -> dict:
        with yt_dlp.YoutubeDL() as ydl:
            return ydl.extract_info(url, download=False)
