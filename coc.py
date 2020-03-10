from dice import dice_pool, dice_roll, d6_pool, Die
from functools import reduce
from math import ceil


class Skill(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.check = False

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
    def generate_random(cls, name):
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
        # Skills
        skill_dict = {
            "accounting": Skill("accounting", 5),
            "anthropology": Skill("anthropology", 1),
            "appraise": Skill("appraise", 5),
            "archaeology": Skill("archaeology", 1),
            "art/craft": Skill("art/craft", 5),
            "charm": Skill("charm", 15),
            "climb": Skill("climb", 20),
            "credit rating": Skill("credit rating", 0),
            "cthulhu mythos": Skill("cthulhu mythos", 0),
            "disguise": Skill("disguise", 5),
            "dodge": Skill("dodge", (dexterity / 2)),
            "drive auto": Skill("drive auto", 20),
            "elec repair": Skill("elec repair", 10),
            "fast talk": Skill("fast talk", 5),
            "brawl": Skill("brawl", 25),
            "handgun": Skill("handgun", 20),
            "rifle/shotgun": Skill("rifle/shotgun", 25),
            "first aid": Skill("first aid", 30),
            "history": Skill("history", 5),
            "intimidate": Skill("intimidate", 15),
            "jump": Skill("jump", 20),
            "language (other)": Skill("language (other)", 1),
            "language (own)": Skill("language (own)", education),
            "law": Skill("law", 5),
            "library use": Skill("library use", 20),
            "listen": Skill("listen", 20),
            "locksmith": Skill("locksmith", 1),
            "mechanical repair": Skill("mechanical repair", 10),
            "medicine": Skill("medicine", 1),
            "natural world": Skill("natural world", 10),
            "navigate": Skill("navigate", 10),
            "occult": Skill("occult", 5),
            "heavy machinery": Skill("heavy machinery", 1),
            "persuade": Skill("persuade", 10),
            "pilot": Skill("pilot", 1),
            "psychology": Skill("psychology", 10),
            "psychoanalysis": Skill("psychoanalysis", 1),
            "ride": Skill("ride", 5),
            "science": Skill("science", 1),
            "sleight of hand": Skill("sleight of hand", 10),
            "spot hidden": Skill("spot hidden", 25),
            "stealth": Skill("stealth", 20),
            "survival": Skill("survival", 10),
            "swim": Skill("swim", 20),
            "throw": Skill("throw", 20),
            "track": Skill("track", 10),
        }
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

    def damage_bonus_table(self):
        key = self.strength + self.size
        if key >= 41:
            return "+2d6"
        elif key >= 33:
            return "+1d6"
        elif key >= 25:
            return "+1d4"
        elif key >= 17:
            return "None"
        elif key >= 13:
            return "-1d4"
        else:
            return "-1d6"

    def damage_roll(self, weapon_damage):
        key = self.strength + self.size
        damage_bonus = 0
        if key >= 41:
            damage_bonus = dice_roll(dice_pool(2, 6))
        elif key >= 33:
            damage_bonus = dice_roll(dice_pool(1, 6))
        elif key >= 25:
            damage_bonus = dice_roll(dice_pool(1, 4))
        elif key >= 17:
            pass
        elif key >= 13:
            damage_bonus = -(dice_roll(dice_pool(1, 4)))
        else:
            damage_bonus = -(dice_roll(dice_pool(1, 6)))
        return weapon_damage + damage_bonus

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


if __name__ == "__main__":
    print("Welcome to the Call of Cthulhu character generator.")
    name = input("Please provide a name for your character: ")
    player = HumanCharacter.generate_random(name)
    print(f"Here is your character, {name}: \n{player}")
    library_roll = player.skill_roll("library use")
    print(
        f"Let's go to the library! You rolled a {library_roll['result']}, which compared to your skill of {player.get_points('library use')} makes it a {'success' if library_roll['outcome'] is True else 'failure'}."
    )
