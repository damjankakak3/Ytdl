import argparse
import sys
import tkinter as tk
from gui import App
from downloader import download_video

if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="YouTube Downloader")
        parser.add_argument("url", help="The URL of the YouTube video or playlist to download.")
        parser.add_argument("-o", "--output", dest="output_path", default=".", help="The output directory.")
        parser.add_argument("-f", "--format", dest="format", default="best", help="The download format.")
        parser.add_argument("--subtitles", action="store_true", help="Download subtitles.")
        parser.add_argument("--sub-lang", dest="sub_lang", default="en", help="Subtitle language.")
        parser.add_argument("-t", "--threads", dest="threads", type=int, default=4, help="Number of concurrent fragments to download.")
        args = parser.parse_args()

        download_video(args.url, args.output_path, args.format, args.subtitles, args.sub_lang, args.threads)
    else:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
