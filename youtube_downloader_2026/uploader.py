import aiohttp
import os
import json

class Uploader:
    def __init__(self):
        self.server = None

    async def _get_server(self):
        if not self.server:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.gofile.io/servers') as response:
                    data = await response.json()
                    if data.get('status') == 'ok':
                        self.server = data['data']['servers'][0]['name']
                    else:
                        raise Exception("Failed to get Gofile server")
        return self.server

    async def upload_file(self, filepath):
        server = await self._get_server()
        url = f'https://{server}.gofile.io/contents/uploadfile'

        filename = os.path.basename(filepath)

        async with aiohttp.ClientSession() as session:
            with open(filepath, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', f, filename=filename)

                async with session.post(url, data=data) as response:
                    result = await response.json()
                    if result.get('status') == 'ok':
                        return result['data']['downloadPage']
                    else:
                        raise Exception(f"Upload failed: {result}")
