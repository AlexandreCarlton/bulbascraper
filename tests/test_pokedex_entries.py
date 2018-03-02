import textwrap

import mwparserfromhell as mw
import pytest

from bulbascraper.pokedex_entries import PokedexEntries, PokedexEntry

# Raticate has multiple forms, which have different entries associated with them.
RATICATE_WIKI_ENTRIES = '''
===Pokédex entries===
====Raticate====
{{Dex/Header|type=Normal}}
{{Dex/Gen|gen=I}}
{{Dex/Entry2|v=Red|v2=Blue|t2=FFF|entry=It uses its whiskers to maintain its balance. It apparently slows down if they are cut off.}}
{{Dex/Entry1|v=Yellow|entry=Its hind feet are webbed. They act as flippers, so it can swim in rivers and hunt for prey.}}
{{Dex/Entry1|v=Stadium|t=FFF|color=000|entry=If attacked, it stands up on its hind legs, bares its fangs and shrieks in an intimidating manner at its enemy.}}
|}
|}
{{Dex/Gen|gen=II}}
{{Dex/Entry1|v=Gold|entry=Gnaws on anything with its tough fangs. It can even topple concrete buildings by gnawing on them.}}
{{Dex/Entry1|v=Silver|entry=Its whiskers help it to maintain balance. Its fangs never stop growing, so it gnaws to pare them down.}}
{{Dex/Entry1|v=Crystal|entry=The webs on its hind legs enable it to cross rivers. It searches wide areas for food.}}
{{Dex/Entry1|v=Stadium 2|t=FFF|color=000|entry=Gnaws on anything with its tough fangs. It can even topple concrete buildings by gnawing on them.}}
|}
|}
{{Dex/Gen|gen=III}}
{{Dex/Entry2|v=Ruby|v2=Sapphire|t=FFF|t2=FFF|entry=Raticate's sturdy fangs grow steadily. To keep them ground down, it gnaws on rocks and logs. It may even chew on the walls of houses.}}
{{Dex/Entry1|v=Emerald|t=FFF|entry=A Raticate's sturdy fangs grow steadily. To keep them ground down, it gnaws on rocks and logs. It may even chew on the walls of houses.}}
{{Dex/Entry1|v=FireRed|entry=Its rear feet have three toes each. They are webbed, enabling it to swim across rivers.}}
{{Dex/Entry1|v=LeafGreen|entry=It uses its whiskers to maintain its balance. It apparently slows down if they are cut off.}}
|}
|}
{{Dex/Gen|gen=IV}}
{{Dex/Entry3|v=Diamond|v2=Pearl|v3=Platinum|entry=It whittles its constantly growing fangs by gnawing on hard things. It can chew apart cinder walls.}}
{{Dex/Entry1|v=HeartGold|entry=Gnaws on anything with its tough fangs. It can even topple concrete buildings by gnawing on them.}}
{{Dex/Entry1|v=SoulSilver|entry=Its whiskers help it to maintain balance. Its fangs never stop growing, so it gnaws to pare them down.}}
|}
|}
{{Dex/Gen|gen=V}}
{{Dex/Entry2|v=Black|v2=White|t=FFF|entry=It whittles its constantly growing fangs by gnawing on hard things. It can chew apart cinder walls.}}
{{Dex/Entry2|v=Black 2|v2=White 2|t=FFF|entry=With its long fangs, this surprisingly violent Pokémon can gnaw away even thick concrete with ease.}}
|}
|}
{{Dex/Gen|gen=VI}}
{{Dex/Entry1|v=X|t=FFF|entry=It whittles its constantly growing fangs by gnawing on hard things. It can chew apart cinder walls.}}
{{Dex/Entry1|v=Y|entry=The webs on its hind legs enable it to cross rivers. It searches wide areas for food.}}
{{Dex/Entry2|v=Omega Ruby|v2=Alpha Sapphire|t=FFF|t2=FFF|entry=Raticate’s sturdy fangs grow steadily. To keep them ground down, it gnaws on rocks and logs. It may even chew on the walls of houses.}}
|}
|}
{{Dex/Gen|gen=VII}}
{{Dex/Entry1|v=Sun|entry=Its hind feet are webbed, so it's a strong swimmer. It can cross rivers and sometimes even oceans.}}
{{Dex/Entry1|v=Moon|entry=Its disposition is far more violent than its looks would suggest. Don't let your hand get too close to its face, as it could bite your hand clean off.}}
{{Dex/Entry1|v=Ultra Sun|entry=People say that it fled from its enemies by using its small webbed hind feet to swim from island to island in Alola.}}
{{Dex/Entry1|v=Ultra Moon|entry=Its whiskers are essential for maintaining its balance. No matter how friendly you are, it will get angry and bite you if you touch its whiskers.}}
|}
|}
{{Dex/Footer}}

====Alolan Raticate====
{{Dex/Header|type=Dark|type2=Normal}}
{{Dex/NA|gen=VII}}
{{Dex/Gen|gen=VII}}
{{Dex/Entry1|v=Sun|entry=It forms a group of Rattata, which it assumes command of. Each group has its own territory, and disputes over food happen often.}}
{{Dex/Entry1|v=Moon|entry=This gourmet Pokémon is particular about the taste and freshness of its food. Restaurants where Raticate live have a good reputation.}}
{{Dex/Entry1|v=Ultra Sun|entry=It has an incredibly greedy personality. Its nest is filled with so much food gathered by Rattata at its direction, it can't possibly eat it all.}}
{{Dex/Entry1|v=Ultra Moon|entry=It commands a nest of Rattata. Different nests don't get along, whipping up severe fights over feeding grounds.}}
|}
|}
{{Dex/Footer}}
'''

