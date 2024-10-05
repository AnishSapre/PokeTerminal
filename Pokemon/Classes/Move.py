from typing import Union
import random as rd

from Data.data import *
import Data.data
from Data.color import color


class Move:
    def __init__(self, name: str, type, category: int, pp: int, power: Union[int, None],
                 accuracy: Union[float, None], times=1):
        #name of move
        self.name = name
        #type of move (fire/water etc etc)
        self.type = type

        #Melee hit, ranged hit or a buff(for self) or debuff(for opponent) depending on the move 0 is Physical 1 is Special 2 is Status effect move
        self.category = category

        #Power points is the number of times you can use the move
        self.pp = pp

        #Power of move
        self.power = power

        # %accuracy
        self.accuracy = accuracy

        #if the move is multiple hit instead of single hit
        self.times = times

    #user and target pokemon
    def use(self, user, target):
        if self.category != 2 and self.power is not None: #if the move if not a buff/debuff move then do this
            try:
                hit = rd.choices(population=[1, 0], weights=[self.accuracy, 1 - self.accuracy])[0]
            except:
                hit = 1
            if hit == 0:
                #evasion
                print(f"{data[target.id - 1]['name']['english']} avoided the attack!")
                return

            #VALUES FOR DAMAGE FORMULA
            #random element
            rand = rd.randint(85, 100) / 100

            #extra damage if move is same type as the user
            stab = 1.5 if len(set(self.type) & set(user.type)) >= 1 else 1

            #extra damage regardless of type
            crit = rd.randint(0, 16) == 1
            critical = 1.5 if crit else 1

            #type advantages and disadvantages
            type_mult = 1
            burned = 0.5 if user.status == 'Burned' and self.category == 0 else 1
            for type in target.type:
                if type in typeChart[self.type]["Strength"]:
                    type_mult *= 2
                elif type in typeChart[self.type]["Weakness"]:
                    type_mult /= 2
                elif type in typeChart[self.type]["NoEffect"]: #no damage if normal on ghost for ex
                    print(color.YELLOW + "its not effective" + color.END)
                    type_mult = 0
                    break

            #if the move is freeze dry and the target pokemon is a water type, the dmg is doubled (exception in normal type advantages)
            if self.name == "Freeze-dry" and "Water" in [target.type]:
                type_mult *= 2

            #used type advantage
            if type_mult > 1:
                print(color.YELLOW + "its very effective!" + color.END)
            #no type advantage
            elif type_mult < 1 and type_mult != 0:
                print(color.YELLOW + "its not very effective" + color.END)


            #DAMAGE FORMULA      
            damage = hit * int((((2 * user.lvl / 5 + 2) * self.power * ((user.stats[1] if self.category == 0 else user.stats[3]) / (target.stats[2] if self.category == 0 else target.stats[4])) / 50) + 2) * rand * stab * critical * type_mult * burned)
            target.HP -= damage

            #english name from json
            print(f"{data[target.id - 1]['name']['english']} got {damage} damage!")
            if crit:
                print(color.RED + "A critical hit!" + color.END)

            #Status effects
            if self.name == "Tri Attack":
                if rd.choices([1, 0], [1, 4])[0]:
                    #randomly give one of three status effects
                    status = rd.choices(["Frozen", "Paralyzed", "Burned"], [1, 1, 1])[0]
                    target.status = status

            #poison target
            if self.name in Data.data.poison_inflict_chances and hit:
                if rd.choices([1, 0], Data.data.poison_inflict_chances[self.name])[0]:
                    target.getStatus("Poisoned")
            #paralyze target
            if self.name in Data.data.paralysis_inflict_chances and hit and "Electric" not in target.type:
                if rd.choices([1, 0], Data.data.paralysis_inflict_chances[self.name])[0]:
                    target.getStatus("Paralyzed")
            #burn target
            if self.name in Data.data.burn_inflict_chances and hit and "Fire" not in target.type:
                if rd.choices([1, 0], Data.data.burn_inflict_chances[self.name])[0]:
                    target.getStatus("Burned")
        
            #freeze target
            if self.name in ["Ice beam", "Blizzard", "Freeze-dry", "Freezing glare", "Ice fang", "Ice punch", "Powder snow", "Shadow chill"] and hit:
                if rd.choices([1, 0], [1, 9])[0]:
                    target.getStatus("Frozen")

            #pokemon will stop being frozen if it is fire type, or it uses scald or steam eruption moves
            if target.status == 'Frozen' and (self.type == 'Fire' or self.name == 'Scald' or self.name == 'Steam erruption'):
                print(color.BOLD + f"{data[target.id - 1]['name']['english']} thawed out!")
                target.status = ''

            #if pokemon faints condition
            if target.HP <= 0:
                target.HP = 0
                target.status = "Fainted"
                print(color.RED + f"{data[target.id - 1]['name']['english']} fainted!" + color.END)