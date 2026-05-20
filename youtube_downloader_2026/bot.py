import discord
import os
import asyncio
import re
from downloader import Downloader
from uploader import Uploader

# Setup Intents
intents = discord.Intents.default()
intents.message_content = True

class YTDLBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.downloader = Downloader()
        self.uploader = Uploader()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        print('Bot is ready to receive direct messages!')

    async def on_message(self, message):
        # Ignore messages from ourselves
        if message.author == self.user:
            return

        # Only process Direct Messages
        if not isinstance(message.channel, discord.DMChannel):
            return

        content = message.content.strip()

        # Simple URL regex (not perfect, but good enough for youtube links)
        url_match = re.search(r'(https?://[^\s]+)', content)

        if not url_match:
            await message.channel.send("Hello! Please send me a YouTube link (video or playlist) and I'll download it for you in up to 4K quality.")
            return

        url = url_match.group(1)
        is_playlist = 'playlist' in url or 'list=' in url
        media_type = "playlist" if is_playlist else "video"

        status_message = await message.channel.send(f"Found a {media_type} link! \n\n<a:loading:1021272635398750248> **Step 1/3: Downloading...** (This might take a while for 4K or playlists)")

        def progress_hook(d):
            # In a real scenario, updating Discord too frequently hits rate limits.
            # We would throttle updates here. For simplicity, we just use the initial status message.
            pass

        try:
            # 1. Download
            if is_playlist:
                filepath, title = await self.downloader.download_playlist(url, progress_callback=progress_hook)
            else:
                filepath, title = await self.downloader.download_video(url, progress_callback=progress_hook)

            if not filepath or not os.path.exists(filepath):
                await status_message.edit(content=f"❌ Error: Could not download the {media_type}.")
                return

            await status_message.edit(content=f"✅ **Step 1/3: Download Complete!** (`{title}`)\n<a:loading:1021272635398750248> **Step 2/3: Uploading to temporary host...**")

            # 2. Upload
            link = await self.uploader.upload_file(filepath)

            # 3. Clean up local file (optional but good for space)
            try:
                os.remove(filepath)
                # If it was a playlist, we also have the unzipped folder
                if is_playlist:
                    import shutil
                    folder_path = filepath.rsplit('.zip', 1)[0]
                    if os.path.exists(folder_path):
                        shutil.rmtree(folder_path)
            except Exception as e:
                print(f"Cleanup error: {e}")

            await status_message.edit(content=f"✅ **Step 2/3: Upload Complete!**\n✅ **Step 3/3: All done!**\n\nHere is your link (valid for a limited time): {link}")

        except Exception as e:
            await status_message.edit(content=f"❌ An error occurred during processing:\n```\n{e}\n```")


def main():
    token_file = "bot_token.txt"
    token = None

    if os.path.exists(token_file):
        with open(token_file, "r") as f:
            token = f.read().strip()

    if not token:
        print("Discord Bot Token not found.")
        token = input("Please enter your Discord Bot Token: ").strip()

        save = input("Do you want to save this token for next time? (y/n): ").strip().lower()
        if save == 'y':
            with open(token_file, "w") as f:
                f.write(token)
            print(f"Token saved to {token_file}")

    if not token:
        print("No token provided. Exiting.")
        return

    client = YTDLBot(intents=intents)

    try:
        client.run(token)
    except discord.errors.LoginFailure:
        print("Invalid token provided. Please check your token and try again.")
        if os.path.exists(token_file):
            os.remove(token_file)

if __name__ == "__main__":
    main()
