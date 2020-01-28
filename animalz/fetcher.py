from typing import List
import bs4
import requests

from .animal import Animal


ANIMAL_WIKI_PAGE = 'https://en.wikipedia.org/wiki/List_of_animal_names'

NUMBER_OF_COLUMNS_IN_ANIMAL_ROW = 7

ANIMALS_TABLE_HEADER = "Animal"


def is_animal_table(table: bs4.element.Tag) -> bool:
    """
    Checks whether a given table is the animal table
    Since there's no special ID on the animal table, we'll define it as the first table to have
    'Animal' as it's first header column

    :param table: to check

    :return: whether it's the animal table
    """
    first_row = table.find('tr')
    if first_row is not None:
        first_header = first_row.find('th')
        return first_header is not None and first_header.get_text() == ANIMALS_TABLE_HEADER
    return False


def parse_animal_from_row(row: bs4.element.Tag) -> Animal:
    """
    Parse an animal from the row
    First column is the name, sixth column is the adjective

    :param row: to get animal from

    :return: animal
    """
    columns = row.find_all('td')
    name_column = columns[0]
    collateral_adjectives_column = columns[5]
    collateral_adjectives = [c.strip() for c in collateral_adjectives_column.contents if isinstance(c, str)]
    return Animal(name=name_column.get_text(),
                  collateral_adjectives=collateral_adjectives,
                  link=name_column.find('a').attrs['href'])


def get_animals_from_animal_table(animal_table: bs4.element.Tag) -> List[Animal]:
    """
    Get a list of animals from the animal table, skipping over irrelevant rows

    :param animal_table: to get animals from

    :return: animals
    """
    # We're starting from row 1: because we want to skip the header row
    return [parse_animal_from_row(row) for row in animal_table.find_all('tr')[1:]
            if len(row.find_all('td')) == NUMBER_OF_COLUMNS_IN_ANIMAL_ROW]


def get_animals_from_wiki_page() -> List[Animal]:
    """
    Get all the animals from the wiki page

    :return: list<Animal>
    """
    res = requests.get(ANIMAL_WIKI_PAGE)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content)
    animal_table = next(table for table in soup.find_all('table') if is_animal_table(table))
    return get_animals_from_animal_table(animal_table)
