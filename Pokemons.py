from Pokemon_class import Pokemon, level_profile

###############################################################################
# Level profiles:
# HP gain, dmg gain, defense gain, speed gain
# All is in per level gains, so 0.5 is one gain per 2 levels
weak_all_rounder = level_profile(1.5, 1, 0.33, 0.25)
medium_all_rounder = level_profile(2, 1, 0.5, 0.33)
# strong

# Defensive builds
weak_defensive_build = level_profile(2.5, 0.5, 0.5, 0.125)
medium_defensive_build = level_profile(2.5, 0.5, 1, 0.125)
# strong

# Attack builds
weak_attack_build = level_profile(1.25, 1.25, 0.33, 0.33)
medium_attack_build = level_profile(1.5, 1.5, 0.33, 0.33)

# Specialist builds:


###############################################################################
    # All pokemons:
    # Pokemon: NAME; HP; MAX_HP; DMG; DEF; SPEED; TYPE; MOVES

# Starters:
squirtle = Pokemon("Squirtle", 10, 10, 2, 1, 2, 5, "Water", ["Tackle","Bubbles"], medium_all_rounder)
charmander= Pokemon("Charmander", 10, 10, 2, 1, 2, 5, "Fire", ["Tackle","Ember"], medium_attack_build)
bulbasaur = Pokemon("Bulbasaur", 10, 10, 2, 1, 2, 5, "Grass", ["Tackle", "Leaf Cut"], medium_defensive_build)

# charizard = Pokemon("Charizard", 100, 100, 3, 1, 3, 25, "Fire", ["Tackle"])
weedle = Pokemon("Weedle", 6, 6, 1, 0, 10, 5, "Grass", ["Tackle", "Tail Whip"], weak_all_rounder)


all_pokemons = {
        "Squirtle": squirtle,
        "Weedle": weedle,
        "Charmander": charmander
    }

