from typing import Dict, List

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
