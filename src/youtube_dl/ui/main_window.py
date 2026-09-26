import tkinter as tk
import threading
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

from youtube_dl.paths import FFMPEG_DIR, DENO_EXE
from youtube_dl.services.downloader import Downloader
from youtube_dl.services.file_manager import open_folder
from youtube_dl.settings import load_download_dir, save_download_dir


class MainWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("YouTube Downloader")
        self.root.geometry("600x300")

        self.output_dir = load_download_dir()
        self.output_dir_var = tk.StringVar(value=str(self.output_dir))

        self.downloader = Downloader(
            ffmpeg_dir=FFMPEG_DIR,
            deno_exe=DENO_EXE,
        )

        self.create_widgets()

    def create_widgets(self) -> None:
        ttk.Label(self.root, text="Download location:").pack(pady=(20, 5))

        output_frame = ttk.Frame(self.root)
        output_frame.pack(fill="x", padx=20)

        ttk.Entry(
            output_frame,
            textvariable=self.output_dir_var,
            state="readonly",
        ).pack(
            side="left",
            fill="x",
            expand=True,
        )

        ttk.Button(
            output_frame,
            text="Browse...",
            command=self.choose_output_dir,
        ).pack(side="left", padx=(10, 0))

        ttk.Button(
            self.root,
            text="Open videos folder",
            command=self.open_videos_folder,
        ).pack(pady=(10, 0))

        self.url_entry = ttk.Entry(self.root, width=70)
        self.url_entry.pack(pady=20)

        self.download_button = ttk.Button(
            self.root,
            text="Download",
            command=self.start_download,
        )
        self.download_button.pack()

        self.progress = ttk.Progressbar(
            self.root,
            length=400,
            mode="determinate",
        )
        self.progress.pack(pady=20)

        self.status_label = ttk.Label(
            self.root,
            text="Ready",
        )
        self.status_label.pack()

    def choose_output_dir(self) -> None:
        selected_dir = filedialog.askdirectory(
            initialdir=self.output_dir,
            title="Choose download folder",
        )

        if selected_dir:
            self.output_dir = Path(selected_dir)
            self.output_dir_var.set(str(self.output_dir))

            save_download_dir(self.output_dir)

    def open_videos_folder(self) -> None:
        open_folder(self.output_dir)

    def start_download(self) -> None:
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showwarning(
                "Missing URL",
                "Please enter a YouTube URL.",
            )
            return

        self.download_button.config(state="disabled")
        self.status_label.config(text="Downloading...")
        self.progress["value"] = 0

        thread = threading.Thread(
            target=self.download,
            args=(url,),
            daemon=True,
        )

        thread.start()

    def download(self, url: str) -> None:
        try:
            self.downloader.download(
                url,
                output_dir=self.output_dir,
                progress_callback=self.on_progress,
            )

            self.root.after(
                0,
                self.download_finished,
            )
        except Exception as error:
            self.root.after(
                0,
                lambda error=error: self.download_error(error),
            )

    def on_progress(self, data: dict) -> None:
        if data["status"] == "downloading":
            percent = data.get("_percent", 0)

            self.root.after(
                0,
                lambda: self.progress.config(value=percent),
            )

        elif data["status"] == "finished":
            self.root.after(
                0,
                lambda: self.status_label.config(text="Processing video..."),
            )

    def download_finished(self) -> None:
        self.progress["value"] = 100
        self.status_label.config(text="Download complete!")
        self.download_button.config(state="normal")

    def download_error(self, error: Exception) -> None:
        self.status_label.config(text="Download failed")

        self.download_button.config(state="normal")

        messagebox.showerror(
            "Download error",
            str(error),
        )

    def run(self) -> None:
        self.root.mainloop()
