
# TODO: Replace with dataclass in Python 3.7

class EVYield(object):

    def __init__(self,
                 hp: int=0,
                 attack: int=0,
                 defense: int=0,
                 special_attack: int=0,
                 special_defence: int=0,
                 speed: int=0):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defence = special_defence
        self.speed = speed

    def total(self):
        return (self.hp +
                self.attack +
                self.defense +
                self.special_attack +
                self.special_defence +
                self.speed)
