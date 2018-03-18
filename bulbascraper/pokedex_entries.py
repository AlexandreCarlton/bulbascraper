
from typing import Optional, Iterator

from dataclasses import dataclass
import mwparserfromhell as mw

# name is Dex/Entry<n>, <n> is the number of games
# there will be a v, v1, v2, ..., v<n> attributes, with the value being the version.
# There is also a 't' attribute. Ignore this, it determiens the colour of the version title text.
# Then there is the entry. That's the actual thing you want.
# E.g.
# {{Dex/Entry2|v=Ruby|v2=Sapphire|t=FFF|t2=FFF|entry=Once Croconaw has clamped its jaws on its foe, it will absolutely not let go. Because the tips of its fangs are forked back like barbed fishhooks, they become impossible to remove when they have sunk in.}}

@dataclass
class PokedexEntry(object):
    version: str
    entry: str
    form: Optional[str] = None

class PokedexEntries(object):

    def __init__(self, section: mw.wikicode.Wikicode) -> None:
        self._section = section

    def __iter__(self) -> Iterator[PokedexEntry]:
        section_without_heading = self._section.get_sections(
            include_headings=False, include_lead=False)[0]
        subsections = section_without_heading.get_sections(include_lead=False)
        if not subsections:
            yield from self._get_entries(self._section.filter_templates())
        else:
            for section in subsections:
                # We may have sections for forms and generations.
                heading = next(section.ifilter_headings())
                templates = section.ifilter_templates()
                entries = self._get_entries(templates)
                for entry in entries:
                    entry.form = str(heading.title)
                    yield entry

    def _get_entries(self, templates: Iterator[mw.nodes.Template]) -> Iterator[PokedexEntry]:
        for template in templates:
            if template.name.startswith('Dex/Entry'):
                wikicode_entry = template.get('entry').value
                entry = self._flatten_templates(wikicode_entry)

                versions = (str(param.value)
                            for param in template.params
                            if param.name.startswith('v'))
                for version in versions:
                    yield PokedexEntry(version=version,
                                       entry=entry)

    @staticmethod
    def _flatten_templates(wikicode: mw.wikicode.Wikicode) -> str:
        string_nodes = []
        for node in wikicode.nodes:
            if isinstance(node, mw.nodes.template.Template):
                if node.name in ('p', 'tt'):
                    string_nodes.append(str(node.get(1)))
            else:
                string_nodes.append(str(node))
        return "".join(string_nodes)
