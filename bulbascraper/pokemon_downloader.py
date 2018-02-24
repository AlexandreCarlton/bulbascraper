# On second thought, this isn't necessary.
# Really doesn't add much.

from pathlib import Path

import requests

from bulbascraper.wiki_downloader import WikiDownloader

INDEX_URL = 'http://bulbapedia.bulbagarden.net/w/index.php'


class PokemonWikiDownloader(object):

    """Downloads Pokemon Wikimedia file."""

    def __init__(self, wiki_downloader: WikiDownloader):
        self.wiki_downloader = wiki_downloader

    def download_pokemon(self, pokemon: str):
        """
        Downloads to <directory>/<pokemon>.wiki
        """
        self.wiki_downloader.download(pokemon + '_(Pokémon)')
