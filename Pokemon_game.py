from Stats import *
import random
import time
from Pokemon_class import Pokemon
from Pokemons import *


###############################################################################

def choose_pokemon():
    my_pokemon = int(input("Choose a pokemon!\n1: Squirtle\n2: Charizard\n3: Weedle\n"))
    if my_pokemon not in [1, 2, 3]:
        choose_pokemon()
    elif my_pokemon == 1:
        return squirtle
    elif my_pokemon == 2:
        return charizard
    elif my_pokemon == 3:
        return weedle
    else:
        choose_pokemon()

def end_check(pokemon1: Pokemon, pokemon2: Pokemon) -> bool:
    """Check if combat has ended"""
    if pokemon1.HP <= 0 or pokemon2.HP <= 0:
        return False
    else:
        return True

def turn_order(pokemon1: Pokemon, pokemon2: Pokemon) -> bool:
    """Determines turn order, pokemon1 should be the trainers pokemon!
    @param pokemon1: Players Pokemon
    @param pokemon2: Opponents Pokemon
    @returns: Determines if pokemon1 is faster than pokemon2
    """
    if pokemon1.speed > pokemon2.speed:
        print(pokemon1.name, "is faster than", pokemon2.name + "!")
        return True
    elif pokemon1.speed < pokemon2.speed:
        print(pokemon2.name, "is faster than", pokemon1.name + "!")
        return False
    if pokemon1.speed == pokemon2.speed:
        print(pokemon1.name, "is equally as fast as", pokemon2.name + "!")
        print("Trainer pokemon goes first!")
        return True



def opponent_turn(opponents_pokemon: Pokemon, my_pokemon: Pokemon):
    """Choose a random move for the opponents pokemon to act upon"""
    print("\n")
    chosen_move = random.randint(0, len(opponents_pokemon.moves)-1)
    move = opponents_pokemon.choose_move(chosen_move)
    opponents_pokemon.find_mv_type(my_pokemon, move)
    # opponents_pokemon.attack_move(my_pokemon, move_dmg, move_type)

def my_turn(my_pokemon: Pokemon, opponents_pokemon: Pokemon):
    chosen_move = my_pokemon.see_moves()
    move = my_pokemon.choose_move(chosen_move)
    my_pokemon.find_mv_type(opponents_pokemon, move)
    # my_pokemon.attack_move(opponents_pokemon, move_dmg, move_type)

def gameloop():
    my_pokemon: Pokemon = choose_pokemon()
    opponents_pokemon: Pokemon = squirtle
    print("\n\n") # Create space before battle
    player_is_faster: bool = turn_order(my_pokemon, opponents_pokemon)
    while end_check(pokemon1=my_pokemon, pokemon2=opponents_pokemon):
        print("-------------------------------------------------")
        print(f"Your Pokemon '{my_pokemon.name}' has {my_pokemon.HP} health remaining")
        print(f"The enemy Pokemon '{opponents_pokemon.name}' has {opponents_pokemon.HP} health remaining")
        if player_is_faster:
            # Player starts attacking
            my_turn(my_pokemon=my_pokemon, opponents_pokemon=opponents_pokemon)
            time.sleep(1.0)
            # Check for end
            if not end_check(pokemon1=my_pokemon, pokemon2=opponents_pokemon):
                print(f"{opponents_pokemon.name} has fainted!")
                break
            # Opponents attack!
            opponent_turn(opponents_pokemon, my_pokemon)
        else:
            # Opponent start attacking
            opponent_turn(opponents_pokemon, my_pokemon)
            time.sleep(1.0)
            # Check for end
            if not end_check(pokemon1=my_pokemon, pokemon2=opponents_pokemon):
                print(f"{my_pokemon.name} has fainted!")
                break
            # Player attack!
            my_turn(my_pokemon=my_pokemon, opponents_pokemon=opponents_pokemon)
        print("\n\n")    
        time.sleep(1.0)

