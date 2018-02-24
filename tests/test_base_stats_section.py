import unittest

import mwparserfromhell as mw
from bulbascraper.base_stats_section import BaseStatsSection, BaseStatsSubsection
from bulbascraper.base_stats import BaseStats

# Could just parameterize this.
# VOLBEAT_SECTION, then an iterable of the stats.

class TestBaseStatsSectionVolbeat(unittest.TestCase):

    def setUp(self):
        # TODO: Can't seem to get matches='Base stats' ?
        with open('wikimedia/pokemon/Volbeat.wiki') as wikifile:
            wikicode = mw.parse(wikifile.read())
        print(wikicode.get_sections(matches='Base stats', include_headings=False))
        template = wikicode.get_sections(matches='Base stats', include_headings=False)[0]
        self.base_stats_section = BaseStatsSection(template)

    def test_sections(self):
        subsections = list(self.base_stats_section.subsections)

        expected_subsections = [
            BaseStatsSubsection(hit_points=65,
                                attack=73,
                                defence=55,
                                special_attack=47,
                                special_defence=75,
                                speed=85,
                                generations=(3, 6)),
            BaseStatsSubsection(hit_points=65,
                                attack=73,
                                defence=75,
                                special_attack=47,
                                special_defence=85,
                                speed=85,
                                generations=(7, 7))
        ]
        assert subsections == expected_subsections

class TestBaseStatsSectionPidgeot(unittest.TestCase):

    def setUp(self):
        with open('wikimedia/pokemon/Pidgeot.wiki') as wikifile:
            wikicode = mw.parse(wikifile.read())
        print(wikicode.get_sections(matches='Base stats', include_headings=False))
        template = wikicode.get_sections(matches='Base stats', include_headings=False)[0]
        self.base_stats_section = BaseStatsSection(template)

    def test_sections(self):
        subsections = list(self.base_stats_section.subsections)

        expected_subsections = [
            BaseStatsSubsection(hit_points=83,
                                attack=80,
                                defence=75,
                                special_attack=70,
                                special_defence=70,
                                speed=91,
                                special=70,
                                generations=(1, 5)),
            BaseStatsSubsection(hit_points=83,
                                attack=80,
                                defence=75,
                                special_attack=70,
                                special_defence=70,
                                speed=101,
                                generations=(6, None)),
            BaseStatsSubsection(hit_points=83,
                                attack=80,
                                defence=80,
                                special_attack=135,
                                special_defence=80,
                                speed=121,
                                form='Mega Pidgeot')
        ]
        assert subsections == expected_subsections
