
import pytest

import itertools
from pathlib import Path
from bulbascraper.pokemon_list_by_ability import (PokemonListByAbility,
                                                  LopAbility)

@pytest.fixture(scope='module')
def pokemon_menu_sprites():
    abilities = PokemonListByAbility(Path('wikimedia'))
    grouped = itertools.groupby(abilities, key=lambda ability: ability.pokemon_name)
    return {pokemon_name: [ability.menu_sprite
                           for ability in grouped_abilities]
            for pokemon_name, grouped_abilities in grouped}

@pytest.mark.parametrize('pokemon_name,menu_sprites', [
    ('Bulbasaur', ['001']),
    ('Charizard', ['006', '006MX', '006MY']),
    ('Deoxys', ['386', '386A', '386D', '386S'])
], ids=str)
def test_pokemon_menu_sprites(pokemon_menu_sprites, pokemon_name, menu_sprites):
    assert pokemon_menu_sprites[pokemon_name] == menu_sprites
