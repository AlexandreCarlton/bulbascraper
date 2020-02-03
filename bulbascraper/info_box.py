from typing import Dict, Iterator, Optional, Tuple

from dataclasses import dataclass
import mwparserfromhell as mw

from bulbascraper.ev_yield import EVYield
from bulbascraper.pokemon_type import PokemonType

@dataclass
class ImageFilename(object):
    form: str
    filename: str

# Contains info for all forms
# Spec: https://bulbapedia.bulbagarden.net/wiki/Template_talk:Pok%C3%A9mon_Infobox
class InfoBox(object):

    '''Provides a way to extract information from a box.
    Designed to be as thin as possible.'''

    def __init__(self, template: mw.nodes.template.Template) -> None:
        self._template = template

    def _get(self, name, default=None):
        if self._template.has(name):
            # Call .get(0) so that we extract the first item
            # (there might be comments in there - See Floette's AZ form).
            return self._template.get(name).value.get(0).strip()
        return default

    @property
    def name(self) -> str:
        return self._get('name')

    @property
    def number(self) -> int:
        return int(self._get('ndex'))

    @property
    def _num_forms(self):
        return int(self._get('forme', '1'))

    @property
    def forms(self) -> Iterator[str]:
        for i in range(1, self._num_forms + 1):
            # Mega forms don't list form1, which is just the original one.
            form = self._get('form{}'.format(i), self.name)
            yield form

    @property
    def images(self) -> Iterator[ImageFilename]:
        forms = {i: form for i, form in enumerate(self.forms, 1)}
        default_filename = "{:03}{}.png".format(self.number, self.name)
        yield ImageFilename(form=forms[1],
                            filename=self._get('image', default_filename))
        for i in range(2, self._num_forms + 1):
            yield ImageFilename(form=forms[i],
                                filename=self._get('image{}'.format(i)))

    @property
    def generation(self) -> int:
        return int(self._get('generation'))

    @property
    def category(self) -> str:
        return self._get('category')

    @property
    def types(self) -> Dict[str, PokemonType]:
        types = {}
        default_typing = PokemonType(self._get('type1'), self._get('type2'))
        for i, form in enumerate(self.forms, 1):
            type1 = self._get(f'form{i}type1')
            type2 = self._get(f'form{i}type2')
            if type1 is not None:
                types[form] = PokemonType(type1, type2)
            else:
                types[form] = default_typing
        return types

    @property
    def height(self) -> Tuple[int, int]:
        raw_height = self._get('height-ftin')
        feet, inches = map(float, raw_height.rstrip('"').split("'"))
        return feet, inches

    @property
    def weight(self) -> float:
        return float(self._get('weight-lbs'))

    # Make an enum from colour?
    @property
    def colour(self) -> str:
        return self._get('color')

    @property
    def egg_groups(self) -> Iterator[str]:
        num_groups = int(self._get('egggroupn'))
        for i in range(1, num_groups+1):
            egg_group = self._get('egggroup{}'.format(i))
            yield egg_group

    @property
    def egg_cycles(self) -> int:
        return int(self._get('eggcycles'))

    @property
    def experience_yield(self) -> int:
        return 0


    @property
    def effort_values(self) -> EVYield:
        # TODO: Different forms have 'evhp2', 'evat3', etc.
        return EVYield(hp=int(self._get('evhp', '0')),
                       attack=int(self._get('evat', '0')),
                       defense=int(self._get('evde', '0')),
                       special_attack=int(self._get('evsa', '0')),
                       special_defence=int(self._get('evsd', '0')),
                       speed=int(self._get('evsp', '0')))
