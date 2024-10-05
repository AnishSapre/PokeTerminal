import random
from Battle import *
from Data.attacks import *

def main():
    with open("config.json") as cnf:
        config = json.load(cnf)

    #create objects for each team: name,list of attack,gender,id from config.json
    YourTeam = list(
        map(lambda x: Pokemon(x["name"], list(map((lambda y: globals()[y]), x["attacks"])), x["gender"], x["id"]),
            config["YourTeam"]))

    FoesTeam = list(
        map(lambda x: Pokemon(x["name"], list(map((lambda y: globals()[y]), x["attacks"])), x["gender"], x["id"]),
            config["FoesTeam"]))

    #call battle.py file for battle engine
    battle(YourTeam, FoesTeam, "Anish", "Computer")

main()