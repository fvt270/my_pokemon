# Generate a random pokemon from a level specification
# Set stats, moves etc.
# Pokemon class needs:
# self.name = name
# self.HP = HP
# self.dmg = dmg
# self.defense = defense
# self.speed = speed
# self.type = type
# self.moves = moves
from Pokemon_class import Pokemon

### Dict to dictate level scaling
# BHP = Base Health Point
level_scaling = {
    "Weedle":{
        "BHP": 6,
        "HP": 1.5,
        "dmg": 1,
        "defense": 0.5,
        "speed": 0.5,
        "type": "Grass",
        "moves": ["Tackle", "Tail Whip"]
    },
}


def gen_pokemon(level, name):
    """
    Generate Pokemon stats given by level and name
    """
    assert name in level_scaling.keys(), "Unkown pokemon: " + name
    poke = level_scaling[name]
    hp = int(poke["BHP"] + (level * poke["HP"]))
    dmg = int(level * poke["dmg"])
    defense = int(level * poke["defense"])
    speed =  int(level * poke["speed"]),
    pokemon_type = poke["type"]
    moves = poke["moves"] # Probably need a random selector for 4!
    return Pokemon(name, hp, dmg, defense, speed, pokemon_type, moves)


print("Generating a weedle lv 1 and lv 5")
lv_one = gen_pokemon(1, "Weedle")
lv_five = gen_pokemon(5, "Weedle")
print("Level one:")
for attr, value in lv_one.__dict__.items():
    print(f"{attr}: {value}")
print("Level five:")
for attr, value in lv_five.__dict__.items():
    print(f"{attr}: {value}")