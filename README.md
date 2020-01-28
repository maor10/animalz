# animalz

Animalz uses the wikipedia page https://en.wikipedia.org/wiki/List_of_animal_names for it's data.
To use Animalz:

```python
import animalz

# Get a list of Animal objects
animals = animalz.get_animals_from_wiki_page()

# Get a mapping from collateral adjectives to animals
adjectives_to_animals = animalz.get_and_map_collateral_adjectives_to_animals_from_wiki_page()

# Download images async
animalz.download_images_asynchronously_from_animals(animals)

# Create html file
animalz.create_html_file_from_collateral_adjectives_to_animals(adjectives_to_animals, html_file_path="/tmp/whatever.html")
```

The complexity of mapping the animals is O(n).
