from typing import Iterable, Iterator, Optional, Union, Tuple

from dataclasses import dataclass
import mwparserfromhell as mw

CURRENT_GENERATION = 7 # TODO: Make better? Would rather not have 'current_generation' everywhere


# TODO: dataclass this!
@dataclass
class BaseStatsSubsection(object):
    """
    Contains BaseStats in addition to metadata (generation, form, etc).
    """
    hit_points: int
    attack: int
    defence: int
    special_attack: int
    special_defence: int
    speed: int
    special: Optional[int] = None

    form: Optional[str] = None
    generations: Optional[Tuple[int, Optional[int]]] = None


class BaseStatsSection(object):

    def __init__(self, section: mw.wikicode.Wikicode):
        '''section is the "Base stats" section.'''
        self._section = section

    @property
    def subsections(self) -> Iterator[BaseStatsSubsection]:
        '''Extracts all base stats for the Pokemon.

        Note that we have several cases:
        - No subsections => Only one Base Stats is available
        - "Generation <x>" => The base form has had stat changes between generations
        - "<Form>" => Applies to the regular form

        Good test cases:
        - Pidgeot (generational changes + mega)
        - Charizard (Only mega changes)
        - Bulbasaur (no changes)
        '''


        section_without_heading = self._section.get_sections(
            include_headings=False, include_lead=False)[0]
        subsections = section_without_heading.get_sections(include_lead=False)

        if not subsections:
            # We have only one set of base stats; just grab the first template.
            template = next(self._section.ifilter_templates(
                lambda node: node.name.startswith('Base stats')))
            yield self._get_base_stats_subsection(template)
        else:
            for section in subsections:
                # We may have sections for forms and generations.
                heading = next(section.ifilter_headings())
                template = next(section.ifilter_templates())
                if heading.title.startswith('Generation '):
                    # We have a generational change
                    raw_generation_range = heading.title[len('Generation '):]
                    generation_interval = self._make_interval(raw_generation_range)
                    subsection = self._get_base_stats_subsection(template)
                    subsection.generations = generation_interval
                    yield subsection
                else:
                    subsection = self._get_base_stats_subsection(template)
                    subsection.form = heading.title.strip()
                    yield subsection

    def _get_base_stats_subsection(self, template: mw.nodes.Template) -> BaseStatsSubsection:
        base_stats = BaseStatsSubsection(
            hit_points=self._get_stat('HP', template),
            attack=self._get_stat('Attack', template),
            defence=self._get_stat('Defense', template),
            special_attack=self._get_stat('SpAtk', template),
            special_defence=self._get_stat('SpDef', template),
            speed=self._get_stat('Speed', template))

        if template.has('Special'):
            base_stats.special = self._get_stat('Special', template)

        return base_stats

    @staticmethod
    def _get_stat(name: str, template: mw.nodes.Template) -> int:
        return int(template.get(name).value.strip())

    @staticmethod
    def _make_interval(raw_interval: str) -> Tuple[int, Optional[int]]:
        """
        Creates a closed interval.
        The latter endpoint may be None, indicating that it is unbounded.
        e.g. (1, None) -> Generation 1 onwards.

        """
        if raw_interval.endswith('onward'):
            starting_generation = raw_interval.split()[0]
            return RomanNumeralConverter.to_int(starting_generation), None
        generations = raw_interval.split('-', 1)
        if len(generations) == 1:
            generation_int = RomanNumeralConverter.to_int(generations[0])
            if generations[0] == CURRENT_GENERATION:
                # The latest generation doesn't have 'onward'.
                return RomanNumeralConverter.to_int(generations[0]), None
            return generation_int, generation_int
        return (RomanNumeralConverter.to_int(generations[0]),
                RomanNumeralConverter.to_int(generations[1]))

class RomanNumeralConverter(object):
    NUMERALS = [
        ('M', 1000),
        ('CM', 900),
        ('D', 500),
        ('CD', 400),
        ('C', 100),
        ('XC', 90),
        ('L', 50),
        ('XL', 40),
        ('X', 10),
        ('IX', 9),
        ('V', 5),
        ('IV', 4),
        ('I', 1)
    ]

    @staticmethod
    def to_int(numeral: str) -> int:
        if not numeral:
            return 0
        for roman_numeral, integer in RomanNumeralConverter.NUMERALS:
            if numeral.startswith(roman_numeral):
                return integer + RomanNumeralConverter.to_int(numeral[len(roman_numeral):])
