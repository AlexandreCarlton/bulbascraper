import textwrap
import unittest

import mwparserfromhell as mw
from bulbascraper.base_stats_section import BaseStatsSection, BaseStatsSubsection
from bulbascraper.base_stats import BaseStats

# Could just parameterize this.
# VOLBEAT_SECTION, then an iterable of the stats.

class TestBaseStatsSectionVolbeat(unittest.TestCase):

    VOLBEAT_STATS = '''
                    ===Stats===
                    ====Base stats====
                    =====Generation III-VI=====
                    {{BaseStats
                    |type=Bug
                    |HP=     65
                    |Attack= 73
                    |Defense=55
                    |SpAtk=  47
                    |SpDef=  75
                    |Speed=  85}}

                    =====Generation VII=====
                    {{BaseStats
                    |type=Bug
                    |HP=     65
                    |Attack= 73
                    |Defense=75
                    |SpAtk=  47
                    |SpDef=  85
                    |Speed=  85}}

                    ====Pokéathlon stats====
                    {{Pokéthlon
                    |type=Bug
                    |Speed=3
                    |SpeedMax=4
                    |Power=3
                    |PowerMax=3
                    |Technique=2
                    |TechniqueMax=2
                    |Stamina=2
                    |StaminaMax=3
                    |Jump=5
                    |JumpMax=5
                    }}
                    '''

    def setUp(self):
        # mwparserfromhell doesn't like indentations between parameter entries.
        wikicode = mw.parse(textwrap.dedent(self.VOLBEAT_STATS))
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

    PIDGEOT_STATS = '''
                    ===Stats===
                    ====Base stats====
                    =====Generation I-V=====
                    {{BaseStats with RBY
                    |type=Normal
                    |type2=Flying
                    |HP=     83
                    |Attack= 80
                    |Defense=75
                    |SpAtk=  70
                    |SpDef=  70
                    |Special=70
                    |Speed=  91 }}

                    =====Generation VI onward=====
                    {{BaseStats
                    |type=Normal
                    |type2=Flying
                    |HP=     83
                    |Attack= 80
                    |Defense=75
                    |SpAtk=  70
                    |SpDef=  70
                    |Speed=  101 }}

                    =====Mega Pidgeot=====
                    {{Base Stats
                    |type=Normal
                    |type2=Flying
                    |HP=83
                    |Attack=80
                    |Defense=80
                    |SpAtk=135
                    |SpDef=80
                    |Speed=121 }}
                    '''

    def setUp(self):
        wikicode = mw.parse(textwrap.dedent(self.PIDGEOT_STATS))
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
