Things I have

## Goals
Remember, this is meant to be a thin layer above the raw wiki markup.
Some things should be provided (like enumerations of things like Type and
Colour), but apart from that not much else.

Keep things simple, so not much cognitive load is needed to get back in the
swing of things.

## InfoBox

### Forms

`forme=<num>` specifies the number of forms if there is more than one.
`form<n>` is the name of the nth form.
`form1` is sometimes specified, for example:
 - `Standard Mode` for Darmanitan
 - `Geodude` for Geodude
 - absent for Venusaur.

How about, we generate something for each form, and the 'base' form will be the
name of the Pokemon (if it doesn't have a 'base' form like Deoxys' Normal Forme)

### Types
`type<num>` for nth type
`form<n>type<m>` for n >= 2

### Dex numbers

| Key       | Regional Dex  |
| -------   | ------------- |
| `ndex`    | National      |
| `oldjdex` | Johto         |
| `jdex`    | Johto (HG/SS) |
| `hdex`    | Hoenn         |
| `hdex6`   | Hoenn (OR/AS) |
| `sdex`    | Sinnoh        |
| `udex`    | Unova         |
| `u2dex`   | Unova (B2/W2) |
| `kdex`    | Kalos         |
| `adex`    | Alola         |

### Abilities

`abilitycolm`
 - 2 for Venusaur (Mega)?

`abilitylayout`:
 -  2+1 for Venusaur

`abilityn` value includes:
 - `d` for Dreamworld,
 - `m` for mega
 - a number to list them otherwise (e.g. 1 for only one ability).

Megas seem to have one ability.
`ability<num>` Is the nth ability
`abilitym` Is the mega ability
`abilityd` Is the dream world ability


### Effort Values
Only the relevant stats that are non-zero are listed.
The key is `ev<stat>`

| Key  | Stat            |
| ---- | --------------- |
| `hp` | Hit Points      |
| `at` | Attack          |
| `de` | Defence         |
| `sa` | Special Attack  |
| `sa` | Special Defence |
| `sp` | Speed           |

Forms which have different EVs specify the 'ev-'

### Forms

## Base Stats
Normally there is one Base Stats entry.
But if there are forms, or the stats have varied between generations, you can
have sections like (for Pidgeot):

 - Generation I-V
 - Generation VI
 - Mega Pidgeot

So we need to take into account:
 - Generational changes
 - Forms
