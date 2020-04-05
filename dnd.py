from dice import dice_roll, dice_pool
from interfaces import Rollable

#TODO #14 implement saving throws
#TODO #12: implement abilties
#TODO #15 implement special skills and abilities
#TODO #16 implement classes
#TODO #17 implement alignment
#TODO #18 implement levelling
#TODO #19 implement armor class
#TODO #13 implement hit points
#TODO #20 consider implementing inventory? or leave it to character sheet class

class Ability(Rollable):
    def __init__(self, name, score, adjustment, abbreviation):
        super.__init__(name, score)
        self.adjustment = adjustment
        self.abbreviation = name[0:2].toUpper()

class PlayerCharacter():
    def __init__(self,
        name,
        cclass,
        level,
        abilities,
        xp,
        hp,
        gp,
        inventory,
        ac,
        saving_throws):
        self.name = name
        self.cclass = cclass
        self.level = level
        self.strength = abilities['strength']
        self.intelligence = abilities['intelligence']
        self.wisdom = abilities['wisdom']
        self.dexterity = abilities['dexterity']
        self.constitution = abilities['constitution']
        self.charisma = abilities['charisma']
        self.xp = xp
        self.hp = hp
        self.saving_throws = saving_throws

    @staticmethod
    def getSavingThrows(cclass):
        if cclass == "Normal Man":
            return {
                'poison or death ray': 14,
                'magic wands': 15,
                'paralysis or turn to stone': 16,
                'dragon breath': 17,
                'rods, staves, or spells': 17
            }
        elif cclass == "Cleric":
            return {
                'poison or death ray': 11,
                'magic wands': 12,
                'paralysis or turn to stone': 14,
                'dragon breath': 16,
                'rods, staves, or spells': 15
            }
        elif cclass == "Dwarf" or "Halfling":
            return {
                'poison or death ray': 10,
                'magic wands': 11,
                'paralysis or turn to stone': 12,
                'dragon breath': 13,
                'rods, staves, or spells': 14
            }
        elif cclass == "Elf":
            return {
                'poison or death ray': 12,
                'magic wands': 13,
                'paralysis or turn to stone': 13,
                'dragon breath': 15,
                'rods, staves, or spells': 15
            }
        elif cclass == "Fighter":
            return {
                'poison or death ray': 12,
                'magic wands': 13,
                'paralysis or turn to stone': 14,
                'dragon breath': 15,
                'rods, staves, or spells': 16
            }
        elif cclass == "Magic-User":
            return {
                'poison or death ray': 13,
                'magic wands': 14,
                'paralysis or turn to stone': 13,
                'dragon breath': 16,
                'rods, staves, or spells': 15
            }
        elif cclass == "Thief":
            return {
                'poison or death ray': 13,
                'magic wands': 14,
                'paralysis or turn to stone': 13,
                'dragon breath': 16,
                'rods, staves, or spells': 15
            }

if __name__ == "__main__":
    print(f'Generating skill rolls...')
    # Step 1
    ability_names = ['strength','intelligence','wisdom','dexterity','constitution','charisma']
    # Step 2
    abilities = dict(zip(ability_names,[dice_roll(dice_pool(3,6)) for x in range(6)]))
    #TODO #21 Step 3: Select Character Class
    #TODO #22 Step 4: Select Special Abilities, like Magic-User and Elf spells
    #TODO #23 Step 5: Ability Score Adjustments
    #TODO #24 Step 6: Bonuses and Penalties
    # Step 7: XP
    #TODO #25 Step 8: HP
    # Step 9: Alignment
    # Step 10: GP
    gp = dice_roll(dice_pool(3,6)) * 10
    #TODO #26 Step 11: Inventory
    #TODO #27 Step 12: Armor Class
    #TODO #28 Step 13: THAC0, Saving throws
    print(f'Available classes: Cleric, Dwarf, Halfling, Elf, Fighter, Magic-User, Thief.')
    cclass = input(f'Please choose a class: ')
    saving_throws = PlayerCharacter.getSavingThrows(cclass)
    