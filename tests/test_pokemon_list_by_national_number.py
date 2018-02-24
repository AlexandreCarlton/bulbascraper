
import pytest

from pathlib import Path
from bulbascraper.pokemon_list_by_national_pokedex_number import PokemonListByNationalPokedexNumber

@pytest.fixture(scope='module')
def pokemon_list():
    return list(PokemonListByNationalPokedexNumber(Path('wikimedia')))

@pytest.mark.parametrize("number,pokemon", [
    (1, "Bulbasaur"),
    (152, "Chikorita"),
    (252, "Treecko"),
    (387, "Turtwig"),
    (495, "Snivy"),
    (650, "Chespin"),
    (650, "Chespin"),
    (722, "Rowlet")
])
def test_pokemon_list_by_national_pokedex_number(pokemon_list, number, pokemon):
    assert pokemon_list[number - 1] == pokemon
