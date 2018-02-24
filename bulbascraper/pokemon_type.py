from typing import Optional
from dataclasses import dataclass

@dataclass
class PokemonType(object):
    primary: str
    secondary: Optional[str]
