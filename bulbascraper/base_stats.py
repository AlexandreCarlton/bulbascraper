from dataclasses import dataclass

@dataclass
class BaseStats(object):
    hit_points: int
    attack: int
    defence: int
    special_attack: int
    special_defence: int
    speed: int

@dataclass
class BaseStatsRBY(object):
    hit_points: int
    attack: int
    defence: int
    special: int
    speed: int
