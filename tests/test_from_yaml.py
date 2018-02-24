"""
Tests the entire translation in its entirety, from page to Pokemon.
"""
from pathlib import Path

import pytest

from bulbascraper.pokemon_factory import PokemonFactory

from pokemon_yaml import PokemonYaml

POKEMON = [
    'Charizard',
    'Deoxys'
]

@pytest.fixture(scope='module', params=POKEMON)
def pokemon(request):
    factory = PokemonFactory(Path('wikimedia/pokemon'))
    pokemon_wiki = factory.make_pokemon_wiki_page(request.param)

    with open(f'tests/pokemon_yaml/{request.param}.yaml') as yaml_file:
        pokemon_yaml = PokemonYaml(yaml_file)
    return pokemon_wiki, pokemon_yaml


def test_name(pokemon):
    actual, expected = pokemon
    assert actual.name == expected.name

def test_forms(pokemon):
    actual, expected = pokemon
    assert actual.forms == expected.forms

def test_types(pokemon):
    actual, expected = pokemon
    assert actual.types == expected.types

def test_images(pokemon):
    actual, expected = pokemon
    assert actual.images == expected.images

def test_base_stats(pokemon):
    actual, expected = pokemon
    assert actual.base_stats == expected.base_stats

def test_pokedex_entries(pokemon):
    actual, expected = pokemon
    assert actual.pokedex_entries == expected.pokedex_entries

