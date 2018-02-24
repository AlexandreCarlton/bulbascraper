from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union

import mwparserfromhell as mw

from bulbascraper.info_box import InfoBox, ImageFilename
from bulbascraper.pokedex_entries import PokedexEntries, PokedexEntry
from bulbascraper.pokemon_type import PokemonType
from bulbascraper.base_stats import BaseStats, BaseStatsRBY
from bulbascraper.base_stats_section import BaseStatsSection

CURRENT_GENERATION = 7

class PokemonWikiPage(object):
    """
    A Pokemon Wikipedia page.
    """

    def __init__(self,
                 info_box: InfoBox,
                 pokedex_entries: PokedexEntries,
                 base_stats: BaseStatsSection,
                 ) -> None:
        self._info_box = info_box
        self._pokedex_entries = pokedex_entries
        self._base_stats = base_stats

    @property
    def name(self) -> str:
        return self._info_box.name

    @property
    def forms(self) -> List[str]:
        return list(self._info_box.forms)

    @property
    def types(self) -> Dict[str, PokemonType]:
        """This does not take into account generational type changes."""
        return self._info_box.types

    @property
    def images(self) -> Dict[str, str]:
        return {image.form: image.filename
                for image in self._info_box.images}

    @property
    def generation(self) -> int:
        return self._info_box.generation

    @property
    def pokedex_entries(self) -> Dict[str, str]:
        return {entry.version: entry.entry
                for entry in self._pokedex_entries}

    @property
    def base_stats(self) -> Dict[Tuple[str, int], Union[BaseStats, BaseStatsRBY]]:
        """
        Note that Mega forms, so far, have only been introduced in Gen VI.
        """

        base_stats = {}

        # generations == None => All generations
        # generations == (x, None) => All generations after (& including) x
        # form == None => Pokemon's name
        for subsection in self._base_stats.subsections:
            form = subsection.form or self.name
            # All forms are introduced in the same generation as the pokemon,
            # With the exception of Mega forms, which were all introduced in generation 6.
            if form.startswith('Mega '):
                generations = range(6, CURRENT_GENERATION + 1)
            elif subsection.generations is None:
                generations = range(self.generation, CURRENT_GENERATION + 1)
            else:
                start, end = subsection.generations
                end = end or CURRENT_GENERATION
                generations = range(start, end + 1)
            for generation in generations:
                if generation == 1:
                    print(type(form))
                    print(type(generation))
                    base_stats[form, generation] = BaseStatsRBY(
                        hit_points=subsection.hit_points,
                        attack=subsection.attack,
                        defence=subsection.defence,
                        special=subsection.special,
                        speed=subsection.speed)
                else:
                    base_stats[form, generation] = BaseStats(
                        hit_points=subsection.hit_points,
                        attack=subsection.attack,
                        defence=subsection.defence,
                        special_attack=subsection.special_attack,
                        special_defence=subsection.special_defence,
                        speed=subsection.speed)
        return base_stats
