from __future__ import unicode_literals
import yt_dlp

from PIL import Image
from io import BytesIO
from pathlib import Path
from datetime import datetime
import requests

from . import extractor
from . import storage
from . import authenticator


class BasketCase:
    def __init__(self):
        # Create application data directory
        self._data_directory = f'{Path.home()!s}/.basketcase'
        Path(self._data_directory).mkdir(parents=True, exist_ok=True)

        # Set output path
        self._output_base = f'{Path.cwd()!s}/basketcase_{datetime.now()!s}'
        self._output_images = self._output_base + '/images'
        self._output_videos = self._output_base + '/videos'

        # Initialize dependencies
        self._storage = storage.Storage(self._data_directory)
        self._http_client = requests.Session()
        self.authenticator = authenticator.Authenticator(self._http_client, self._storage)
        self._extractor = extractor.Extractor(self._http_client)

    def fetch(self, target_urls):
        resources = self._extractor.scan(target_urls)

        if resources['images'] or resources['videos']:
            # Create media output directories
            Path(self._output_images).mkdir(parents=True, exist_ok=True)
            Path(self._output_videos).mkdir(parents=True, exist_ok=True)

            for index, resource in resources['images'].items():
                self._get_image(resource)
            
            self._get_videos(resources['videos'])
        else:
            print('Nothing to download.')

    def _get_image(self, resource):
        print(f'Downloading image: {resource["url"]}')

        image = None

        with self._http_client.get(resource['url'], timeout=10) as request:
            # Build image from binary response data
            image = Image.open(BytesIO(request.content))

        image.save(f'{self._output_images}/{resource["id"]}.jpg', format='JPEG')

    def _get_videos(self, urls):
        if self._http_client.cookies.get('sessionid'):
            # Add the session cookie
            yt_dlp.utils.std_headers.update({'Cookie': 'sessionid=' + self._http_client.cookies.get('sessionid')})

        ydl_opts = {
            'outtmpl': self._output_videos + '/%(title)s.%(ext)s'  # Set output directory
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)
