from concurrent.futures import wait
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict, List
from bs4 import BeautifulSoup

from .animal import Animal
from .fetcher import get_animals_from_wiki_page


def map_collateral_adjectives_to_animals(animals) -> Dict[str, List[Animal]]:
    """
    Creates and returns a mapping from each collateral adjective to all the animals in it

    :param animals: to create mapping from

    :return: mapping from collateral adjective to animal
    """
    collateral_adjectives_to_animals = {}
    for animal in animals:
        for collateral_adjective in animal.collateral_adjectives:
            collateral_adjectives_to_animals.setdefault(collateral_adjective, []).append(animal)
    return collateral_adjectives_to_animals


def get_and_map_collateral_adjectives_to_animals_from_wiki_page() -> Dict[str, List[Animal]]:
    """
    Main entry point - will retrieve all the animals from the wiki page,
    and then map the collateral adjectives to the animals

    :return: mapping from collateral adjective to animal
    """
    animals = get_animals_from_wiki_page()
    return map_collateral_adjectives_to_animals(animals)



def download_images_asynchronously_from_animals(animals: List[Animal], workers: int=10):
    """
    Download images asynchronously from a list of animals- will get the default wikipedia pic for each animal
    Will return when all images have finished downloading

    :param animals: to download images from
    :param workers: number of workers
    """
    executor = ThreadPoolExecutor(max_workers=workers)
    futures = [executor.submit(animal.download_image) for animal in animals]
    wait(futures)


def create_html_file_from_collateral_adjectives_to_animals(collateral_adjectives_to_animals: Dict[str, List[Animal]],
                                                           html_file_path: str):
    """
    Create an html file displaying the mapping from collateral adjectives to the animals

    :param collateral_adjectives_to_animals: a mapping from collateral adjectives to a list of animals
    :param html_file_path: path to save html at
    """
    soup = BeautifulSoup("<html></html>")
    original_tag = soup.html

    table = soup.new_tag("table")
    original_tag.append(table)
    for collateral_adjective, animals in collateral_adjectives_to_animals.items():
        row = soup.new_tag("tr")
        collateral_adjective_column = soup.new_tag("td")
        collateral_adjective_column.append(collateral_adjective)
        row.append(collateral_adjective_column)
        animals_column = soup.new_tag("td")
        for animal in animals:
            animals_column.append(animal.name)
            animals_column.append(soup.new_tag("br"))
        row.append(animals_column)
        table.append(row)
    with open(html_file_path, 'w') as f:
        f.write(str(soup))
