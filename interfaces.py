from dice import Die
from abc import ABCMeta, abstractmethod

class Addable(object,metaclass=ABCMeta):
    def __init__(self, score):
        self.score = score

    def __add__(self, x):
        return self.score + x

    def __radd__(self, x):
        return self.score + x

    def __sub__(self, x):
        return self.score - x

    def __rsub__(self, x):
        return self.score - x
    def __gt__(self, x):
        return self.score > x
    def __lt__(self, x):
        return self.score < x
    def __eq__(self, x):
        return self.score == x
    def __ge__(self, x):
        return self.score >= x
    def __le__(self, x):
        return self.score <= x


class Rollable(Addable):
    # TODO #9: make it so that all the reading methods are inside here as static or class methods
    def __init__(self, name, score):
        self.name = name
        super().__init__(score)

    # Remember to fix this and add error handling later
    @classmethod
    def from_tuple(cls, name_score_tuple):
        rollable = cls(name=name_score_tuple[0], score=name_score_tuple[1])
        return rollable

    def __repr__(self):
        msg = f"{self.name}: {self.score}"
        return msg

    def __str__(self):
        msg = f"{self.name.title()}: {self.score}"
        return msg
    
    def points(self):
        return self.score

    def add_points(self, points):
        self.score += points



