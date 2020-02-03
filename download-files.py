#!usr/bin/env python3

import logging
import os
from pathlib import Path
from typing import Iterable

import mwparserfromhell as mw
import requests

URL = 'http://bulbapedia.bulbagarden.net/w/index.php'
POKEMON_LIST_TITLE = 'List_of_Pokémon_by_National_Pokédex_number'
MOVE_LIST_TITLE = None # TODO

def download_file(title: str, filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    req = requests.get(URL, params={'title': title, 'action': 'raw'})
    with filepath.open('w') as wikifile:
        wikifile.write(req.text)

def get_pokemon_list() -> Iterable[str]:
    filepath = Path('wikimedia') / (POKEMON_LIST_TITLE + '.wiki')
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
        pokepath = Path('wikimedia') / 'pokemon2' / (pokemon + '.wiki')
        print("{} does not exist, downloading.".format(pokepath))
        download_file(pokemon + '_(Pokémon)', pokepath)



if __name__ == "__main__":
    get_pokemon_list()
