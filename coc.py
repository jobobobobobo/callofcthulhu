from dice import dice_pool, dice_roll, d6_pool, Die
from abc import ABCMeta, abstractmethod
from functools import reduce
from math import ceil
from random import sample
import csv

# The damage bonus table can be found on page 33 of the 7th revised edition.
def damage_bonus_table(strength, size):
    key = strength + size
    damage_bonus = 0
    damage_bonus_string = None
    build = 0
    if key >= 165:
        number_d6 = ceil(((key-204)/80)+1)
        damage_bonus_string = f"+{number_d6}d6"
        damage_bonus = dice_roll(d6_pool(number_d6))
        build = number_d6 + 1
    elif key >= 125:
        damage_bonus_string = f"+1d4"
        damage_bonus = dice_roll(dice_pool(1,4))
        build = 1
    elif key >= 85:
        pass
    else:
        damage_bonus = -1 if key >= 65 else -2
        damage_bonus_string = str(damage_bonus)
        build = damage_bonus
    return {'damage-bonus': damage_bonus, 'build': build, 'dice': damage_bonus_string}
# * being able to read in from a skill csv could be extended to read from a characteristics + skill csv

class Addable(object,metaclass=ABCMeta):
    def __init__(self, score):
        self.score = score

    def __add__(self, x):
        return self.score + x

    def __radd__(self, x):
        return self.score + x


class Rollable(Addable,metaclass=ABCMeta):
    # TODO: make it so that all the reading methods are inside here as static or class methods
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

    def check(self, roll, check=self.check):
        if check == True:
            if roll > self.score:
                self.score += Die(6).result

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
    def __init__(self, name, short_name=name[0:3], score=0, check=False, rules=None):
        super().__init__(name, score, check)
        self.short_name = short_name.upper()
    
    def __repr__(self):
        msg = f"{self.short_name}: {self.score}"
        return msg


