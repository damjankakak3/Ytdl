import yt_dlp

def download_video(url, output_path=".", format="best", subtitles=False, sub_lang="en", threads=4):
    """Downloads a YouTube video or playlist from a given URL using yt-dlp."""
    try:
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'yes-playlist': True,
            'concurrent_fragment_downloads': threads,
        }
        if format in ["mp3", "m4a"]:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
            }]
        else:
            ydl_opts['format'] = format

        if subtitles:
            ydl_opts['writesubtitles'] = True
            ydl_opts['subtitleslangs'] = [sub_lang]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")
