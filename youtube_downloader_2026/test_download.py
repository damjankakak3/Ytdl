import asyncio
import os
from downloader import Downloader
from uploader import Uploader

async def main():
    print("YouTube Downloader & Uploader Test")
    print("----------------------------------")

    url = input("Enter a YouTube URL (video or playlist): ").strip()
    if not url:
        print("No URL provided.")
        return

    downloader = Downloader()
    uploader = Uploader()

    is_playlist = 'playlist' in url or 'list=' in url

    print("\n[1/3] Downloading...")
    def my_hook(d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            print(f"\rDownloading... {percent}", end='', flush=True)
        elif d['status'] == 'finished':
            print("\nDownload finished, merging/post-processing...")

    try:
        if is_playlist:
            filepath, title = await downloader.download_playlist(url, progress_callback=my_hook)
        else:
            filepath, title = await downloader.download_video(url, progress_callback=my_hook)

        if not filepath or not os.path.exists(filepath):
            print("\nError: File was not created.")
            return

        print(f"\n[2/3] Download complete: {title}")
        print(f"File saved to: {filepath}")

        print("\n[3/3] Uploading to temporary host (Gofile)...")
        link = await uploader.upload_file(filepath)

        print(f"\nSuccess! Your file is available at:")
        print(f"-> {link}")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
