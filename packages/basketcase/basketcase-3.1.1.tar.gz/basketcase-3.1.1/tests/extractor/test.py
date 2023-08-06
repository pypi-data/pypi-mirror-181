from basketcase.extractor import Extractor

import unittest
from importlib import resources
from unittest.mock import MagicMock

import requests
import json


class ExtractorTest(unittest.TestCase):
    def test_get_media_id(self):
        response = MagicMock()
        response.text = resources.read_text('tests.extractor.sample', 'response.html')

        http = requests.Session()
        http.get = MagicMock(return_value=response)

        extractor = Extractor(http)
        media_id = extractor._get_media_id('https://www.instagram.com/p/CJjfDDgptFw/')
        self.assertEqual(media_id, '2477960769353208176')

    def test_get_media_info(self):
        response = MagicMock()
        sample = resources.read_text('tests.extractor.sample', 'api.json')
        sample = json.loads(sample)
        response.json = MagicMock(return_value=sample)

        http = requests.Session()
        http.get = MagicMock(return_value=response)

        extractor = Extractor(http)
        media_info = extractor._get_media_info('2477960769353208176')
        self.assertIsInstance(media_info, dict)