RATICATE_PARSED_ENTRIES = [
    PokedexEntry(form='Raticate', version='Red',            entry='It uses its whiskers to maintain its balance. It apparently slows down if they are cut off.'),
    PokedexEntry(form='Raticate', version='Blue',           entry='It uses its whiskers to maintain its balance. It apparently slows down if they are cut off.'),
    PokedexEntry(form='Raticate', version='Yellow',         entry='Its hind feet are webbed. They act as flippers, so it can swim in rivers and hunt for prey.'),
    PokedexEntry(form='Raticate', version='Stadium',        entry='If attacked, it stands up on its hind legs, bares its fangs and shrieks in an intimidating manner at its enemy.'),
    PokedexEntry(form='Raticate', version='Gold',           entry='Gnaws on anything with its tough fangs. It can even topple concrete buildings by gnawing on them.'),
    PokedexEntry(form='Raticate', version='Silver',         entry='Its whiskers help it to maintain balance. Its fangs never stop growing, so it gnaws to pare them down.'),
    PokedexEntry(form='Raticate', version='Crystal',        entry='The webs on its hind legs enable it to cross rivers. It searches wide areas for food.'),
    PokedexEntry(form='Raticate', version='Stadium 2',      entry='Gnaws on anything with its tough fangs. It can even topple concrete buildings by gnawing on them.'),
    PokedexEntry(form='Raticate', version='Ruby',           entry='Raticate\'s sturdy fangs grow steadily. To keep them ground down, it gnaws on rocks and logs. It may even chew on the walls of houses.'),
    PokedexEntry(form='Raticate', version='Sapphire',       entry='Raticate\'s sturdy fangs grow steadily. To keep them ground down, it gnaws on rocks and logs. It may even chew on the walls of houses.'),
    PokedexEntry(form='Raticate', version='Emerald',        entry='A Raticate\'s sturdy fangs grow steadily. To keep them ground down, it gnaws on rocks and logs. It may even chew on the walls of houses.'),
    PokedexEntry(form='Raticate', version='FireRed',        entry='Its rear feet have three toes each. They are webbed, enabling it to swim across rivers.'),
    PokedexEntry(form='Raticate', version='LeafGreen',      entry='It uses its whiskers to maintain its balance. It apparently slows down if they are cut off.'),
    PokedexEntry(form='Raticate', version='Diamond',        entry='It whittles its constantly growing fangs by gnawing on hard things. It can chew apart cinder walls.'),
    PokedexEntry(form='Raticate', version='Pearl',          entry='It whittles its constantly growing fangs by gnawing on hard things. It can chew apart cinder walls.'),
    PokedexEntry(form='Raticate', version='Platinum',       entry='It whittles its constantly growing fangs by gnawing on hard things. It can chew apart cinder walls.'),
    PokedexEntry(form='Raticate', version='HeartGold',      entry='Gnaws on anything with its tough fangs. It can even topple concrete buildings by gnawing on them.'),
    PokedexEntry(form='Raticate', version='SoulSilver',     entry='Its whiskers help it to maintain balance. Its fangs never stop growing, so it gnaws to pare them down.'),
    PokedexEntry(form='Raticate', version='Black',          entry='It whittles its constantly growing fangs by gnawing on hard things. It can chew apart cinder walls.'),
    PokedexEntry(form='Raticate', version='White',          entry='It whittles its constantly growing fangs by gnawing on hard things. It can chew apart cinder walls.'),
    PokedexEntry(form='Raticate', version='Black 2',        entry='With its long fangs, this surprisingly violent Pokémon can gnaw away even thick concrete with ease.'),
    PokedexEntry(form='Raticate', version='White 2',        entry='With its long fangs, this surprisingly violent Pokémon can gnaw away even thick concrete with ease.'),
    PokedexEntry(form='Raticate', version='X',              entry='It whittles its constantly growing fangs by gnawing on hard things. It can chew apart cinder walls.'),
    PokedexEntry(form='Raticate', version='Y',              entry='The webs on its hind legs enable it to cross rivers. It searches wide areas for food.'),
    PokedexEntry(form='Raticate', version='Omega Ruby',     entry='Raticate’s sturdy fangs grow steadily. To keep them ground down, it gnaws on rocks and logs. It may even chew on the walls of houses.'),
    PokedexEntry(form='Raticate', version='Alpha Sapphire', entry='Raticate’s sturdy fangs grow steadily. To keep them ground down, it gnaws on rocks and logs. It may even chew on the walls of houses.'),
    PokedexEntry(form='Raticate', version='Sun',            entry='Its hind feet are webbed, so it\'s a strong swimmer. It can cross rivers and sometimes even oceans.'),
    PokedexEntry(form='Raticate', version='Moon',           entry='Its disposition is far more violent than its looks would suggest. Don\'t let your hand get too close to its face, as it could bite your hand clean off.'),
    PokedexEntry(form='Raticate', version='Ultra Sun',      entry='People say that it fled from its enemies by using its small webbed hind feet to swim from island to island in Alola.'),
    PokedexEntry(form='Raticate', version='Ultra Moon',     entry='Its whiskers are essential for maintaining its balance. No matter how friendly you are, it will get angry and bite you if you touch its whiskers.'),

    PokedexEntry(form='Alolan Raticate', version='Sun',        entry='It forms a group of Rattata, which it assumes command of. Each group has its own territory, and disputes over food happen often.'),
    PokedexEntry(form='Alolan Raticate', version='Moon',       entry='This gourmet Pokémon is particular about the taste and freshness of its food. Restaurants where Raticate live have a good reputation.'),
    PokedexEntry(form='Alolan Raticate', version='Ultra Sun',  entry='It has an incredibly greedy personality. Its nest is filled with so much food gathered by Rattata at its direction, it can\'t possibly eat it all.'),
    PokedexEntry(form='Alolan Raticate', version='Ultra Moon', entry='It commands a nest of Rattata. Different nests don\'t get along, whipping up severe fights over feeding grounds.')
]

