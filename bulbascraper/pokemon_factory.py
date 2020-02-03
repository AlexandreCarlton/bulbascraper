import logging
from pathlib import Path

import mwparserfromhell as mw

from bulbascraper.base_stats_section import BaseStatsSection
from bulbascraper.info_box import InfoBox
from bulbascraper.pokedex_entries import PokedexEntries
from bulbascraper.pokemon_wiki_page import PokemonWikiPage
from bulbascraper.wiki_downloader import WikiDownloader
from bulbascraper.wiki_page import WikiPage

class PokemonFactory(object):

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self._parser = mw.parser.Parser()
        self.logger = logging.getLogger(__name__)

    def make_pokemon_wiki_page(self, name: str) -> PokemonWikiPage:
        filename = self.directory / (name +  '_(Pokémon).wiki')

        if not filename.exists():
            self.logger.info("File %s does not exist, downloading...", filename)
            downloader = WikiDownloader(self.directory)
            downloader.download_wiki(name + '_(Pokémon)')

        with filename.open('r') as wikifile:
            wikicode = self._parser.parse(wikifile.read())

        wiki_page = WikiPage(wikicode)
        return PokemonWikiPage(wiki_page)
