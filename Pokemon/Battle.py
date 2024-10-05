import random as rd
import time
import os
from dotenv import load_dotenv

from Classes.Pokemon import Pokemon
from Data.color import color
from Classes.Move import Move
from Data.data import *

load_dotenv(".env")

#For printing separators
SECTION_SEPARATOR = os.getenv("SECTION_SEPARATOR")
TURN_SEPARATOR = os.getenv("TURN_SEPARATOR")
DELAY_TIME = float(os.getenv("DELAY_TIME"))

#Add delay
def delay():
    time.sleep(DELAY_TIME)

#Display HP
def print_hp(target: Pokemon):

    hp_col = []

    #high hp
    if target.HP / target.stats[0] > 0.5:
        hp_col = [color.GREEN, color.END]
    #medium hp
    if target.HP / target.stats[0] <= 0.5:
        hp_col = [color.YELLOW, color.END]
    #low hp
    if target.HP / target.stats[0] <= 0.25:
        hp_col = [color.RED, color.END]

    #male or female symbol
    gender = color.BOLD + color.BLUE + "♂" + color.END if target.gender == 1 \
        else color.BOLD + color.FAIRY + "♀" + color.END

    #decide status of pokemon
    status = ''
    if target.status == 'Fainted':
        status = '|' + color.RED + target.status + color.END + '|'
    elif target.status == 'Paralyzed':
        status = '|' + color.YELLOW + target.status + color.END + '|'
    elif target.status in ['Poisoned', 'BPoisoned']:
        status = '|' + color.PURPLE + 'Poisoned' + color.END + '|'
    elif target.status == 'Sleeping':
        status = '|' + color.BOLD + target.status + color.END + '|'
    elif target.status == 'Frozen':
        status = '|' + color.BLUE + target.status + color.END + '|'
    elif target.status == 'Burned':
        status = '|' + color.RED + target.status + color.END + '|'

    #string for name and gender
    hp = f"{data[target.id - 1]['name']['english']} {gender} "

    #fixed length for hp string for uniformity
    while len(hp) < 27:
        hp += ' '

    #length of actual hp and length of total hp bar
    hp_filling = '█' * round(target.HP / target.stats[0] / .05) + '░' * (20 - round(target.HP / target.stats[0] / .05))

    #final string for all information which is actually displayed
    print(f"{hp}lv{target.lvl} {hp_col[0]}[{hp_filling}]{hp_col[1]} {target.HP}/{target.stats[0]}\t{status}")

#call print hp function
def print_game_status(your_team, foes_team, y_now, f_now):
    print_hp(y_now)
    print_hp(f_now)

#print one move of pokemon
def print_move(target: Pokemon, move: Move):
    #white text for normal pp
    if target.pp[target.moves.index(move)] / move.pp >= 0.5:
        move_col = [color.END, color.END]
    #yellow text for moderate pp
    elif target.pp[target.moves.index(move)] / move.pp >= 0.25:
        move_col = [color.YELLOW, color.END]
    #red text for low or zero pp
    else:
        move_col = [color.RED, color.END]

    #display the color of text depending on the type of the move, blue for [water], red for [fire] from color.py file
    type_col = [color.__dict__[move.type.upper()], color.END]

    #change the color of text and then reset it to white
    move_str = move_col[0] + move.name + f" [{target.pp[target.moves.index(move)]}/{move.pp}]" + move_col[1]
    #for uniform length
    while len(move_str) < 35:
        move_str += ' '

    #print final move string for ONE move
    print(move_str + type_col[0] + f'|{move.type}|' + type_col[1])

def print_frozen(frozen: bool, target: Pokemon, game_data):
    # game_data[your_team,foes_team,y_now,f_now,turn,deployed]
    if frozen:
        print(color.BOLD + f"{data[target.id - 1]['name']['english']} is frozen solid!" + color.END)
        print_game_status(*game_data[:4])
        print(f"\n{TURN_SEPARATOR}\n")
        
        #return if frozen
        return game_data[3], game_data[2], game_data[4], game_data[5]
    else:
        #pokemon thaws out
        target.status = ''
        print(color.BOLD + f"{data[game_data[3].id - 1]['name']['english']} thawed out!")

