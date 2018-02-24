import pytest

import mwparserfromhell as mw

from bulbascraper.info_box import InfoBox
from bulbascraper.pokemon_type import PokemonType

# TODO:
# Parameterise this for multiple Pokemon (forms, etc.)

@pytest.fixture(scope='module')
def info_box():
    raw_template = '''{{Pokémon Infobox|
                   name=Bulbasaur |
                   jname=フシギダネ |
                   tmname=Fushigidane |
                   ndex=001 |
                   oldjdex=226 |
                   jdex=231 |
                   hdex=203 |
                   karea=Central |
                   kdex=080 |
                   fbrow=001 |
                   obrow=014 |
                   opbrow=004 |
                   typebox=1 |
                   type1=Grass |
                   type2=Poison |
                   category=Seed |
                   height-ftin=2'04" |
                   height-m=0.7 |
                   weight-lbs=15.2 |
                   weight-kg=6.9 |
                   abilityn=d |
                   ability1=Overgrow |
                   abilityd=Chlorophyll |
                   egggroupn=2 |
                   egggroup1=Monster |
                   egggroup2=Grass |
                   eggcycles=21 |
                   evtotal=1 |
                   evsa=1 |
                   expyield=64 |
                   oldexp=64 |
                   lv100exp=1,059,860 |
                   gendercode=31 |
                   color=Green |
                   catchrate=45 |
                   body=08 |
                   generation=1 |
                   pokefordex=bulbasaur |
                   friendship=70|
                   }}'''
    template = next(mw.parse(raw_template).ifilter_templates())
    return InfoBox(template)

def test_name(info_box):
    assert info_box.name == 'Bulbasaur'

def test_number(info_box):
    assert info_box.number == 1

def test_generation(info_box):
    assert info_box.generation == 1

def test_types(info_box):
    assert info_box.types == {'Bulbasaur': PokemonType('Grass', 'Poison')}

def test_height(info_box):
    assert info_box.height == (2, 4)

def test_weight(info_box):
    assert info_box.weight == 15.2

def test_category(info_box):
    assert info_box.category == 'Seed'

def test_egg_groups(info_box):
    assert list(info_box.egg_groups) == ['Monster', 'Grass']

def test_egg_cycles(info_box):
    assert info_box.egg_cycles == 21