CATERPIE_WIKI_ENTRIES = '''
===Pokédex entries===
{{Dex/Header|type=Bug}}
{{Dex/Gen|gen=I}}
{{Dex/Entry2|v=Red|v2=Blue|t2=FFF|entry=Its short feet are tipped with suction pads that enable it to tirelessly climb slopes and walls.}}
{{Dex/Entry1|v=Yellow|entry=If you touch the feeler on top of its head, it will release a horrible stink to protect itself.}}
{{Dex/Entry1|v=Stadium|t=FFF|color=000|entry=It has large, eye-like patterns on its head as protection. They are used to frighten off enemies.}}
|}
|}
{{Dex/Gen|gen=II}}
{{Dex/Entry1|v=Gold|entry=For protection, it releases a horrible stench from the antennae on its head to drive away enemies.}}
{{Dex/Entry1|v=Silver|entry=Its feet have suction cups designed to stick to any surface. It tenaciously climbs trees to forage.}}
{{Dex/Entry1|v=Crystal|entry=It crawls into foliage where it camouflages itself among leaves that are the same color as its body.}}
{{Dex/Entry1|v=Stadium 2|t=FFF|color=000|entry=For protection, it releases a horrible stench from the antennae on its head to drive away enemies.}}
|}
|}
{{Dex/Gen|gen=III}}
{{Dex/Entry2|v=Ruby|v2=Sapphire|t=FFF|t2=FFF|entry=Caterpie has a voracious appetite. It can devour leaves bigger than its body right before your eyes. From its antenna, this Pokémon releases a terrifically strong odor.}}
{{Dex/Entry1|v=Emerald|t=FFF|entry=Its voracious appetite compels it to devour leaves bigger than itself without hesitation. It releases a terribly strong odor from its antennae.}}
{{Dex/Entry1|v=FireRed|entry=It is covered with a green skin. When it grows, it sheds the skin, covers itself with silk, and becomes a cocoon.}}
{{Dex/Entry1|v=LeafGreen|entry=Its short feet are tipped with suction pads that enable it to tirelessly climb slopes and walls.}}
|}
|}
{{Dex/Gen|gen=IV}}
{{Dex/Entry3|v=Diamond|v2=Pearl|v3=Platinum|entry=It releases a stench from its red antenna to repel enemies. It grows by molting repeatedly.}}
{{Dex/Entry1|v=HeartGold|entry=For protection, it releases a horrible stench from the antennae on its head to drive away enemies.}}
{{Dex/Entry1|v=SoulSilver|entry=Its feet have suction cups designed to stick to any surface. It tenaciously climbs trees to forage.}}
|}
|}
{{Dex/Gen|gen=V}}
{{Dex/Entry2|v=Black|v2=White|t=FFF|entry=It releases a stench from its red antenna to repel enemies. It grows by molting repeatedly.}}
{{Dex/Entry2|v=Black 2|v2=White 2|t=FFF|entry=It releases a stench from its red antenna to repel enemies. It grows by molting repeatedly.}}
|}
|}
{{Dex/Gen|gen=VI}}
{{Dex/Entry1|v=X|t=FFF|entry=For protection, it releases a horrible stench from the antennae on its head to drive away enemies.}}
{{Dex/Entry1|v=Y|entry=Its feet have suction cups designed to stick to any surface. It tenaciously climbs trees to forage.}}
{{Dex/Entry2|v=Omega Ruby|v2=Alpha Sapphire|t=FFF|t2=FFF|entry=Caterpie has a voracious appetite. It can devour leaves bigger than its body right before your eyes. From its antenna, this Pokémon releases a terrifically strong odor.}}
|}
|}
{{Dex/Gen|gen=VII}}
{{Dex/Entry1|v=Sun|entry=When attacked by bird Pokémon, it resists by releasing a terrifically strong odor from its antennae, but it often becomes their prey.}}
{{Dex/Entry1|v=Moon|entry=It's easy to catch, and it grows quickly, making it one of the top recommendations for novice Pokémon Trainers.}}
{{Dex/Entry1|v=Ultra Sun|entry=Perhaps because it would like to grow up quickly, it has a voracious appetite, eating a hundred leaves a day.}}
{{Dex/Entry1|v=Ultra Moon|entry=Its body is soft and weak. In nature, its perpetual fate is to be seen by others as food.}}
|}
|}
{{Dex/Footer}}
'''

