# YouTube Downloader

This is a simple YouTube downloader with a command-line interface (CLI) and a graphical user interface (GUI).

## Features

- Download YouTube videos and playlists
- Choose video and audio formats
- Download audio only
- Download subtitles
- Concurrent downloads

## Installation

1. Clone the repository:
   ```
   git clone <repository_url>
   ```
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. **Important:** For audio format conversion (e.g., to MP3), you need to install `ffmpeg`. You can download it from [https://ffmpeg.org/](https://ffmpeg.org/).

## Usage

### GUI

To start the graphical user interface, run the following command:
```
python3 src/main.py
```

### CLI

To download a video or playlist, use the following command:
```
python3 src/main.py <url> [options]
```

**Options:**
- `-o, --output <path>`: The output directory.
- `-f, --format <format>`: The download format (e.g., `best`, `mp4`, `mp3`).
- `--subtitles`: Download subtitles.
- `--sub-lang <lang>`: Subtitle language (e.g., `en`, `hu`).
- `-t, --threads <number>`: Number of concurrent fragments to download.
