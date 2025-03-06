import os


# dmg is the damage multiplier!!!
all_moves = {
    "Bubbles":{
        "dmg": 1,
        "type": "Water",
        "status": None,
        "mvtype": "Attack",
        "flavortext": lambda my_pokemon, enemy_pokemon: f"{my_pokemon} blew bubbles at {enemy_pokemon}."
    },
    "Tackle":{
        "dmg": 1,
        "type": "Normal",
        "status": None,
        "mvtype": "Attack",
        "flavortext": lambda my_pokemon, enemy_pokemon: f"{my_pokemon} tackles {enemy_pokemon}."
    },
    "Ember":{
        "dmg": 1,
        "type": "Fire",
        "status": None,
        "mvtype": "Attack",
        "flavortext": lambda my_pokemon, enemy_pokemon: f"{my_pokemon} burned {enemy_pokemon}."
    },
    "Leaf Cut":{
        "dmg": 1,
        "type": "Grass",
        "status": None,
        "mvtype": "Attack",
        "flavortext": lambda my_pokemon, enemy_pokemon: f"{my_pokemon} threw sharp leaves at \n{enemy_pokemon}!"
    },
    "Tail Whip":{
        "dmg": 1,
        "type": "Normal",
        "status": "Defense",
        ##### How much bla bla....
        "mvtype": "Debuff",
        "flavortext": lambda my_pokemon, enemy_pokemon: f"{my_pokemon} waggles its tail,\nlowering {enemy_pokemon}'s defense."
    },
    "Defense Curl":{
        "dmg": 1,
        "type": "Normal",
        "status": "Defense",
        ##### How much bla bla....
        "mvtype": "Buff",
        "flavortext": lambda my_pokemon, enemy_pokemon: f"{my_pokemon} curled up and increased its defense."
    }
}

img_paths = {
    "Squirtle": os.path.join("assets","Squirtle.png"),
    "Weedle": os.path.join("assets","Weedle.png"),
    "Charmander": os.path.join("assets","Charmander.png"),
    "Bulbasaur": os.path.join("assets","Bulbasaur.png"),
}