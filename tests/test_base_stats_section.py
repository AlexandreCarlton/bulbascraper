import textwrap

import mwparserfromhell as mw
import pytest

from bulbascraper.base_stats_section import BaseStatsSection, BaseStatsSubsection
from bulbascraper.base_stats import BaseStats

VOLBEAT_WIKI_STATS = '''
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
VOLBEAT_PARSED_STATS = [
    BaseStatsSubsection(hit_points=65, attack=73, defence=55,
                        special_attack=47, special_defence=75, speed=85,
                        generations=(3, 6)),
    BaseStatsSubsection(hit_points=65, attack=73, defence=75,
                        special_attack=47, special_defence=85, speed=85,
                        generations=(7, 7))
]

PIDGEOT_WIKI_STATS = '''
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
PIDGEOT_PARSED_STATS = [
    BaseStatsSubsection(hit_points=83, attack=80, defence=75,
                        special_attack=70, special_defence=70, speed=91,
                        special=70, generations=(1, 5)),
    BaseStatsSubsection(hit_points=83, attack=80, defence=75,
                        special_attack=70, special_defence=70, speed=101,
                        generations=(6, None)),
    BaseStatsSubsection(hit_points=83, attack=80, defence=80,
                        special_attack=135, special_defence=80, speed=121,
                        form='Mega Pidgeot')
]

# Single base stat section
BULBASAUR_WIKI_STATS = '''
                       ===Stats===
                       ====Base stats====
                       {{Stats
                       |HP=45
                       |Attack=49
                       |Defense=49
                       |SpAtk=65
                       |SpDef=65
                       |Speed=45
                       |Special=65
                       |type=Grass
                       |type2=Poison
                       }}
                       '''
BULBASAUR_PARSED_STATS = [
    BaseStatsSubsection(hit_points=45, attack=49, defence=49,
                        special_attack=65, special_defence=65, speed=45,
                        special=65)
]

@pytest.mark.parametrize("raw_stats,expected_subsections", [
    (VOLBEAT_WIKI_STATS, VOLBEAT_PARSED_STATS),
    (PIDGEOT_WIKI_STATS, PIDGEOT_PARSED_STATS),
    (BULBASAUR_WIKI_STATS, BULBASAUR_PARSED_STATS),
], ids=["Volbeat", "Pidgeot", "Bulbasaur"])
def test_base_stats_section(raw_stats, expected_subsections):
    wikicode = mw.parse(textwrap.dedent(raw_stats))
    template = wikicode.get_sections(matches='Base stats')[0]
    base_stats_section = BaseStatsSection(template)
    subsections = list(base_stats_section.subsections)
    assert subsections == expected_subsections
