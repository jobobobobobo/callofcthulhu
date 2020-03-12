from dice import dice_pool, dice_roll, d6_pool, Die
from functools import reduce
from math import ceil
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

class Skill(object):
    def __init__(self, name, score, check=False, rules=None, important=False):
        self.name = name
        self.score = score
        self.check = check
        self.rules = rules
        self.important = important

    def points(self):
        return self.score

    def check(self, roll):
        if check == True:
            if roll > score:
                self.score += Die(6).result

    def roll(self):
        result = Die(100).result
        outcome = True if (result <= self.score) else False
        if outcome is True:
            self.check = True
        return {"outcome": outcome, "result": result}

    def add_points(self, points):
        self.score += points

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


class HumanCharacter(object):
    
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
            "CHA": self.charisma,
            "INT": self.intelligence,
            "SIZ": self.size,
            "EDU": self.education,
        }

    def raise_skill(self, skill_name, points):
        self.skill_dict[skill_name].add_points(points)

    def get_points(self, skill_name):
        ret = self.skill_dict[skill_name].points()
        return ret

    @classmethod
    def generate_random(cls, name,skill_dict):
        # TODO: update this to 7th edition rules!!!
        # STR, CON, POW, DEX, CHA are all 3d6
        strength = dice_roll(d6_pool(3))
        constitution = dice_roll(d6_pool(3))
        power = dice_roll(d6_pool(3))
        dexterity = dice_roll(d6_pool(3))
        charisma = dice_roll(d6_pool(3))

        # INT and SIZ are 2d6 + 6
        intelligence = dice_roll(d6_pool(2), 6)
        size = dice_roll(d6_pool(2), 6)

        # EDU is 3d6+3
        education = dice_roll(d6_pool(3), 3)
        # Age is 17+2d6, but has a minimum of EDU + 5
        age = dice_roll(d6_pool(2), 17)
        age = age if age >= (education + 5) else (education + 5)

        character = cls(
            name,
            strength,
            constitution,
            power,
            dexterity,
            charisma,
            intelligence,
            size,
            education,
            age,
            skill_dict,
        )
        return character


    def __init__(
        self,
        name,
        strength,
        constitution,
        power,
        dexterity,
        charisma,
        intelligence,
        size,
        education,
        age,
        skill_dict,
    ):
        self.name = name
        # STR, CON, POW, DEX, CHA are all 3d6
        self.strength = strength
        self.constitution = constitution
        self.power = power
        self.dexterity = dexterity
        self.charisma = charisma

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
            f" DEX: {self.dexterity:>2} | CHA: {self.charisma:>2}\n"
            f" SIZ: {self.size:>2} | EDU: {self.education:>2}\n"
            f"  HP: {self.current_hp}/{self.max_hp}"
        )
        for key in self.skill_dict:
            msg += "\n" + str(self.skill_dict[key])
        return msg

    def skill_roll(self, skill_name):
        skill = self.skill_dict[skill_name]
        return skill.roll()

class Characteristic(object):
    def __init__(self, name, short_name, score):
        self.name = name
        self.short_name = short_name
        self.score = score

    def __repr__(self):
        msg = f"{self.short_name}: {self.score}"
        return msg

    def __add__(self, x):
        return self.score + x

    def __radd__(self, x):
        return self.score + x

if __name__ == "__main__":
    print("Welcome to the Call of Cthulhu character generator.")
    name = input("Please provide a name for your character: ")
    skill_dict = HumanCharacter.read_skill_dict()
    # Now we will start creating a character.
    # TODO: Generate characteristics
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