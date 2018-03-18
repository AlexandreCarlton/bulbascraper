import mwparserfromhell as mw

class WikiPage(object):
    '''Provides parsed wikicode from a Pokemon Bulbapedia page.'''

    def __init__(self, page: str):
        self._wikicode = mw.parse(page) # type: mwparserfromhell.wikicode.Wikicode

    @property
    def info_box(self) -> mw.nodes.template.Template:
        templates = self._wikicode.ifilter_templates(matches='Pokémon Infobox')
        return next(templates)

    @property
    def game_data(self) -> mw.wikicode.Wikicode:
        return self._wikicode.get_sections(matches='Game data')[0]

    @property
    def base_stats(self) -> mw.wikicode.Wikicode:
        return self.game_data.get_sections(matches='Base stats')[0]

    @property
    def pokedex_entries(self) -> mw.wikicode.Wikicode:
        return self.game_data.get_sections(matches='Pokédex entries')[0]
