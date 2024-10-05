import json
import math as m

data = json.loads(open("Data/pokedata.json", "r").read())
baseXp = json.loads(open("Data/baseXp.json", "r").read())

#strength and weakness chart
typeChart = {
    "Normal": {"Strength": [], "Weakness": ["Rock", "Steel"], "NoEffect": ["Ghost"]},
    "Fire": {"Strength": ["Grass", "Steel", "Ice", "Bug"], "Weakness": ["Fire", "Water", "Rock", "Dragon"], "NoEffect": []},
    "Water": {"Strength": ["Fire", "Ground", "Rock"], "Weakness": ["Water", "Grass", "Dragon"], "NoEffect": []},
    "Grass": {"Strength": ["Water", "Ground", "Rock"], "Weakness": ["Fire", "Grass", "Dragon", "Poison", "Bug", "Flying", "Steel"], "NoEffect": []},
    "Electric": {"Strength": ["Water", "Flying"], "Weakness": ["Electric", "Grass", "Dragon"], "NoEffect": ["Ground"]},
    "Ice": {"Strength": ["Grass", "Ground", "Flying", "Dragon"], "Weakness": ["Fire", "Water", "Ice", "Steel"], "NoEffect": []},
    "Fighting": {"Strength": ["Normal", "Ice", "Rock", "Dark", "Steel"], "Weakness": ["Poison", "Flying", "Physical", "Bug", "Fairy"], "NoEffect": ["Ghost"]},
    "Poison": {"Strength": ["Grass", "Fairy"], "Weakness": ["Poison", "Ground", "Rock", "Ghost"], "NoEffect": ["Steel"]},
    "Ground": {"Strength": ["Fire", "Electric", "Poison", "Rock", "Steel"], "Weakness": ["Grass", "Bug"], "NoEffect": ["Flying"]},
    "Flying": {"Strength": ["Grass", "Fighting", "Bug"], "Weakness": ["Electric", "Rock", "Steel"], "NoEffect": []},
    "Psychic": {"Strength": ["Fighting", "Poison"], "Weakness": ["Psychic", "Steel"], "NoEffect": ["Dark"]},
    "Bug": {"Strength": ["Grass", "Psychic", "Dark"], "Weakness": ["Fire", "Fighting", "Poison", "Flying", "Ghost", "Steel", "Fairy"], "NoEffect": []},
    "Rock": {"Strength": ["Fire", "Ice", "Flying", "Bug"], "Weakness": ["Fighting", "Ground", "Steel"], "NoEffect": []},
    "Ghost": {"Strength": ["Psychic", "Ghost"], "Weakness": ["Dark"], "NoEffect": ["Normal"]},
    "Dragon": {"Strength": ["Dragon"], "Weakness": ["Steel"], "NoEffect": ["Fairy"]},
    "Dark": {"Strength": ["Psychic", "Ghost"], "Weakness": ["Fighting", "Dark", "Fairy"], "NoEffect": []},
    "Steel": {"Strength": ["Ice", "Rock", "Fairy"], "Weakness": ["Fire", "Water", "Electric", "Steel"], "NoEffect": []},
    "Fairy": {"Strength": ["Fighting", "Dragon", "Dark"], "Weakness": ["Poison", "Steel"], "NoEffect": []},
}

#standard exp formula- erratic, fast, medium fast, medium slow, slow, fluctuating
#n is level which is passed to lambda function 
expFormulas = [
    lambda n: (n ** 3) * (100 - n) // 50 if n < 50
    else (n ** 3) * (150 - n) // 100 if n < 68
    else (n ** 3) * m.floor((1911 - 10 * n) / 3) // 500 if n < 98
    else (n ** 3) * (160 - n) // 100,

    lambda n: 4 * (n ** 3) // 5,

    lambda n: n ** 3,

    lambda n: round(6 / 5 * (n ** 3) - 15 * (n ** 2) + 100 * n - 140),

    lambda n: 5 * (n ** 3) // 4,

    lambda n: round((n ** 3) * ((m.floor((n + 1) / 3) + 24) / 50)) if n < 15
    else (n ** 3) * (n + 14) // 50 if n < 36
    else (n ** 3) * (m.floor(n / 2) + 32) // 50
]

#Exp Gain Type
#0-Erratic
#1-Fast
#2-Medium Fast
#3-Medium Slow
#4-Slow
#5-Fluctuating

natureList = ["Hardy", "Lonely", "Adamant", "Naughty", "Brave",
              "Bold", "Docile", "Impish", "Lax", "Relaxed",
              "Modest", "Mild", "Bashful", "Rash", "Quiet",
              "Calm", "Gentle", "Careful", "Quirky", "Sassy",
              "Timid", "Hasty", "Jolly", "Naive", "Serious"]

#poison chances of each poison move
poison_inflict_chances = {
    "Cross poison": [1, 9],     # 10%
    "Poison tail": [1, 9],      # 10%
    "Sludge wave": [1, 9],      # 10%
    "Gunk shot": [3, 7],        # 30%
    "Poison jab": [3, 7],       # 30%
    "Poison sting": [3, 7],     # 30%
    "Sludge bomb": [3, 7],      # 30%
    "Sludge": [3, 7],           # 30%
    "Shell side arm": [2, 8],   # 20%
    "Smog": [4, 6]              # 40%
}

#paralyze chances of each electric move
paralysis_inflict_chances = {
    "Nuzzle": [1, 0],           # 100%
    "Zap cannon": [1,0],        # 100%
    "Body slam": [3, 7],        # 30%
    "Bounce": [3, 7],           # 30%
    "Discharge": [3, 7],        # 30%
    "Dragon breath": [3, 7],    # 30%
    "Force palm": [3, 7],       # 30%
    "Freeze shock": [3, 7],     # 30%
    "Lick": [3, 7],             # 30%
    "Spark": [3, 7],            # 30%
    "Thunder": [3, 7],          # 30%
    "Bolt strike": [2, 8],      # 20%
    "Thunderbolt": [1, 9],      # 10%
    "Shadow bolt": [1, 9],      # 10%
    "Thunder fang": [1, 9],     # 10%
    "Thunder punch": [1, 9],    # 10%
    "Thunder shock": [1, 9]     # 10%
}

#burn chances of each fire move
burn_inflict_chances = {
    "Inferno": [1, 0],          # 100%
    "Lava plume": [3, 7],       # 30%
    "Scald": [3, 7],            # 30%
    "Steam eruption": [3, 7],   # 30%
    "Searing shot": [3, 7],     # 30%
    "Blue flare": [2, 8],       # 20%
    "Blaze kick": [1, 9],       # 10%
    "Ember": [1, 9],            # 10%
    "Fire blast": [1, 9],       # 10%
    "Fire fang": [1, 9],        # 10%
    "Fire punch": [1, 9],       # 10%
    "Flame wheel": [1, 9],      # 10%
    "Flamethrower": [1, 9],     # 10%
    "Flare blitz": [1, 9],      # 10%
    "Heat wave": [1, 9],        # 10%
    "Pyro ball": [1, 9],        # 10%
}