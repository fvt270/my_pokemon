# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 720

# Text box dimensions
TEXT_BOX_HEIGHT = SCREEN_HEIGHT // 4  # Bottom 1/4 of the screen
TEXT_BOX_WIDTH = SCREEN_WIDTH * (2/3) # Width 2/3 of the screen
# Option box dimentsions
OPTION_BOX_HEIGHT = SCREEN_HEIGHT // 4
OPTION_BOX_WIDTH = SCREEN_WIDTH * (1/3)

TEXT_SIZE = 36
LINE_SPACING = 10 # Space between lines

ANIMATION_TIMER = 3000.0 # Three seconds for each animation

FPS = 30
active = False
current_intro = "BATTLE_INTRO" # Whether to display fight, bag, pokemon or battle_intro etc.
valid_intros = ["BATTLE_INTRO", "POKEMON", "BAG", "RUN", "ENEMY_TURN", "MOVE", "FIGHT"]
# Move animation toggle:
fight_animation_timer: float = 0.0
pokemon_passive_animation_timer: float = 5000.0
points = None # initial points for pokemon_drawing
# Pokemon rendering base stats
pokemon_scaling = 4
height_scaling = SCREEN_HEIGHT // (pokemon_scaling * 2)
width_scaling = SCREEN_WIDTH // (pokemon_scaling * 2)
ENEMY_POS = (500, 100)
MY_POKEMON_POS = (140, 250)
ENEMY_PLATFORM_POS = (ENEMY_POS[0] + width_scaling, ENEMY_POS[1] + height_scaling)
MY_POKEMON_PLATFORM_POS = (MY_POKEMON_POS[0] + width_scaling, MY_POKEMON_POS[1] + height_scaling)
platform_radius = 150
wiggle = 10 # Wiggle by ten pixels
wiggle_iteration = 0 # First wiggle iteration