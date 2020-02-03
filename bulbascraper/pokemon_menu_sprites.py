
import itertools
from typing import List
from bulbascraper.pokemon_list_by_ability import PokemonListByAbility

class PokemonMenuSprites(object):

    def __init__(self, abilities: PokemonListByAbility):
        grouped = itertools.groupby(abilities, key=lambda ability: ability.pokemon_name)
        self._menu_sprites =  {str(pokemon_name): [ability.menu_sprite
                                                   for ability in grouped_abilities]
                               for pokemon_name, grouped_abilities in grouped}

    def __getitem__(self, key) -> List[str]:
        return self._menu_sprites[key]
