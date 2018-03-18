from pathlib import Path

import mwparserfromhell as mw

from bulbascraper.base_stats_section import BaseStatsSection
from bulbascraper.info_box import InfoBox
from bulbascraper.pokedex_entries import PokedexEntries
from bulbascraper.pokemon_wiki_page import PokemonWikiPage
from bulbascraper.wiki_downloader import WikiDownloader

class PokemonFactory(object):

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self._parser = mw.parser.Parser()

    def make_pokemon_wiki_page(self, name: str) -> PokemonWikiPage:
        filename = self.directory / (name +  '_(Pokémon).wiki')

        if not filename.exists():
            downloader = WikiDownloader(self.directory)
            downloader.download_wiki(name + '_(Pokémon)')

        with filename.open('r') as wikifile:
            wikicode = self._parser.parse(wikifile.read())

        templates = wikicode.filter_templates()
        game_data = wikicode.get_sections(matches='Game data',
                                          include_headings=False)[0]

        info_box = InfoBox(next(template
                                for template in templates
                                if template.name.strip() == 'Pokémon Infobox'))
        pokedex_entries = PokedexEntries(
            game_data.get_sections(matches='Pokédex entries',
                                   include_headings=False)[0])
        base_stats = wikicode.get_sections(matches='Base stats')[0]

        return PokemonWikiPage(info_box=info_box,
                               pokedex_entries=pokedex_entries,
                               base_stats=BaseStatsSection(base_stats))


