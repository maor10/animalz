from dataclasses import dataclass
from typing import List


@dataclass
class Animal:

    name: str
    collateral_adjectives: List[str]
    link: str