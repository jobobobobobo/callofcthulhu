from random import randint
from functools import reduce


class Die(object):
    def __init__(self, faces):
        self.faces = faces
        self.result = randint(1, faces)

    def get_result(self):
        return self.result

    def roll(self):
        self.result = randint(1, self.faces)

    def __add__(self, x):
        return self.result + x

    def __radd__(self, x):
        return self.result + x

    def __sub__(self, x):
        return self.result - x

    def __rsub__(self, x):
        return self.result - x

    def __repr__(self):
        return f"d{self.faces}: {self.result}"


def exploding_dice(d=10, count=1, target=8, explode=10, ez=False):
    success = 0
    results = dice_pool(count, d)
    for die in results:
        while die.get_result() >= explode:
            if ez is True:
                success += 2
            else:
                success += 1
                results.append(Die(d))
            break
        if die.get_result() >= target:
            success += 1
    return success


def fudge_dice(count=1):
    results = [Die(3) for _ in range(count)]
    result = 0
    for die in results:
        if die == 1:
            result += 1
        elif die == 3:
            result -= 1
    return result


def dice_pool(count, faces):
    return [Die(faces) for _ in range(count)]


def d6_pool(count):
    return dice_pool(count, 6)


def d10_pool(count):
    return dice_pool(count, 10)


def dice_roll(dice_list, static_mod=0):
    dice_sum = reduce((lambda x, y: x + y), dice_list)
    return dice_sum + static_mod


if __name__ == "__main__":
    pool = int(input(f"Please provide the dice pool for your exploding dice: "))
    print(f"You rolled {exploding_dice(count=pool)} successes")
    print(f"If these were Fudge dice, you would have rolled {fudge_dice(pool)}")
