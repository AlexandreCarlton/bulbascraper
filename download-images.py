#!/usr/bin/env python

import logging
from pathlib import Path

import mwparserfromhell as mw
from bulbascraper.image_downloader import ImageDownloader, NoImageException
from bulbascraper.info_box import InfoBox

logging.basicConfig(level=logging.DEBUG)

pokemon_wiki_directory = Path('wikimedia/pokemon')

image_directory = Path('images')
image_directory.mkdir(parents=True, exist_ok=True)

image_downloader = ImageDownloader(image_directory)


for pokemon_wiki_filename in pokemon_wiki_directory.glob('*.wiki'):

    with pokemon_wiki_filename.open('r') as wikifile:
        wikicode = mw.parse(wikifile.read())

    template = next(wikicode.ifilter_templates(
        matches=lambda node: node.name.strip() == 'Pokémon Infobox'))
    info_box = InfoBox(template)

    for image_filename in info_box.images:
        if not (image_directory / image_filename).exists():
            try:
                image_downloader.download_image(image_filename)
            except NoImageException as exception:
                print(exception.args)