CATERPIE_PARSED_ENTRIES = [
    PokedexEntry(version='Red', entry='Its short feet are tipped with suction pads that enable it to tirelessly climb slopes and walls.'),
    PokedexEntry(version='Blue', entry='Its short feet are tipped with suction pads that enable it to tirelessly climb slopes and walls.'),
    PokedexEntry(version='Yellow', entry='If you touch the feeler on top of its head, it will release a horrible stink to protect itself.'),
    PokedexEntry(version='Stadium', entry='It has large, eye-like patterns on its head as protection. They are used to frighten off enemies.'),
    PokedexEntry(version='Gold', entry='For protection, it releases a horrible stench from the antennae on its head to drive away enemies.'),
    PokedexEntry(version='Silver', entry='Its feet have suction cups designed to stick to any surface. It tenaciously climbs trees to forage.'),
    PokedexEntry(version='Crystal', entry='It crawls into foliage where it camouflages itself among leaves that are the same color as its body.'),
    PokedexEntry(version='Stadium 2', entry='For protection, it releases a horrible stench from the antennae on its head to drive away enemies.'),
    PokedexEntry(version='Ruby', entry='Caterpie has a voracious appetite. It can devour leaves bigger than its body right before your eyes. From its antenna, this Pokémon releases a terrifically strong odor.'),
    PokedexEntry(version='Sapphire', entry='Caterpie has a voracious appetite. It can devour leaves bigger than its body right before your eyes. From its antenna, this Pokémon releases a terrifically strong odor.'),
    PokedexEntry(version='Emerald', entry='Its voracious appetite compels it to devour leaves bigger than itself without hesitation. It releases a terribly strong odor from its antennae.'),
    PokedexEntry(version='FireRed', entry='It is covered with a green skin. When it grows, it sheds the skin, covers itself with silk, and becomes a cocoon.'),
    PokedexEntry(version='LeafGreen', entry='Its short feet are tipped with suction pads that enable it to tirelessly climb slopes and walls.'),
    PokedexEntry(version='Diamond', entry='It releases a stench from its red antenna to repel enemies. It grows by molting repeatedly.'),
    PokedexEntry(version='Pearl', entry='It releases a stench from its red antenna to repel enemies. It grows by molting repeatedly.'),
    PokedexEntry(version='Platinum', entry='It releases a stench from its red antenna to repel enemies. It grows by molting repeatedly.'),
    PokedexEntry(version='HeartGold', entry='For protection, it releases a horrible stench from the antennae on its head to drive away enemies.'),
    PokedexEntry(version='SoulSilver', entry='Its feet have suction cups designed to stick to any surface. It tenaciously climbs trees to forage.'),
    PokedexEntry(version='Black', entry='It releases a stench from its red antenna to repel enemies. It grows by molting repeatedly.'),
    PokedexEntry(version='White', entry='It releases a stench from its red antenna to repel enemies. It grows by molting repeatedly.'),
    PokedexEntry(version='Black 2', entry='It releases a stench from its red antenna to repel enemies. It grows by molting repeatedly.'),
    PokedexEntry(version='White 2', entry='It releases a stench from its red antenna to repel enemies. It grows by molting repeatedly.'),
    PokedexEntry(version='X', entry='For protection, it releases a horrible stench from the antennae on its head to drive away enemies.'),
    PokedexEntry(version='Y', entry='Its feet have suction cups designed to stick to any surface. It tenaciously climbs trees to forage.'),
    PokedexEntry(version='Omega Ruby', entry='Caterpie has a voracious appetite. It can devour leaves bigger than its body right before your eyes. From its antenna, this Pokémon releases a terrifically strong odor.'),
    PokedexEntry(version='Alpha Sapphire', entry='Caterpie has a voracious appetite. It can devour leaves bigger than its body right before your eyes. From its antenna, this Pokémon releases a terrifically strong odor.'),
    PokedexEntry(version='Sun', entry='When attacked by bird Pokémon, it resists by releasing a terrifically strong odor from its antennae, but it often becomes their prey.'),
    PokedexEntry(version='Moon', entry='It\'s easy to catch, and it grows quickly, making it one of the top recommendations for novice Pokémon Trainers.'),
    PokedexEntry(version='Ultra Sun', entry='Perhaps because it would like to grow up quickly, it has a voracious appetite, eating a hundred leaves a day.'),
    PokedexEntry(version='Ultra Moon', entry='Its body is soft and weak. In nature, its perpetual fate is to be seen by others as food.'),
]


@pytest.mark.parametrize("raw_entries,expected_entries", [
    (RATICATE_WIKI_ENTRIES, RATICATE_PARSED_ENTRIES),
    (CATERPIE_WIKI_ENTRIES, CATERPIE_PARSED_ENTRIES),
], ids=['Raticate', 'Caterpie'])
def test_base_stats_section(raw_entries, expected_entries):
    wikicode = mw.parse(textwrap.dedent(raw_entries))
    section = wikicode.get_sections(matches='Pokédex entries', include_headings=False)[0]
    pokedex_entries = PokedexEntries(section)
    entries = list(pokedex_entries)
    assert entries == expected_entries