class Investigator(object):
    
    @staticmethod
    def read_skill_dict(filename="skills.csv"):
        skill_dict = {}
        with open(filename,newline='\n') as csvfile:
            skill_reader = csv.reader(csvfile,delimiter=',',quotechar='|')
            for row in skill_reader:
                name = row[0]
                skill = Skill(name,int(row[1]),rules=row[2])
                skill_dict.update({name : skill})
        return skill_dict

    def stat_dictionary(self):
        return {
            "STR": self.strength,
            "CON": self.constitution,
            "POW": self.power,
            "DEX": self.dexterity,
            "APP": self.appearance,
            "INT": self.intelligence,
            "SIZ": self.size,
            "EDU": self.education,
        }

    def raise_skill(self, skill_name, points):
        self.skill_dict[skill_name].add_points(points)

    def get_points(self, skill_name):
        ret = self.skill_dict[skill_name].points()
        return ret

    def apply_age_penalty(self, strength, constitution, size, dexterity, appearance, intelligence, power, education, luck):
        if self.age >= 80:
            self.strength = strength

    # TODO: implement the age penalty. more complicated than I thought
    # TODO: make a new constructor for Skills and Characteristics to pull from a tuple like (Skill_name, score).
    # XXX: Characteristic could derive the short_name from the first 3 letters of the name
    # XXX: that will make it easier to implement rule packs and the csvs

    @classmethod
    def generate_random(cls, name,skill_dict):
        # RULES: STR, CON, POW, DEX, APP are all 3d6
        # RULES: INT and SIZ are 2d6 + 6
        # RULES: EDU is 2d6+6
        # RULES: under 7th edition rules I multiply them by 5
        # RULES: under the laundry files age is 17 + 2d6, but we are hard coding 7e for now

        age = sample(range(15,90),1)       
        character = cls(
            name=name,
            strength=Characteristic("Strength", "STR", dice_roll(d6_pool(3)) * 5),
            constitution=Characteristic("Constitution", "CON", dice_roll(d6_pool(3)) * 5),
            size=Characteristic("Size", "SIZ", dice_roll(d6_pool(2),6) * 5),
            dexterity=Characteristic("Dexterity", "DEX", dice_roll(d6_pool(3)) * 5),
            appearance=Characteristic("Appearance", "APP", dice_roll(d6_pool(3)) * 5),
            intelligence=Characteristic("Intelligence", "INT", dice_roll(d6_pool(2),6) * 5),
            power=Characteristic("Power", "POW", dice_roll(d6_pool(3)) * 5),
            education=Characteristic("Education", "EDU", dice_roll(d6_pool(2),6) * 5),
            luck=Characteristic("Luck", "LUK", dice_roll(d6_pool(3)) * 5),
            age=age,
            skill_dict=skill_dict,
        )
        character.apply_age_penalty(age)


        return character


    def __init__(
        self,
        name,
        strength: Characteristic,
        constitution: Characteristic,
        power: Characteristic,
        dexterity: Characteristic,
        appearance: Characteristic,
        intelligence: Characteristic,
        size: Characteristic,
        education: Characteristic,
        luck: Characteristic,
        age,
        skill_dict,
    ):
        self.name = name
        # STR, CON, POW, DEX, APP are all 3d6
        self.strength = strength
        self.constitution = constitution
        self.power = power
        self.dexterity = dexterity
        self.appearance = appearance
        self.luck = luck

        # INT and SIZ are 2d6 + 6
        self.intelligence = intelligence
        self.size = size

        # EDU is 3d6+3
        self.education = education
        # Age is 17+2d6, but has a minimum of EDU + 5
        self.age = age

        # Derived stats
        self.damage_bonus = self.damage_bonus_table()
        self.max_hp = ceil((self.constitution + self.size) / 2)
        self.current_hp = self.max_hp
        self.wound_threshold = ceil(self.max_hp / 2)
        self.xp_bonus = ceil(self.intelligence / 2)

        # Skills
        self.skill_dict = skill_dict

    def damage_roll(self, weapon_damage):
        damage_bonus = damage_bonus_table(self.strength, self.size)
        return weapon_damage + damage_bonus['damage-bonus']

    def __repr__(self):
        msg = (
            f"Name: {self.name}\n Age: {self.age:>2}\n"
            f" STR: {self.strength:>2} | INT: {self.intelligence:>2}\n"
            f" CON: {self.constitution:>2} | POW: {self.power:>2}\n"
            f" DEX: {self.dexterity:>2} | APP: {self.appearance:>2}\n"
            f" SIZ: {self.size:>2} | EDU: {self.education:>2}\n"
            f"  HP: {self.current_hp}/{self.max_hp}"
        )
        for key in self.skill_dict:
            msg += "\n" + str(self.skill_dict[key])
        return msg

    def skill_roll(self, skill_name):
        skill = self.skill_dict[skill_name]
        return skill.roll()
# TODO: refactor this to be a subclass of Skill, to use the improvement check method.


if __name__ == "__main__":
    print("Welcome to the Call of Cthulhu character generator.")
    name = input("Please provide a name for your character: ")
    skill_dict = Investigator.read_skill_dict()
    # Now we will start creating a character.
    stat_block = {
        "STR" : Characteristic("Strength", "STR", dice_roll(d6_pool(3)) * 5),
        "CON" : Characteristic("Constitution", "CON", dice_roll(d6_pool(3)) * 5),
        "SIZ" : Characteristic("Size", "SIZ", dice_roll(d6_pool(2),6) * 5),
        "DEX" : Characteristic("Dexterity", "DEX", dice_roll(d6_pool(3)) * 5),
        "APP" : Characteristic("Appearance", "APP", dice_roll(d6_pool(3)) * 5),
        "INT" : Characteristic("Intelligence", "INT", dice_roll(d6_pool(2),6) * 5),
        "POW" : Characteristic("Power", "POW", dice_roll(d6_pool(3)) * 5),
        "EDU" : Characteristic("Education", "EDU", dice_roll(d6_pool(2),6) * 5),
        "LUK" : Characteristic("Luck", "LUK", dice_roll(d6_pool(3)) * 5)
    }
    print("I have generated your stats in the background for now.")
    age = input("Please enter an age for your investigator: ")
    # TODO: age has different effects - see pg 32 of 7e revised
    print("Thank you. This will have an effect on your investigator later on.")
    max_hp = math.floor((stat_block['CON'] + stat_block['SIZ'])/10)
    movement_rate = 0
    # TODO: movement rate rules on page 33 of 7th edition revised

    # TODO: Determine Occupation
    # TODO: Decide skills & allocate points
    # TODO: Create a backstory
    # TODO: Equip investigator