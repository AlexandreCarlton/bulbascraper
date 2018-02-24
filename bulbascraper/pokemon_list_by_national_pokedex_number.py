import itertools
from pathlib import Path
from typing import Iterator

import mwparserfromhell as mw

from bulbascraper.wiki_downloader import WikiDownloader


class PokemonListByNationalPokedexNumber(object):

    def __init__(self, wiki_directory: Path):
        self.wiki_directory = wiki_directory

    def __iter__(self) -> Iterator[str]:
        wiki_filepath = self.wiki_directory / 'List_of_Pokémon_by_National_Pokédex_number.wiki'
        if not wiki_filepath.exists():
            wiki_downloader = WikiDownloader(self.wiki_directory)
            wiki_downloader.download_wiki('List_of_Pokémon_by_National_Pokédex_number')
        with wiki_filepath.open('r') as wiki_file:
            wikicode = mw.parse(wiki_file)
        templates = wikicode.filter_templates(
            matches=lambda node: node.name == 'rdex')
        # Different forms for a Pokemon are listed multiple times; so we just
        # collapse them.
        grouped = itertools.groupby(templates, lambda t: str(t.get(3)))
        for name, _ in grouped:
            yield name
