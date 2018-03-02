from typing import Dict, Iterator, List, Tuple, Union
import yaml

from bulbascraper.pokemon_type import PokemonType
from bulbascraper.base_stats import BaseStats, BaseStatsRBY

# It's easier to use the class (and test it, even) if we return a dict instead
# of an iterable of key-value pairs.
# Then we can go: charizard.pokedex_entry['Red']

class PokemonYaml(object):
    """
    A test mirror to PokemonWikiPage.
    """

    def __init__(self, yaml_file):
        self._yaml = yaml.load(yaml_file)

    @property
    def name(self) -> str:
        return self._yaml['name']

    @property
    def forms(self) -> List[str]:
        return self._yaml['forms']

    @property
    def images(self) -> Dict[str, str]:
        return {image['form']: image['filename']
                for image in self._yaml.get('images', [])}

    @property
    def types(self) -> Dict[str, PokemonType]:
        return {type_['form']: PokemonType(type_['primary'],
                                           type_.get('secondary'))
                for type_ in self._yaml.get('types', [])}

    @property
    def pokedex_entries(self) -> Dict[str, Dict[str, str]]:
        pokedex_entries = {}
        for pokedex_yaml_entry in self._yaml.get('pokedex_entries', []):
            for form in pokedex_yaml_entry['forms']:
                pokedex_entries[form] = {}
                for entry in pokedex_yaml_entry['entries']:
                    pokedex_entries[form][entry['version']] = entry['entry']
        return pokedex_entries

    @property
    def base_stats(self) -> Dict[Tuple[str, int], Union[BaseStats, BaseStatsRBY]]:
        base_stats = {}
        for stat in self._yaml['base_stats']:
            form = stat['form']
            generations = stat['generations']
            for generation in generations:
                if generation == 1:
                    base_stats[form, generation] = BaseStatsRBY(
                        hit_points=stat['hit_points'],
                        attack=stat['attack'],
                        defence=stat['defence'],
                        special=stat['special'],
                        speed=stat['speed'])
                else:
                    base_stats[form, generation] = BaseStats(
                        hit_points=stat['hit_points'],
                        attack=stat['attack'],
                        defence=stat['defence'],
                        special_attack=stat['special_attack'],
                        special_defence=stat['special_defence'],
                        speed=stat['speed'])
        return base_stats
