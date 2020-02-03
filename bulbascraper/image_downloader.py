
from io import StringIO
import logging
from pathlib import Path

from lxml import etree
import requests

class NoImageException(Exception):
    pass

class ImageDownloader(object):

    """
    Downloads official artwork from bulbapedia.
    Image filenames should be roughly match <pokedex_number><pokemon>.png;
    though this may vary with forms and special characters.
    The filename can be found from the InfoBox the main Pokemon article.
    """

    def __init__(self, directory: Path):
        self.directory = directory
        self.html_parser = etree.HTMLParser()
        self.logger = logging.getLogger(self.__class__.__name__)

    def download_image(self, image_filename: str, overwrite: bool=True):
        """
        Locates the filename on Bulbapedia, and downloads it to the
        directory.
        """
        destination = self.directory / image_filename
        image_url = self.get_image_url(image_filename)
        image_response = requests.get(image_url)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('wb') as image_file:
            image_file.write(image_response.content)

    def get_image_url(self, image_filename: str):
        """
        Retrieve the URL of the official artwork of the pokemon with the given
        image filename.
        """
        url = 'https://bulbapedia.bulbagarden.net/wiki/File:{}'.format(image_filename)
        self.logger.debug("Downloading url %s", url)
        site_response = requests.get(url)
        tree = etree.parse(StringIO(site_response.text), self.html_parser) # type: etree.ElementTree
        try:
            hyperlink_element = tree.xpath("//div[@id='file']/a")[0]
        except IndexError:
            raise NoImageException("No image filename found for '{}'.".format(image_filename))
        href = hyperlink_element.attrib['href']
        self.logger.debug("href attribute found with value %s", href)

        return 'https:' + href
