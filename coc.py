from dice import dice_pool, dice_roll, d6_pool, Die
from functools import reduce
from interfaces import Characteristic, Skill
import math
from random import sample
import csv

# The damage bonus table can be found on page 33 of the 7th revised edition.
def damage_bonus_table(strength, size):
    key = strength + size
    damage_bonus = 0
    damage_bonus_string = None
    build = 0
    if key >= 165:
        number_d6 = math.ceil(((key-204)/80)+1)
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
class Skill(Rollable):
    def __init__(self, name, score, check=False, rules=None, important=False):
        super().__init__(name, score)
        self.rules = rules
        self.important = important
        self.check = check

    def skill_improvement(self, check=True, roll=Die(100).result):
        if check == True:
            if roll > self.score:
                self.score += Die(6)

    def __str__(self):
        box = "\u25a1"
        checked = "\u2611"
        msg = f"{box if self.check is False else checked} {self.name.title()}: {self.score}"
        return msg

    def roll(self):
        result = Die(100).result
        outcome = True if (result <= self.score) else False
        if outcome is True:
            self.check = True
        return {"outcome": outcome, "result": result}

    @classmethod
    def from_tuple(cls, name_score_tuple):
        skill = super().from_tuple(name_score_tuple)
        return skill

class Characteristic(Rollable):
    def __init__(self, name, short_name=None, score=0, rules=None):
        if short_name == None:
           self.short_name = name[0:3]
        super().__init__(name, score)
        self.short_name = short_name.upper()

    def roll(self):
        result = Die(100).result
        outcome = True if (result <= self.score) else False
        if outcome is True:
            self.check = True
        return {"outcome": outcome, "result": result}
    
    def __str__(self):
        msg = f"{self.short_name}: {self.score:>2}"
        return msg
    def __repr__(self):
        msg = f"{self.short_name}: {self.score:>2}"
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

    @staticmethod
    def calculate_movement_rate(strength, dexterity, size):
        rate = 0
        if dexterity < size and strength < size:
            rate = 7
        elif (strength >= size or dexterity >= size) or strength == size and dexterity == size:
            rate = 8
        elif strength > size and dexterity > size:
            rate = 9
        return Characteristic("Movement Rate", "MOV", rate)
        

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

    def apply_age_penalty(
        self, 
        strength=None, 
        constitution=None, 
        size=None, 
        dexterity=None, 
        appearance=None, 
        intelligence=None, 
        power=None, 
        education=None
        ):
        if strength == None:
            strength = self.strength
        if constitution == None:
            constitution = self.constitution
        if size == None:
            size = self.size
        if dexterity == None:
            dexterity = self.dexterity
        if appearance == None:
            appearance = self.appearance
        if intelligence == None:
            intelligence = self.intelligence
        if power == None:
            power = self.power
        if education == None:
            education = self.education
        if self.age >= 80:
            for _ in range(4):
                education.skill_improvement(check=True)
            self.strength = strength
            self.constitution = constitution
            self.dexterity = dexterity
            self.appearance.score -= 25
            self.movement_rate.score -= 5
        elif self.age >= 70:
            for _ in range(4):
                education.skill_improvement(check=True)
            self.strength = strength
            self.constitution = constitution
            self.dexterity = dexterity
            self.appearance.score -= 20
            self.movement_rate.score -= 4
        elif self.age >= 60:
            for _ in range(4):
                education.skill_improvement(check=True)
            self.strength = strength
            self.constitution = constitution
            self.dexterity = dexterity
            self.appearance.score -= 15
            self.movement_rate.score -= 3
        elif self.age >= 50:
            for _ in range(3):
                education.skill_improvement(check=True)
            self.strength = strength
            self.constitution = constitution
            self.dexterity = dexterity
            self.appearance.score -= 10
            self.movement_rate.score -= 2
        elif self.age >= 40:
            for _ in range(2):
                education.skill_improvement(check=True)
            self.strength = strength
            self.constitution = constitution
            self.dexterity = dexterity
            self.appearance.score -= 5
            self.movement_rate.score -= 1
        elif self.age >= 20:
            education.skill_improvement(check=True)
        elif self.age >= 15:
            self.size = size
            self.strength = strength
            self.education.score -= 5
            luck_roll = [d6_pool(3),d6_pool(3)]
            self.luck = max(dice_roll(x) for x in luck_roll) * 5
        self.damage_bonus_table = damage_bonus_table(strength, size)



    # TODO #8: make a new constructor for Skills and Characteristics to pull from a tuple like (Skill_name, score).
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
        # character.apply_age_penalty(age)


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
        age: int,
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
        self.apply_age_penalty(self.age)

        # Derived stats
        self.damage_bonus_table = damage_bonus_table(self.strength, self.size)
        self.max_hp = Characteristic("Hit Points", "HP", score=math.floor((self.constitution + self.size)/10))
        self.current_hp = self.max_hp
        self.wound_threshold = math.ceil(self.max_hp.score / 2)
        self.movement_rate = Investigator.calculate_movement_rate(strength=self.strength,dexterity=self.dexterity,size=self.size)

        # Skills
        self.skill_dict = skill_dict

    def damage_roll(self, weapon_damage):
        damage_bonus = damage_bonus_table(self.strength, self.size)
        return weapon_damage + damage_bonus['damage-bonus']

    def __repr__(self):
        msg = (
            f" Name: {self.name}\n Age: {self.age:>2}\n"
            f"  {self.strength} | {self.intelligence}\n"
            f"  {self.constitution} | {self.power}\n"
            f"  {self.dexterity} | {self.appearance}\n"
            f"  {self.size} | {self.education}\n"
            f"  {self.current_hp}/{self.max_hp.score}\n"
            f"  {self.movement_rate}"
        )
        skill_dict = self.get_skill_list(important=True)
        for key in skill_dict:
            msg += "\n" + str(skill_dict[key])
        return msg

    def get_skill_list(self, important=False):
        if important is False:
            return [skill for skill in self.skill_dict]
        elif important is True:
            return [skill_dict[key] for key in self.skill_dict.keys() if skill_dict[key].important is True]

    def skill_roll(self, skill_name):
        skill = self.skill_dict[skill_name]
        return skill.roll()


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
    age = int(input("Please enter an age for your investigator: "))
    print("Thank you. This will have an effect on your investigator later on.")
    leonard = Investigator(
        name=name, 
        strength=stat_block['STR'], 
        constitution=stat_block['CON'], 
        size=stat_block['SIZ'],
        dexterity=stat_block['DEX'],
        appearance=stat_block['APP'],
        intelligence=stat_block['INT'],
        power=stat_block['POW'],
        education=stat_block['EDU'],
        luck=stat_block['LUK'],
        age=age,
        skill_dict=skill_dict
    )
    required_penalty = 0
    if age >= 80:
        required_penalty = 80
    elif age >= 70:
        required_penalty = 40
    elif age >= 60:
        required_penalty = 20
    elif age >= 50:
        required_penalty = 10
    elif age >= 40:
        required_penalty = 5    
    elif age >= 15:
        required_penalty = 0
    remaining_penalty = required_penalty
    while (remaining_penalty > 0):
        print(f"You currently have to apply {remaining_penalty} out of {required_penalty} points.")
        if age >= 20:
            stat_apply_to = input("Please choose between STR, CON, and DEX: ")
        else:
            stat_apply_to = input("Please choose between STR and SIZ: ").upper()
        penalty_to_apply = int(input(f"Please input an amount no greater than {remaining_penalty}: "))
        if penalty_to_apply >= remaining_penalty:
            penalty_to_apply = remaining_penalty
        if penalty_to_apply >= stat_block[stat_apply_to].score:
            penalty_to_apply = stat_block[stat_apply_to].score
        remaining_penalty -= penalty_to_apply
        stat_block[stat_apply_to].score -= penalty_to_apply
    leonard.apply_age_penalty(
        strength=stat_block['STR'], 
        constitution=stat_block['CON'], 
        size=stat_block['SIZ'], 
        dexterity=stat_block['DEX'], 
        appearance=stat_block['APP'], 
        intelligence=stat_block['INT'], 
        power=stat_block['POW'], 
        education=stat_block['EDU']
    )
    print(leonard)
    occupation_name = input("Please provide a title for your occupation: ")
    # TODO #11 Find a way to import occupations
    # TODO #10 Find a way to generate credit scores
    print(f"Now it is time to determine {name}'s occupation.")
    credit_score = int(input("Please enter a credit score for your character: "))
    occupation_skills = {}
    for _ in range(8):
        skill_name = input("Please provide a name for your skill: ")
        skill_base = input("Please input a base value for the skill: ")
        skill = Skill(skill_name, skill_base,important=True)
        occupation_skills.update({skill_name: skill})
    
    
    # TODO #5 implement Decide skills & allocate points step
    # update step for the skills we've been selecting
    leonard.skill_dict.update(occupation_skills)
    # TODO #4 implement Create a backstory step
    # TODO #3 implement Equip investigator step
    print(leonard)