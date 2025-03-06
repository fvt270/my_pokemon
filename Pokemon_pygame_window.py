from Stats import *
import sys
from Pokemon_class import Pokemon
from Pokemons import *
from pygame_helpers.COLORS import *
from pygame_helpers.pygame_metadata import *
from pygame_helpers.pygame_helpers import calculate_spacing, core_game_loop_pygame, fight_move_quadrant_calculations, death_screen, check_death, choose_pokemon_screen, victory_screen, load_saved_game_screen
from pygame_helpers.save_game_feature import save_the_game
from Pokemons import *
import pygame
# import threading # For slowly ticking down health bar


clock = pygame.time.Clock()

# Pokemon stats:
MY_POKEMON = squirtle
ENEMY_POKEMON = weedle.copy_pokemon_class()

# Initialize Pygame
pygame.init()

# HEALTH BARS RENDERING
MY_HEALTH_BOX_DIMENSIONS = pygame.Rect(0, 420, 300, 120)
ENEMY_HEALTH_BOX_DIMENSIONS = pygame.Rect(SCREEN_WIDTH-300, 0, 300, 80) # Make it not as high, as exact HP is not mentioned for the enemy!

# WORDS FOR OPTION
# 4 words: ["FIGHT", "POKEMON", "BAG", "RUN"]
# 5 spaces
option_words = ["FIGHT", "POKEMON", "BAG", "RUN"]
spacing = calculate_spacing(OPTION_BOX_HEIGHT, TEXT_SIZE, len(option_words))
# Option buttons
option_button_rects: list[pygame.Rect] = []
option_quarter = OPTION_BOX_HEIGHT
for i,word in enumerate(option_words):
    option_rect = pygame.Rect(TEXT_BOX_WIDTH, SCREEN_HEIGHT-option_quarter, OPTION_BOX_WIDTH, OPTION_BOX_HEIGHT / len(option_words))
    option_button_rects.append(option_rect)
    option_quarter -= OPTION_BOX_HEIGHT / len(option_words)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rasmus's Pokemon")

# Font for rendering text
font = pygame.font.Font(None, TEXT_SIZE)

# Text box rect
text_box_rect = pygame.Rect(0, SCREEN_HEIGHT - TEXT_BOX_HEIGHT, TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT)
options_box_rect = pygame.Rect(TEXT_BOX_WIDTH, SCREEN_HEIGHT - OPTION_BOX_HEIGHT, OPTION_BOX_WIDTH, OPTION_BOX_HEIGHT) # Starts after text_box_rect

# Battle_intro
battle_intro = f'{MY_POKEMON.name} encounters {ENEMY_POKEMON.name}!\nTime to battle!'
# Fight_moves quadrants:
fight_move_quadrants = fight_move_quadrant_calculations(text_box_rect)
animation_running = False

# Choosen_pokemon and other flags 
pokemon_chosen: bool = False
battle_active: bool = False
already_defeated_flag: bool = False # To only gain battle rewards once
new_game: bool = False # Flag to tell whether the save is a new game or not



xp_gained, level_up = None, None

enemy_pokemon_options = [weedle]

# Save feature settings
game_name = None
pokemons_all_mine = [squirtle, bulbasaur, charmander]
saved_games_folder = "saved_games"
temp_save_name = "" # For editing your save game name, when creating a new game


# Main loop
running = True
while running:
    assert current_intro in valid_intros, f"Current intro: {current_intro} is not found in valid intros: {'\n'.join(valid_intros)}"
    dt = clock.tick(FPS) # Slow down the game


    ###########################################
    # Testing Suite


    # Need a way to save the game
    #   - Also a way to load seperate safe file or start a new
    # I also need to have the pokemons carry over so you can continue playing
    # Leveling is busted
    # Would also be nice to have a way to catch pokemon
    # Would also be nice to have a way to heal all your pokemon between each combat - but you get more for not healing!
    # Also handle speed, so fast pokemons act first
    if game_name is None:
        pokemons_all_mine, game_name, new_game, temp_save_name = load_saved_game_screen(screen=screen, font=font, new_game=new_game, saved_games_folder=saved_games_folder, temp_save_name=temp_save_name)
        pygame.display.flip()
        continue

    ############################################

    if not pokemon_chosen:
        pokemon_chosen, MY_POKEMON, battle_active, ENEMY_POKEMON = choose_pokemon_screen(screen=screen, font=font, my_pokemons=pokemons_all_mine, enemy_pokemon_options=enemy_pokemon_options)
    elif not check_death(MY_POKEMON, ENEMY_POKEMON) and battle_active:
        running, battle_active, battle_intro, current_intro, pokemon_passive_animation_timer, wiggle_iteration,animation_running, fight_animation_timer = core_game_loop_pygame(text_box_rect, MY_POKEMON.moves, fight_move_quadrants, MY_POKEMON, ENEMY_POKEMON, option_button_rects, option_words, options_box_rect, screen, font, spacing, ENEMY_PLATFORM_POS,MY_POKEMON_PLATFORM_POS,platform_radius,pokemon_scaling,MY_POKEMON_POS,ENEMY_POS,MY_HEALTH_BOX_DIMENSIONS,ENEMY_HEALTH_BOX_DIMENSIONS,wiggle,animation_running,current_intro,battle_intro,active,pokemon_passive_animation_timer,wiggle_iteration,points,fight_animation_timer)
    else:
        # Check which death
        if MY_POKEMON.HP <= 0:
            death_screen(pokemon_that_fainted=MY_POKEMON.name, screen=screen, font=font)
        elif ENEMY_POKEMON.HP <= 0:
            if already_defeated_flag:
                pass
            else:
                xp_gained, level_up = MY_POKEMON.gain_xp(ENEMY_POKEMON)
                already_defeated_flag = True
            pokemon_chosen = victory_screen(pokemon_that_fainted=ENEMY_POKEMON, my_pokemon=MY_POKEMON, screen=screen, font=font, xp_gained=xp_gained, level_up= level_up, my_pokemons_all=pokemons_all_mine, game_name=game_name, saved_folder=saved_games_folder) 
            save_the_game(pokemons_all_mine, game_name, saved_folder=saved_games_folder)
        else:
            # Continue fighting
            pass


    # Update the display
    pygame.display.flip()


# Quit Pygame, but save beforehand
save_the_game(pokemons_all_mine, game_name, saved_folder=saved_games_folder)
pygame.quit()
sys.exit()

