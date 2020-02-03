#!usr/bin/env python3

import logging
import os
from pathlib import Path
from typing import Iterable

import requests

URL = 'https://pokeapi.co/api/v2'
POKEMON_LIST_TITLE = 'List_of_Pokémon_by_National_Pokédex_number'
MOVE_LIST_TITLE = None # TODO

# https://pokeapi.co/api/v2/pokedex/national/
# https://pokeapi.co/api/v2/pokemon-species/bulbasaur/
# https://pokeapi.co/api/v2/pokemon/bulbasaur/

def download_file(title: str, filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    req = requests.get(URL)
    with filepath.open('w') as jsonfile:
        jsonfile.write(req.text)

def get_pokemon_list() -> Iterable[str]:
    # TODO: Make this write to json files for caching purposes.
    filepath = Path('pokeapi') / (POKEMON_LIST_TITLE + '.j')
    print(filepath)
    if not filepath.exists():
        print("{} does not exist, downloading.".format(filepath))
        download_file(POKEMON_LIST_TITLE, filepath)
    with filepath.open('r') as wikifile:
        wikicode = mw.parse(wikifile)
    templates = wikicode.filter_templates(
        matches=lambda node: node.name == 'rdex')
    pokemon_set = { str(template.get(3)) for template in templates }
    for pokemon in sorted(pokemon_set):
        pokepath = Path('wikimedia') / 'pokemon' / (pokemon + '.wiki')
        print("{} does not exist, downloading.".format(pokepath))
        download_file(pokemon + '_(Pokémon)', pokepath)



if __name__ == "__main__":
    get_pokemon_list()
