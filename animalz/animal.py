import json
import os
from dataclasses import dataclass
from typing import List, Dict

import requests

WIKIPEDIA_API_METADATA_URL = 'https://en.wikipedia.org/api/rest_v1/page/summary/{animal_name}'

DOWNLOAD_DIRECTORY = '/tmp/animal_pics'


@dataclass
class Animal:

    name: str
    collateral_adjectives: List[str]
    link: str

    def get_api_metadata(self) -> Dict:
        """
        Get wikipedia metadata for animal

        :return: metadata
        """
        response = requests.get(WIKIPEDIA_API_METADATA_URL.format(animal_name=self.name))
        response.raise_for_status()
        return json.loads(response.content)

    def download_image(self) -> str:
        """
        Downloads the animals image from wikipedia to the DOWNLOAD_DIRECTORY

        :return: the image name
        """
        metadata = self.get_api_metadata()
        source_url = metadata['originalimage']['source']
        image = requests.get(source_url)
        image_name = source_url.split("/")[-1]
        os.makedirs(DOWNLOAD_DIRECTORY, exist_ok=True)
        with open(os.path.join(DOWNLOAD_DIRECTORY, image_name), 'wb') as f:
            f.write(image.content)
        return image_name
