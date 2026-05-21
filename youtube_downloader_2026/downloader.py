import os
import yt_dlp
import asyncio

class Downloader:
    def __init__(self, download_path='downloads'):
        self.download_path = download_path
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    async def download_video(self, url, progress_callback=None):
        def _download():
            ydl_opts = {
                'format': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]', # Up to 4K
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'merge_output_format': 'mkv', # Better support for combining video/audio
                'quiet': True,
                'no_warnings': True,
            }

            if progress_callback:
                ydl_opts['progress_hooks'] = [progress_callback]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)
                # If merged, the extension might change
                base, ext = os.path.splitext(filename)
                if os.path.exists(base + '.mkv'):
                    filename = base + '.mkv'
                elif os.path.exists(base + '.mp4'):
                    filename = base + '.mp4'
                elif os.path.exists(base + '.webm'):
                    filename = base + '.webm'

                return filename, info_dict.get('title', 'Unknown Title')

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _download)

    async def download_playlist(self, url, progress_callback=None):
        def _download():
            ydl_opts = {
                'format': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]',
                'outtmpl': os.path.join(self.download_path, '%(playlist_title)s', '%(playlist_index)s - %(title)s.%(ext)s'),
                'merge_output_format': 'mkv',
                'quiet': True,
                'no_warnings': True,
                'extract_flat': 'in_playlist',
            }

            if progress_callback:
                ydl_opts['progress_hooks'] = [progress_callback]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # First extract info to get the playlist title for the folder
                info_dict = ydl.extract_info(url, download=False)
                if 'entries' not in info_dict:
                    return None # Not a playlist

                playlist_title = info_dict.get('title', 'Playlist')

                # Use sanitize_filename to avoid OS file path issues when making the zip
                from yt_dlp.utils import sanitize_filename
                sanitized_title = sanitize_filename(playlist_title, restricted=True)

                # Update outtmpl with sanitized title to match folder name that will actually be created
                ydl_opts['outtmpl'] = os.path.join(self.download_path, sanitized_title, '%(playlist_index)s - %(title)s.%(ext)s')

                # Now actually download
                ydl_opts['extract_flat'] = False
                with yt_dlp.YoutubeDL(ydl_opts) as ydl_down:
                    ydl_down.download([url])

                playlist_folder = os.path.join(self.download_path, sanitized_title)

                # Create a zip file of the playlist
                import shutil
                zip_filename = os.path.join(self.download_path, f"{sanitized_title}.zip")
                shutil.make_archive(os.path.join(self.download_path, sanitized_title), 'zip', playlist_folder)

                return zip_filename, playlist_title

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _download)
