from Data.color import color
from Data.data import *
import json
import numpy as np
import random as r

expTypes = json.loads(open("Data/expType.json", 'r').read())


class Pokemon:
    def __init__(self, name: str, moves, gender: int, id: int, lvl: int = 100, status: str = ''):
        self.name = name
        self.gender = gender
        self.moves = moves

        #Decide PP or Power Points from the moves
        self.pp = [move.pp for move in moves]
        self.nature = r.choice(natureList)
        self.natureStat = [1, 1, 1, 1, 1]

        #A nature will multiply the value of one stat by 1.1, and the value of another stat by 0.9. 
        #This basically adds or subtracts 10% to or from the stat.
        self.natureStat[natureList.index(self.nature) % 5] -= 0.1
        self.natureStat[natureList.index(self.nature) // 5] += 0.1

        self.id = id #pokedex ID

        #data = json.loads(open("Data/Json/pokedata.json", "r").read()) from here in the data file
        self.type = data[id - 1]['type']

        self.lvl = lvl

        #calculate the growth rate from the json file and s
        self.expType = ['Erratic','Fast','Medium Fast','Medium Slow','Slow','Fluctuating'].index(expTypes[str(self.id)])
        
        #current exp and exp for next level
        self.exp = [expFormulas[self.expType](lvl), expFormulas[self.expType](lvl + 1)]

        self.status = status

        self.iv = [r.randint(0, 31), r.randint(0, 31), r.randint(0, 31)] #RANDOM VALUES FOR IV
        self.ev = [0, 0, 0, 0, 0, 0] #NOT ASSIGNING EVS

        self.baseStats = np.array(list(data[self.id - 1]["base"].values())) #Take base stats from json by pokemon index

        #numpy array to store stats
        #HP formula = floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + Level + 10
        #Other Stat formulae = (floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + 5) x Nature

        self.stats = np.array([m.floor(0.01 * (2 * self.baseStats[0] + self.iv[0] + m.floor(0.25 * self.ev[0])) * self.lvl) + self.lvl + 5, #HP STAT

                            #REMAINING STATS (ATK,SPATK,DEF,SPDEF,SPEED)

                               m.floor((0.01 * ((2 * self.baseStats[1] + self.iv[1] + m.floor(0.25 * self.ev[1])) * self.lvl) + 5) * self.natureStat[0]),

                               m.floor((0.01 * ((2 * self.baseStats[2] + self.iv[1] + m.floor(0.25 * self.ev[2])) * self.lvl) + 5) * self.natureStat[1]),

                               m.floor((0.01 * ((2 * self.baseStats[3] + self.iv[1] + m.floor(0.25 * self.ev[3])) * self.lvl) + 5) * self.natureStat[2]),

                               m.floor((0.01 * ((2 * self.baseStats[4] + self.iv[2] + m.floor(0.25 * self.ev[4])) * self.lvl) + 5) * self.natureStat[3]),

                               m.floor((0.01 * ((2 * self.baseStats[5] + self.iv[1] + m.floor(0.25 * self.ev[5])) * self.lvl) + 5) * self.natureStat[4]),
                               ])
        self.HP = self.stats[0] #ASSIGN CALCULATED HP TO POKEMON HP

    #decrease pp for every move used
    def attack(self, moveId, target):
        if self.pp[moveId] != 0:
            self.moves[moveId].use(self, target)
        self.pp[moveId] -= 1

    #increase stats on level gain
    def changeStats(self, statId, value):
        self.stats[statId] += value

    #get status of pokemon
    def getStatus(self, status):
        #exit function conditions, 
        #pokemon cant be burned if it is fire type
        #pokemon cant be paralyzed if it is electric type
        #pokemon cant be frozen if it is ice type
        #pokemon cant be poisoned if it is steel type
        if 'Fire' in self.type and status == 'Burned':
            return
        if 'Ice' in self.type and status == 'Frozen':
            return
        if 'Electric' in self.type and status == 'Paralyzed':
            return
        if 'Steel' in self.type and status in ['Poisoned', 'BPoisoned']:
            return

        #continue if no exceptions
        if self.status == '':
            self.status = status
            if self.status in ['Poisoned', 'Burned', 'Paralyzed']:
                print(color.BOLD + f"\n{data[self.id - 1]['name']['english']} is {self.status}!\n" + color.END)
                if self.status == 'Paralyzed':

                    #speed stat reduction if paralyzed
                    self.stats[5] *= 0.5

            #display status messages
            if self.status == 'Frozen':
                print(color.BOLD + f"\n{data[self.id - 1]['name']['english']} is frozen solid!\n" + color.END)
            if self.status == 'Sleeping':
                print(color.BOLD + f"\n{data[self.id - 1]['name']['english']} felt asleep!\n" + color.END)
            if self.status == 'BPoisoned':
                print(color.BOLD + f"\n{data[self.id - 1]['name']['english']} is badly poisoned!\n" + color.END)