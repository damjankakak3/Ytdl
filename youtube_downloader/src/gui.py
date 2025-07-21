import tkinter as tk
from tkinter import filedialog
from downloader import download_video

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")

        self.url_label = tk.Label(root, text="YouTube URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        self.output_label = tk.Label(root, text="Output Directory:")
        self.output_label.pack()

        self.output_path = tk.StringVar()
        self.output_path.set(".")
        self.output_entry = tk.Entry(root, textvariable=self.output_path, width=50)
        self.output_entry.pack()

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_directory)
        self.browse_button.pack()

        self.format_label = tk.Label(root, text="Format:")
        self.format_label.pack()

        self.format_var = tk.StringVar(root)
        self.format_var.set("best")
        self.format_menu = tk.OptionMenu(root, self.format_var, "best (video)", "mp4", "webm", "best (audio)", "mp3", "m4a")
        self.format_menu.pack()

        self.subtitles_var = tk.BooleanVar()
        self.subtitles_check = tk.Checkbutton(root, text="Download subtitles", variable=self.subtitles_var)
        self.subtitles_check.pack()

        self.sub_lang_label = tk.Label(root, text="Subtitle language (e.g., en, hu):")
        self.sub_lang_label.pack()

        self.sub_lang_entry = tk.Entry(root, width=10)
        self.sub_lang_entry.pack()

        self.threads_label = tk.Label(root, text="Number of threads:")
        self.threads_label.pack()

        self.threads_entry = tk.Entry(root, width=5)
        self.threads_entry.insert(0, "4")
        self.threads_entry.pack()

        self.download_button = tk.Button(root, text="Download", command=self.download)
        self.download_button.pack()

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path.set(directory)

    def download(self):
        url = self.url_entry.get()
        output_path = self.output_path.get()
        format_str = self.format_var.get()
        if "audio" in format_str:
            format_str = format_str.split(" ")[0]

        subtitles = self.subtitles_var.get()
        sub_lang = self.sub_lang_entry.get()
        threads = int(self.threads_entry.get())

        download_video(url, output_path, format_str, subtitles, sub_lang, threads)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
