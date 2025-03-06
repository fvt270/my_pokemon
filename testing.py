from Pokemon_game import *

# gameloop()

from pygame_helpers.save_game_feature import saved_game, load_game
from Pokemons import *

# # save game
# test_save = saved_game([squirtle, weedle], "test_save")
# # mess with HP of a pokemon
# print(test_save.pokemons[0].HP)
# test_save.pokemons[0].HP -= 1
# print(test_save.pokemons[0].HP)
# test_save.save_game()

# load game
test = load_game("Louploup")
print(test.pokemons[0].HP)
print(test.pokemons[0].level)
print(test.pokemons[0].xp)



# import pygame
# from pygame_helpers.pygame_helpers import load_saved_game_screen
# # Initialize Pygame
# pygame.init()
# screen = pygame.display.set_mode((720, 800))
# pygame.display.set_caption("Rasmus's Pokemon")

# # Font for rendering text
# font = pygame.font.Font(None, 36)
# load_saved_game_screen(screen=screen, font=font, new_game=False)