#same logic as frozen
def print_paralyzed(paralyzed: bool, target: Pokemon, game_data):
    # game_data[your_team,foes_team,y_now,f_now,turn,deployed]
    if not paralyzed:
        print(color.BOLD + f"{data[target.id - 1]['name']['english']} is paralyzed! It can't move!" + color.END)
        print_game_status(*game_data[:4])
        print(f"\n{TURN_SEPARATOR}\n")
        return game_data[3], game_data[2], game_data[4], game_data[5]


#main battle function
def battle(your_team, foes_team, you, foe):

    y_temp_stats = list(map(lambda x: x.stats, your_team))
    f_temp_stats = list(map(lambda x: x.stats, foes_team))

    #true - player
    #false - computer
    turn = False

    #assigned current pokemon at start
    y_now = your_team[0]
    f_now = foes_team[0]
    #sent out pokemon message
    print(f"{you} send out {y_now.name}!")
    print(f"{foe} send out {f_now.name}!\n")
    deployed = {y_now}

    #check if entire team fainted
    def y_check_faint():
        if not list(filter(lambda x: x.status != 'Fainted', your_team)):
            raise Exception("You Lost")
        print('------------------------------------------')
        for i in range(len(your_team)):
            print(f'({i}) ', end='')
            print_hp(your_team[i])
        print('------------------------------------------\n')
        print(color.BOLD + 'Choose your next Pokemon!\n' + color.END)
        ch_poke = input().strip()
        while not ch_poke.isdigit() or int(ch_poke) not in [i for i in range(len(your_team))] or \
                your_team[int(ch_poke)] not in list(filter(lambda x: x.status != 'Fainted', your_team)):
            print('------------------------------------------')
            for i in range(len(your_team)):
                print(f'({i}) ', end='')
                print_hp(your_team[i])
            print('------------------------------------------\n')
            ch_poke = input().strip()
        y_now = your_team[int(ch_poke)]
        return y_now

    #user attack
    def y_attack(f_now, y_now, turn, deployed):
        #non damaging status effects which stop moves
        if y_now.status == 'Frozen':
            #if frozen and not using any fire moves, random chance of thawing out or staying frozen
            frozen: bool = rd.choices([True, False], [8, 2])[0] and not ch_move.name in [
                "Fusion flare", "Flame wheel", "Sacred fire", "Flare blitz", "scald", "Steam eruption"]
            print_frozen(frozen, y_now, [your_team, foes_team, y_now, f_now, turn, deployed])

        #if paralyzed, random chance of becoming normal
        if y_now.status == 'Paralyzed':
            paralyzed = rd.choices([True, False], [3, 1])[0]
            print_paralyzed(paralyzed, y_now, [your_team, foes_team, y_now, f_now, turn, deployed])

        #message telling that the move has been used
        print(f"{y_now.name} used {color.BOLD}{ch_move.name}{color.END}!")

        #user pokemon y_now attack foe f_now with move ch_move
        y_now.attack(y_now.moves.index(ch_move), f_now)

        #if foe faints
        if f_now.status == "Fainted":
            delay()
            deployed = {y_now}

            #send out pokemon next in index of foe's team
            try:
                f_now = rd.choice(list(filter(lambda x: x.status != "Fainted", foes_team)))

                print(color.BOLD + f"{foe} is going to send out {data[f_now.id - 1]['name']['english']}!" + color.END)
                print("Do you want to switch pokemon (y/N)?")

                switch = False
                ch = input().lower().strip()

                #user input to switch pokemon
                while ch not in ['y', 'n', 'yes', 'no', '']:
                    ch = input().strip()

                #do nothing if no
                if ch in ['n', 'no', '']: pass
                #ask for new pokemon
                else:
                    #switch flag
                    switch = True
                    print(color.BOLD + "Choose a Pokemon to switch!" + color.END)
                    print(f'{SECTION_SEPARATOR}')

                    #display team
                    for i in range(len(your_team)):
                        print(f'({i}) ', end='')
                        print_hp(your_team[i])

                    print(f'{SECTION_SEPARATOR}')

                    #ask for pokemon index based on team
                    ch_poke = input().strip()
                    back = False

                    #switched pokemon should not be fainted

                    #entered value is a digit and in valid range
                    while not ch_poke.isdigit() or int(ch_poke) not in [i for i in range(len(your_team))] or \
                            your_team[int(ch_poke)] not in list(filter(lambda x: x.status != 'Fainted', your_team)):
                        if ch_poke == '':
                            back = True
                            break

                        print(f'{SECTION_SEPARATOR}')

                        for i in range(len(your_team)):
                            print(f'({i}) ', end='')
                            print_hp(your_team[i])
                        print(f'{SECTION_SEPARATOR}\n')

                        ch_poke = input().strip()

                    #switch active pokemon to the now selected pokemon
                    if not back:
                        y_now = your_team[int(ch_poke)]
                        deployed = {y_now}
                    #no switch
                    else:
                        switch = False
                #foe sends next pokemon
                print(f"{foe} sent out {f_now.name}!")

                #if the switch flag is true, send out new pokemon, otherwise message will be "user let {current_pokemon} stay out"
                if switch:
                    print(f"{you} sent out {y_now.name}!")
                else:
                    print(f"{you} let {y_now.name} stay out!")

                #switch to computer turn
                turn = False
            except IndexError:
                pass

        #print hp of you and foe
        print_game_status(your_team, foes_team, y_now, f_now)
        print(f"\n{TURN_SEPARATOR}\n")

        delay()
        return f_now, y_now, turn, deployed

    #foe attack
    def fAttack(f_now, y_now, turn, deployed):

        #randomly select move
        ch_move = rd.randint(0, len(f_now.moves) - 1)

        if f_now.status == 'Burned':
            #burn dmg is 1/8th of health
            burn_dmg = f_now.stats[0] // 8

            print(color.BOLD + f"{data[f_now.id - 1]['name']['english']} is hurt by its burn" + color.END)

            f_now.HP -= burn_dmg

            #check if burn dmg faints pokemon
            if f_now.HP <= 0:
                f_now.status = 'Fainted'

                print(color.RED + f"{data[f_now.id - 1]['name']['english']} fainted!" + color.END)
        #same logic as burn
        if f_now.status == 'Poisoned':
            poison_dmg = f_now.stats[0] // 8

            print(color.BOLD + f"{data[f_now.id - 1]['name']['english']} is hurt by poison!" + color.END)

            f_now.HP -= poison_dmg

            if f_now.HP <= 0:
                f_now.status = 'Fainted'

                print(color.RED + f"{data[f_now.id - 1]['name']['english']} fainted!" + color.END)

        #clear frozen status if the move used is from the given selection
        if f_now.status == 'Frozen':
            if f_now.moves[ch_move].name in ["Fusion flare", "Flame wheel", "Sacred fire", "Flare blitz", "scald", "Steam eruption"]:
                f_now.status = ''
                print(color.BOLD + f"{data[f_now.id - 1]['name']['english']} thawed out!")
            else:
                #random chance of thawing out
                frozen: bool = rd.choices([True, False], [8, 2])[0]
                print_frozen(frozen, f_now, [your_team, foes_team, y_now, f_now, turn, deployed])


        if f_now.status == 'Paralyzed':
            #random chance of move working even if paralysis
            paralyzed = rd.choices([True, False], [3, 1])[0]
            print_paralyzed(paralyzed, f_now, [your_team, foes_team, y_now, f_now, turn, deployed])

        #delay if fainted
        if f_now.status == "Fainted":
            delay()

            
            deployed = {y_now}
            try:
                f_now = rd.choice(list(filter(lambda x: x.status != "Fainted", foes_team)))

                print(
                    color.BOLD + f"{foe} is going to send out {data[f_now.id - 1]['name']['english']}!" + color.END)
                print("Do you want to switch pokemon (y/N)?")

                switch = False
                ch = input().lower().strip()

                while ch not in ['y', 'n', 'yes', 'no', '']:
                    ch = input().strip()

                if ch in ['n', 'no', '']:
                    pass
                else:
                    switch = True

                    print(color.BOLD + "Choose a Pokemon to switch!" + color.END)
                    print(f'{SECTION_SEPARATOR}')

                    for i in range(len(your_team)):
                        print(f'({i}) ', end='')
                        print_hp(your_team[i])

                    print(f'{SECTION_SEPARATOR}\n')

                    ch_poke = input().strip()
                    back = False

                    while not ch_poke.isdigit() or int(ch_poke) not in [i for i in range(len(your_team))] or \
                            your_team[int(ch_poke)] not in list(filter(lambda x: x.status != 'Fainted', your_team)):
                        if ch_poke == '':
                            back = True
                            break

                        print(f'{SECTION_SEPARATOR}')

                        for i in range(len(your_team)):
                            print(f'({i}) ', end='')
                            print_hp(your_team[i])

                        print(f'{SECTION_SEPARATOR}\n')

                        ch_poke = input().strip()

                    if not back:
                        y_now = your_team[int(ch_poke)]
                    else:
                        switch = False

                print(f"{foe} sent out {f_now.name}!")

                #if the switch flag is true, send out new pokemon, otherwise message will be "user let {current_pokemon} stay out"
                if switch:
                    print(f"{you} sent out {y_now.name}!")
                else:
                    print(f"{you} let {y_now.name} stay out!")

                return f_now, y_now, turn, deployed

            except IndexError:
                pass

            print(f"\n{TURN_SEPARATOR}\n")
            print_game_status(your_team, foes_team, y_now, f_now)

            return f_now, y_now, turn, deployed

        print(f"{f_now.name} used {color.BOLD}{f_now.moves[ch_move].name}{color.END}!")

        f_now.attack(ch_move, y_now)

        print_game_status(your_team, foes_team, y_now, f_now)
        print(f"\n{TURN_SEPARATOR}\n")

        delay()

        return f_now, y_now, turn, deployed

    print_game_status(your_team, foes_team, y_now, f_now)
    print(f"\n{TURN_SEPARATOR}\n")

    #game loop runs till either team has fainted
    while list(filter(lambda x: x.status != "Fainted", your_team)) and list(filter(lambda x: x.status != "Fainted", foes_team)):
        turn = not turn #switch turn

        if turn:
            #hurt from burn
            if y_now.status == 'Burned':
                burn_dmg = f_now.stats[0] // 8

                print(color.BOLD + f"{data[y_now.id - 1]['name']['english']} is hurt by its burn!" + color.END)

                y_now.HP -= burn_dmg

                if y_now.HP <= 0:
                    y_now.Hp = 0
                    y_now.status = 'Fainted'

                    print(color.RED + f"{data[y_now.id - 1]['name']['english']} fainted!" + color.END)

                    y_check_faint()

            #hurt from poison
            if y_now.status == 'Poisoned':
                poison_dmg = f_now.stats[0] // 8

                print(color.BOLD + f"{data[y_now.id - 1]['name']['english']} is hurt by poison!" + color.END)

                y_now.HP -= poison_dmg
                if y_now.HP <= 0:
                    y_now.Hp = 0
                    y_now.status = 'Fainted'
                    print(color.RED + f"{data[y_now.id - 1]['name']['english']} fainted!" + color.END)
                    y_check_faint()

            #what to do?
            print(*["(0) Attack", "(1) Pokemon"], sep = "\n", end="\n\n")

            turn_option = input().strip()

            #wrong input, what to do?
            while turn_option not in ["0", "1"]:
                print(*["(0) Attack", "(1) Pokemon"], sep="\n", end="\n\n")
                turn_option = input().strip()

            #print move if the user decides to attack
            if turn_option == "0":
                print(f'{SECTION_SEPARATOR}')

                for i in range(len(y_now.moves)):
                    print(f'({i}) ', end=' ')
                    print_move(y_now, y_now.moves[i])

                print(f'{SECTION_SEPARATOR}\n')

                #ask for move input
                ch_move = input().strip()
                back = False

                #validity of input similar to before
                while not ch_move.isdigit() or int(ch_move) not in [i for i in range(len(y_now.moves))] or y_now.moves[int(ch_move)] \
                        not in list(filter(lambda x: y_now.pp[y_now.moves.index(x)] > 0, y_now.moves)):
                    if ch_move == '':
                        back = True
                        break

                    print(f'{SECTION_SEPARATOR}')

                    for i in range(4):
                        print(f'({i}) ', end=' ')
                        print_move(y_now, y_now.moves[i])

                    print(f'{SECTION_SEPARATOR}\n')

                    ch_move = input().strip()
                if back:
                    turn = False
                    continue

                ch_move = y_now.moves[int(ch_move)]
                tch_move = ch_move

                if y_now.stats[5] >= f_now.stats[5]:
                    f_now, y_now, turn, deployed = y_attack(f_now, y_now, turn, deployed)
                    if not turn:
                        continue
                else:
                    print(f"\n{TURN_SEPARATOR}\n")

                    f_now, y_now, turn, deployed = fAttack(f_now, y_now, turn, deployed)

                    if y_now.status == "Fainted":
                        try:
                            y_now = y_check_faint()
                        except:
                            break
                        deployed.add(y_now)

                        print(f"\n{you} sent out {y_now.name}!")

                        turn = False
                        continue

                    ch_move = tch_move
                    delay()
                    f_now, y_now, turn, deployed = y_attack(f_now, y_now, turn, deployed)

                    if not turn:
                        continue
                    turn = not turn

            #if the user decides to switch pokemon
            elif turn_option == "1":

                print(color.BOLD + "Choose a Pokemon to switch!" + color.END)
                print(f'{SECTION_SEPARATOR}')

                for i in range(len(your_team)):
                    print(f'({i}) ', end='')
                    print_hp(your_team[i])

                print(f'{SECTION_SEPARATOR}\n')

                ch_poke = input().strip()
                back = False

                #validity of input similar to before
                while not ch_poke.isdigit() or int(ch_poke) not in [i for i in range(len(your_team))] or\
                        your_team[int(ch_poke)] not in list(filter(lambda x: x.status != 'Fainted', your_team)) or your_team[int(ch_poke)] == y_now:
                    if ch_poke == '':
                        back = True
                        break

                    print(f'{SECTION_SEPARATOR}')

                    for i in range(len(your_team)):
                        print(f'({i}) ', end='')
                        print_hp(your_team[i])

                    print(f'{SECTION_SEPARATOR}\n')

                    ch_poke = input().strip()
                if back:
                    turn = False
                    continue

                y_now = your_team[int(ch_poke)]
                deployed.add(y_now)

                print(f'{you} sent out {y_now.name}!')

            
        else:
            f_now, y_now, turn, deployed = fAttack(f_now, y_now, turn, deployed)
            if y_now.status == "Fainted":
                try:
                    y_now = y_check_faint()
                except:
                    break
                deployed.add(y_now)

                print(f"\n{you} send out {y_now.name}!\n")
                print(f"\n{TURN_SEPARATOR}")
                print_game_status(your_team, foes_team, y_now, f_now)

                turn = False
                continue

    #win/lose message at the end
    if list(filter(lambda x: x.status != "Fainted", your_team)):
        
        print("""
__   __           __        __            _ 
\ \ / /__  _   _  \ \      / /__  _ ___   | |
 \ V / _ \| | | |  \ \ /\ / / _ \| '_  \  | |
  | | (_) | |_| |   \ V  V / (_) | | | | |_|
  |_|\___/ \__,_|    \_/\_/ \___/|_| |_| (_)
""")
        
    else:
        print("""
__   __            _              _             __
\ \ / /__  _   _  | |    ___  ___| |_      _   / /
 \ V / _ \| | | | | |   / _ \/ __| __|    (_) | | 
  | | (_) | |_| | | |__| (_) \__ \ |_      _  | | 
  |_|\___/ \__,_| |_____\___/|___/\__|    (_) | | 
                                               \_\\
""")
    #extra \ because python escape sequence

    for i in range(len(your_team)):
        your_team[i].stats = y_temp_stats[i]
    for i in range(len(foes_team)):
        foes_team[i].stats = f_temp_stats[i]