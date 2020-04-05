from dice import Die

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
    def __init__(self, name, score, check):
        self.name = name
        super().__init__(score)
        self.check = check

    # Remember to fix this and add error handling later
    @classmethod
    def from_tuple(cls, name_score_tuple):
        rollable = cls(name=name_score_tuple[0], score=name_score_tuple[1])
        return rollable

    def __repr__(self):
        box = "\u25a1"
        checked = "\u2611"
        msg = f"{self.name}: {self.score}"
        return msg

    def __str__(self):
        box = "\u25a1"
        checked = "\u2611"
        msg = f"{box if self.check is False else checked} {self.name.title()}: {self.score}"
        return msg
    
    def points(self):
        return self.score

    def skill_improvement(self, check=True, roll=Die(100).result):
        if check == True:
            if roll > self.score:
                self.score += Die(6)

    def roll(self):
        result = Die(100).result
        outcome = True if (result <= self.score) else False
        if outcome is True:
            self.check = True
        return {"outcome": outcome, "result": result}

    def add_points(self, points):
        self.score += points

class Skill(Rollable):
    def __init__(self, name, score, check=False, rules=None, important=False):
        super().__init__(name, score, check)
        self.rules = rules
        self.important = important 

    @classmethod
    def from_tuple(cls, name_score_tuple):
        skill = super().from_tuple(name_score_tuple)
        return skill

class Characteristic(Rollable):
    def __init__(self, name, short_name=None, score=0, check=False, rules=None):
        if short_name == None:
           self.short_name = name[0:3]
        super().__init__(name, score, check)
        self.short_name = short_name.upper()
    
    def __str__(self):
        msg = f"{self.short_name}: {self.score:>2}"
        return msg
    def __repr__(self):
        msg = f"{self.short_name}: {self.score:>2}"
        return msg

