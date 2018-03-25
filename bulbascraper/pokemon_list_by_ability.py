from pathlib import Path
from typing import Iterator, Optional

from dataclasses import dataclass
import mwparserfromhell as mw

from bulbascraper.wiki_downloader import WikiDownloader

@dataclass
class LopAbility(object):
    menu_sprite: str
    pokemon_name: str
    ability_1: str
    ability_2: Optional[str]
    ability_2_generation_onwards: Optional[int]
    hidden_ability: Optional[int]
    hidden_ability_generation_onwards: Optional[int]
    form: Optional[str]


class PokemonListByAbility(object):

    def __init__(self, wiki_directory: Path):
        self.wiki_directory = wiki_directory

    def __iter__(self) -> Iterator[LopAbility]:
        wiki_filepath = self.wiki_directory / 'List_of_Pokémon_by_Ability.wiki'
        if not wiki_filepath.exists():
            wiki_downloader = WikiDownloader(self.wiki_directory)
            wiki_downloader.download_wiki('List_of_Pokémon_by_Ability')
        with wiki_filepath.open('r') as wiki_file:
            wikicode = mw.parse(wiki_file)
        templates = wikicode.filter_templates(matches='lop/ability')
        for template in templates:
            yield LopAbility(menu_sprite=get(template, 1),
                             pokemon_name=get(template, 2),
                             ability_1=get(template, 3),
                             ability_2=get(template, 4),
                             ability_2_generation_onwards=get(template, 5),
                             hidden_ability=get(template, 6),
                             hidden_ability_generation_onwards=get(template, 7),
                             form=get(template, 8))

def get(template, key, default=None):
    if template.has(key):
        return template.get(key)
    return default
