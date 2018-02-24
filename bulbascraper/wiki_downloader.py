
from pathlib import Path

import requests

URL = 'http://bulbapedia.bulbagarden.net/w/index.php'

# TODO: Should really allow destination in download_wiki to make things more
# transparent;
# Could be reduced to a function, really (but it's good to be consistent with
# the ImageDownloader)
# Then have other downloader functions that use this one.
class WikiDownloader(object):
    """
    Downloads a raw media wiki file into a specified directory.
    """

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def download_wiki(self, title: str) -> None:
        req = requests.get(URL, params={'title': title, 'action': 'raw'})
        wiki_path = self.directory / (title + '.wiki')
        with wiki_path.open('w') as wiki_file:
            wiki_file.write(req.text)
