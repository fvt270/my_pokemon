import pygame
from Stats import img_paths, all_moves # Use moves for typing
from shapes.shape_functions import hypotenuse
from pygame_helpers.COLORS import *
from pygame_helpers.save_game_feature import saved_game, load_game, save_the_game
from pygame_helpers.pygame_metadata import *
import random, os 
from Pokemon_class import Pokemon
from Pokemons import *

def calculate_spacing(y_size: float | int, text_size: int, n_words: int):
    """
    Calcualte spacing between each word to have a nice look
    @param y_size: Size to fit the spacing in
    @param text_size: Size of your text
    @param n_words: Number of words to fit in y_size
    @returns: size of spaces between each word
    """
    # Ensure there are no zero or negative values for n_words
    if n_words <= 0:
        raise ValueError("Number of words must be greater than zero.")

    # Calculate the total space occupied by words
    total_word_space = n_words * text_size

    # Remaining space for the gaps (y_size minus the space taken by words)
    total_spacing = y_size - total_word_space

    # Ensure that total_spacing is not negative
    if total_spacing < 0:
        raise ValueError("y_size is too small to fit the text and required spacing.")

    # Calculate the size of each space
    spaces = n_words + 1  # There are always one more space than the number of words
    space_size = total_spacing / spaces

    return space_size


def render_pokemon(pokemon_name, dimensions, enemy, pokemon_scaling):
    """
    Render and scale pokemon in Pygame
    @param pokemon_name: Name of the pokemon to render
    @param dimensions: Dimensions of screen
    @param enemy: Whether to render for enemy. True for enemy
    @param pokemon_scaling: Factor to scale pokemon by
    """
    # assert dimensions == (800, 720), "Rendering only made for 800x720"
    image = pygame.image.load(img_paths[pokemon_name]).convert_alpha()
    scaled = pygame.transform.scale(image, (dimensions[0]//pokemon_scaling, dimensions[1]//pokemon_scaling))
    if enemy:
        return scaled
    elif not enemy:
        return pygame.transform.flip(scaled, flip_x=1, flip_y=0)
    

def increase_wiggle(radius, iteration: int):
    """
    Makes a point rotate such that images don't just stand in place
    @param radius: How much to rotate the point by (Hypotenuse)
    @param iteration: Which point to draw (out of 4 (0 to 3))
    @returns: How much to add to points (x,y) and next iteration number
    """
    # Order of drawing:
    # [(x, y), (-x, y), (x, -y), (-x, -y), (y, x), (-y, x), (y, -x), (-y, -x)]
    circle_points = [(1,1), (-1,1), (1,-1), (-1,-1)]
    if iteration > 3:
        iteration = 0
    points = (radius*circle_points[iteration][0], radius*circle_points[iteration][1])
    return points, iteration + 1



def battle_intro_print_text(battle_intro: str, text_box_rect: pygame.Rect, screen: pygame.Surface, font: pygame.font, active: bool, fps: int = 30):
    """
    Print the battle_intro text inside the text_box_rect on screen
    """
    intros = battle_intro.split("\n")
    font_size_move_down = LINE_SPACING
    for intro in intros:
        text_surface = font.render(intro, True, WHITE if active else GRAY)
        screen.blit(text_surface, (text_box_rect.x + LINE_SPACING, text_box_rect.y + font_size_move_down))
        font_size_move_down += TEXT_SIZE
    

def option_text_print(option_words, option_button_rects, options_box_rect, screen, spacing, font):
    """
    Print the options inside the option_box_rect on screen with buttons
    """
    for i, word in enumerate(option_words):
        # Render option buttons
        pygame.draw.rect(screen, WHITE, option_button_rects[i])
        pygame.draw.rect(screen, BLACK, option_button_rects[i], 1, 2)
        go_down_space = int(spacing*2 + (i)* (TEXT_SIZE + spacing)) # This works... idk why
        text_surface = font.render(word, True, BLACK)
        screen.blit(text_surface, (options_box_rect.x + LINE_SPACING, options_box_rect.y + go_down_space))

def fight_move_quadrant_calculations(text_box_rect) -> dict[pygame.Rect]:
    """
    Calculate quadrants for each fight move, such that they each take up a quarter
    """
    quadrants = {
        0: pygame.Rect(text_box_rect.left, text_box_rect.top, text_box_rect.width/2, text_box_rect.height/2),
        1: pygame.Rect(text_box_rect.left + text_box_rect.width/2, text_box_rect.top, text_box_rect.width/2, text_box_rect.height/2),
        2: pygame.Rect(text_box_rect.left, text_box_rect.top + text_box_rect.height/2, text_box_rect.width/2, text_box_rect.height/2),
        3: pygame.Rect(text_box_rect.left + text_box_rect.width/2, text_box_rect.top + text_box_rect.height/2, text_box_rect.width/2, text_box_rect.height/2)
    }
    return quadrants

def pokemon_typing_to_color(typing: str) -> (int,int,int):
    typing = typing.lower()
    if typing == "water":
        return BLUE
    elif typing == "fire":
        return RED
    elif typing == "normal":
        return GRAY
    elif typing == "grass":
        return GREEN
    else:
        raise NotImplementedError

def determine_move_type_color(move: str) -> (int,int,int):
    """
    Return RGB color according to movetype
    @param move: Name of the move used
    @returns: RGB color code
    """
    move_type = all_moves[move]["type"]
    return pokemon_typing_to_color(move_type)
    



def fight_moves_print(moves: list[str], text_box_rect: pygame.Rect, screen: pygame.Surface, font: pygame.font, quadrants: dict[pygame.Rect]):
    """
    Print the moves of your pokemon in the text box
    """
    # Divide text_box into quadrants:
    # quadrants = fight_move_quadrant_calculations(text_box_rect=text_box_rect) # Don't do calculation each time
    for i, move in enumerate(moves):
        col = determine_move_type_color(move)
        text_surface = font.render(move, True, col) # Can maybe make move-type into the color
        pygame.draw.rect(screen, WHITE, quadrants[i])
        pygame.draw.rect(screen, BLACK, quadrants[i], 2, 5)
        screen.blit(text_surface, (quadrants[i].x +10, quadrants[i].y + text_box_rect.height/5))

def fight_collide_points(moves: list[str], quadrants: dict[pygame.Rect], pos) -> str | None:
    for i, move in enumerate(moves):
        if quadrants[i].collidepoint(pos):
            return move
        else:
            continue
    return None

def use_move_print(move_intro, text_box_rect: pygame.Rect, screen: pygame.Surface, font: pygame.font):
    intros = move_intro.split("\n")
    font_size_move_down = LINE_SPACING
    for intro in intros:
        text_surface = font.render(intro, True, WHITE)
        screen.blit(text_surface, (text_box_rect.x + LINE_SPACING, text_box_rect.y + font_size_move_down))
        font_size_move_down += TEXT_SIZE

def death_screen(pokemon_that_fainted: str, screen:pygame.Surface, font: pygame.font):
    """
    Writes on screen you died
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit Pygame
            pygame.quit()
    screen.fill(BLACK)
    screen_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    text_surface = font.render(f"Your Pokemon: {pokemon_that_fainted} fainted!", True, WHITE)
    text_rect = text_surface.get_rect()
    screen.blit(text_surface, (screen_center[0] - (text_rect.width // 2), screen_center[1]))

def __victory_screen_buttons(screen:pygame.Surface, top_of_buttons: int, font: pygame.font):
    """
    Rects for victory screen drawing buttons,returning the rects
    """
    fifth_of_screen = SCREEN_WIDTH // 5
    eigth_of_height = SCREEN_HEIGHT // 8
    yes_button = pygame.Rect(fifth_of_screen, top_of_buttons, fifth_of_screen, eigth_of_height)
    no_button = pygame.Rect(fifth_of_screen * 3, top_of_buttons, fifth_of_screen, eigth_of_height)


    # Drawing the buttons:
    pygame.draw.rect(screen, GREEN, yes_button)
    pygame.draw.rect(screen, RED, no_button)

    
    text_y_coordinate = yes_button.top + (yes_button.height // 3)
    text_surface = font.render(f"Fight again!", True, BLACK)
    text_rect = text_surface.get_rect()
    text_x_coordinate_yes = yes_button.x + ((yes_button.width - text_rect.width) // 2)
    screen.blit(text_surface, (text_x_coordinate_yes, text_y_coordinate))
    text_surface = font.render(f"Quit", True, BLACK)
    text_rect = text_surface.get_rect()
    text_x_coordinate_no = no_button.x + ((no_button.width - text_rect.width) // 2)
    screen.blit(text_surface, (text_x_coordinate_no, text_y_coordinate))
    return yes_button, no_button

def victory_screen(pokemon_that_fainted: Pokemon, my_pokemon: Pokemon, my_pokemons_all: list[Pokemon], game_name: str, saved_folder: str, screen:pygame.Surface, font: pygame.font, xp_gained: int, level_up: bool):
    """
    Writes on screen you won!

    @returns: False if press continue for pokemon_chosen
    """
    screen.fill(LINEN)
    screen_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    # Print who fainted
    text_surface = font.render(f"The enemy {pokemon_that_fainted.name} fainted!", True, BLACK)
    text_rect = text_surface.get_rect()
    screen.blit(text_surface, (screen_center[0] - (text_rect.width // 2), screen_center[1]))
    # Print battle rewards:

    # Only gain xp if not lv. 100
    if my_pokemon.level > 99:
        yes_button, no_button = __victory_screen_buttons(screen=screen, top_of_buttons=screen_center[1] + 3 * TEXT_SIZE, font=font)
    else:
        text_surface = font.render(f"Your {my_pokemon.name} gained {xp_gained} xp.", True, BLACK)
        text_rect = text_surface.get_rect()
        screen.blit(text_surface, (screen_center[0] - (text_rect.width // 2), screen_center[1] + TEXT_SIZE))
        if level_up:
            text_surface = font.render(f"Your {my_pokemon.name} leveled up to lv. {my_pokemon.level}!", True, BLACK)
            text_rect = text_surface.get_rect()
            screen.blit(text_surface, (screen_center[0] - (text_rect.width // 2), screen_center[1] + 2 * TEXT_SIZE))
            yes_button, no_button = __victory_screen_buttons(screen=screen, top_of_buttons=screen_center[1] + 4 * TEXT_SIZE, font=font)
        else:
            yes_button, no_button = __victory_screen_buttons(screen=screen, top_of_buttons=screen_center[1] + 3 * TEXT_SIZE, font=font)

    # Buttons for continuing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit Pygame
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if yes_button.collidepoint(event.pos):
                print("Continue!")
                return False
            elif no_button.collidepoint(event.pos):
                print("Quit!")
                save_the_game(my_pokemons_all, game_name, saved_folder=saved_folder)
                pygame.quit()
    return True

def check_death(my_pokemon: Pokemon, enemy_pokemon: Pokemon) -> bool:
    """Check if there is death among the pokemons"""
    if my_pokemon.HP <= 0 or enemy_pokemon.HP <= 0:
        return True
    else:
        return False

def core_game_loop_pygame(text_box_rect, 
                          MY_POKEMON_MOVES, 
                          fight_move_quadrants, 
                          MY_POKEMON, ENEMY_POKEMON, 
                          option_button_rects, 
                          option_words, 
                          options_box_rect, 
                          screen, 
                          font, 
                          spacing, 
                          ENEMY_PLATFORM_POS,
                          MY_POKEMON_PLATFORM_POS,
                          platform_radius,
                          pokemon_scaling,
                          MY_POKEMON_POS,
                          ENEMY_POS,
                          MY_HEALTH_BOX_DIMENSIONS,
                          ENEMY_HEALTH_BOX_DIMENSIONS,
                          wiggle,
                          animation_running,
                          current_intro,
                          battle_intro,
                          active,
                          pokemon_passive_animation_timer,
                          wiggle_iteration,
                          points,
                          fight_animation_timer
                          ):
    """
    @returns: running, battle_active, battle_intro, current_intro, pokemon_passive_animation_timer, wiggle_iteration,animation_running, fight_animation_timer
    """
    
    running = True # Initiate running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif animation_running:
            None # Do nothing while animations are running- can't click anything!
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click is inside the text box
            if text_box_rect.collidepoint(event.pos):
                active = not active  # Toggle the text box activation
            else:
                active = False
            ############################################################################################
            # Can do collidepoints with the current_intro, which indicates what is already on screen
            move = fight_collide_points(MY_POKEMON_MOVES, fight_move_quadrants, event.pos) # Which move is used
            if current_intro == "FIGHT" and move is not None:
                current_intro = "MOVE"
                fight_animation_timer:float = pygame.time.get_ticks()
                battle_intro = f"{MY_POKEMON.name} used {move}!" + "\n" + all_moves[move]["flavortext"]("Your " + MY_POKEMON.name, "Enemy " + ENEMY_POKEMON.name) + MY_POKEMON.print_typing_effectiveness(ENEMY_POKEMON, all_moves[move]["type"], all_moves[move]["mvtype"])
                MY_POKEMON.find_mv_type(ENEMY_POKEMON, all_moves[move]) # Do damage, debuff etc.
                animation_running = True # Start animation
                # print(pygame.time.get_ticks())
            ############################################################################################

            
            # Test speed
            # if current_intro == "BATTLE_INTRO" and not ENEMY_POKEMON.test_speed(MY_POKEMON): # We are at the start and the enemy is faster
            #     current_intro = "ENEMY_TURN"
            # else:
            for i, rects in enumerate(option_button_rects):
                # option_words = ["FIGHT", "POKEMON", "BAG", "RUN"]
                if rects.collidepoint(event.pos):
                    print(option_words[i])
                    current_intro = option_words[i]
                    break

    # Fill the screen
    screen.fill(LINEN)

    # Draw the text box
    pygame.draw.rect(screen, BLACK, text_box_rect)

    # Draw the option box
    pygame.draw.rect(screen, WHITE, options_box_rect)
    pygame.draw.rect(screen, BLACK, options_box_rect, 2)  # Border

    ##############################################################################
    # THIS SHOULD BE DYNAMIC DEPENDENT ON THE OPTION BUTTON PRESSED
    # Render the battle intro
    if current_intro == "BATTLE_INTRO":
        battle_intro_print_text(battle_intro, text_box_rect, screen, font, active)
    elif current_intro == "FIGHT":
        fight_moves_print(moves=MY_POKEMON_MOVES, text_box_rect=text_box_rect, screen=screen,font=font, quadrants=fight_move_quadrants)
    elif current_intro == "POKEMON":
        print("POKEMON")
    elif current_intro == "BAG":
        print("BAG")
    elif current_intro == "RUN":
        print("RUN")
    elif current_intro == "MOVE" and not animation_running: # When animation stops, then it is the enemy´s turn
        current_intro = "ENEMY_TURN"
    elif current_intro == "MOVE":
        use_move_print(battle_intro, text_box_rect=text_box_rect, screen=screen, font=font)
    elif current_intro == "ENEMY_TURN":    
        print("ENEMY_TURN") 
        # Enemy turn
        # Pick a move
        chosen_move = random.randint(0, len(ENEMY_POKEMON.moves)-1)
        ENEMY_POKEMON.find_mv_type(MY_POKEMON, all_moves[ENEMY_POKEMON.moves[chosen_move]])
        battle_intro = f"Enemy {ENEMY_POKEMON.name} used {ENEMY_POKEMON.moves[chosen_move]}!" + "\n" + all_moves[ENEMY_POKEMON.moves[chosen_move]]["flavortext"]("Enemy " + ENEMY_POKEMON.name, "Your " +  MY_POKEMON.name) + ENEMY_POKEMON.print_typing_effectiveness(MY_POKEMON, all_moves[ENEMY_POKEMON.moves[chosen_move]]["type"], all_moves[ENEMY_POKEMON.moves[chosen_move]]["mvtype"])
        print(battle_intro)
        fight_animation_timer:float = pygame.time.get_ticks()
        animation_running = True # Start animation
        use_move_print(battle_intro, text_box_rect=text_box_rect, screen=screen, font=font)
        current_intro = "BATTLE_INTRO"
    # elif current_intro == "ENEMY_TURN" and not animation_running:
    #     current_intro = "BATTLE_INTRO"
    else:
        running = False #CRASH

    ###############################################################################
    # Render option text
    option_text_print(option_words, option_button_rects, options_box_rect, screen, spacing, font)        


    ###############################################################################
    # Render battle arena / platforms
    pygame.draw.circle(screen, FORESTGREEN, ENEMY_PLATFORM_POS, platform_radius)
    pygame.draw.circle(screen, FORESTGREEN, MY_POKEMON_PLATFORM_POS, platform_radius)

    # print(pokemon_passive_animation_timer)
    if pokemon_passive_animation_timer >= 5000: # Every ten frames (500 / 30 FPS)
        points, wiggle_iteration = increase_wiggle(wiggle, wiggle_iteration) # Makes the pokemon be dynamic and not static in one place
        screen.blit(render_pokemon(MY_POKEMON.name, (SCREEN_WIDTH + points[0],SCREEN_HEIGHT + points[1]), enemy=False, pokemon_scaling=pokemon_scaling), MY_POKEMON_POS)
        # Render Opponents pokemon
        screen.blit(render_pokemon(ENEMY_POKEMON.name, (SCREEN_WIDTH - points[0],SCREEN_HEIGHT + points[1]), enemy=True, pokemon_scaling=pokemon_scaling), ENEMY_POS)
        pokemon_passive_animation_timer = 0.0
    else:
        # Still draw the pokemon, but don't indrease wiggle
        points, _ = increase_wiggle(wiggle, wiggle_iteration) # Makes the pokemon be dynamic and not static in one place
        screen.blit(render_pokemon(MY_POKEMON.name, (SCREEN_WIDTH + points[0],SCREEN_HEIGHT + points[1]), enemy=False, pokemon_scaling=pokemon_scaling), MY_POKEMON_POS)
        # Render Opponents pokemon
        screen.blit(render_pokemon(ENEMY_POKEMON.name, (SCREEN_WIDTH - points[0],SCREEN_HEIGHT + points[1]), enemy=True, pokemon_scaling=pokemon_scaling), ENEMY_POS)
        pokemon_passive_animation_timer += 500#pygame.time.Clock.get_time()

    ################################################################################
    # Render Health Bar
    # First draw White box:
    pygame.draw.rect(screen, SNOW, MY_HEALTH_BOX_DIMENSIONS, border_radius=10)
    pygame.draw.rect(screen, SNOW, ENEMY_HEALTH_BOX_DIMENSIONS, border_radius=10)

    # Render names
    text_name = font.render(MY_POKEMON.name, True, BLACK)
    screen.blit(text_name, (MY_HEALTH_BOX_DIMENSIONS.x + 10, MY_HEALTH_BOX_DIMENSIONS.y + 10))
    text_name = font.render(ENEMY_POKEMON.name, True, BLACK)
    screen.blit(text_name, (ENEMY_HEALTH_BOX_DIMENSIONS.x + 10, ENEMY_HEALTH_BOX_DIMENSIONS.y + 10))
    # Render Level
    text_name = font.render("Lv." + str(MY_POKEMON.level), True, BLACK)
    screen.blit(text_name, (MY_HEALTH_BOX_DIMENSIONS.x + MY_HEALTH_BOX_DIMENSIONS.width - 75, MY_HEALTH_BOX_DIMENSIONS.y + 10))
    text_name = font.render("Lv." + str(ENEMY_POKEMON.level), True, BLACK)
    screen.blit(text_name, (ENEMY_HEALTH_BOX_DIMENSIONS.x + ENEMY_HEALTH_BOX_DIMENSIONS.width - 75, ENEMY_HEALTH_BOX_DIMENSIONS.y + 10))
    ###################################################################################
    # Render HP
    # Calculate percentages for Width calculations
    my_pokemon_hp_percent = max(0,float((int(MY_POKEMON.HP) / int(MY_POKEMON.MAX_HP))))
    if my_pokemon_hp_percent <= 0.1:
        my_color = RED
    elif my_pokemon_hp_percent <= 0.33:
        my_color = EARTH_ORANGE
    else:
        my_color = GREEN
    my_hp_display = pygame.Rect(20, 460, 260*my_pokemon_hp_percent, 20)
    my_hp_outline = pygame.Rect(19, 460, 260, 20)
    pygame.draw.rect(screen, my_color, my_hp_display, border_radius=5)
    # Black outline
    pygame.draw.rect(screen, BLACK, my_hp_outline, width=1, border_radius=5)

    # Display own pokemon health:
    health_info = f"HP: {MY_POKEMON.HP} / {MY_POKEMON.MAX_HP}"
    text_surface = font.render(health_info, True, BLACK)
    screen.blit(text_surface, (20, 480))


    # Enemy HP
    enemy_pokemon_hp_percent = max(0,float((int(ENEMY_POKEMON.HP) / int(ENEMY_POKEMON.MAX_HP))))
    if enemy_pokemon_hp_percent <= 0.1:
        my_color = RED
    elif enemy_pokemon_hp_percent <= 0.33:
        my_color = EARTH_ORANGE
    else:
        my_color = GREEN
    enemy_hp_display = pygame.Rect(SCREEN_WIDTH-280, 40, 260*enemy_pokemon_hp_percent, 20)
    enemy_hp_outline = pygame.Rect(SCREEN_WIDTH-281, 40, 260, 20)
    pygame.draw.rect(screen, my_color, enemy_hp_display, border_radius=5)
    pygame.draw.rect(screen, BLACK, enemy_hp_outline, width=1, border_radius=5) # Black outline

    # Move animations:
    if animation_running and (pygame.time.get_ticks() - fight_animation_timer) < ANIMATION_TIMER: # 5 seconds for animation
        # print("Animation Running!")
        None
    else:
        animation_running = False

    if not check_death(MY_POKEMON, ENEMY_POKEMON):
        battle_active = True
    else:
        battle_active = False

    return running, battle_active, battle_intro, current_intro, pokemon_passive_animation_timer, wiggle_iteration, animation_running, fight_animation_timer


def choose_pokemon_screen(screen: pygame.Surface, font: pygame.font, my_pokemons: list[Pokemon], enemy_pokemon_options: list[Pokemon] | Pokemon):
    """
    Choose my Pokemon
    """   
    screen.fill(BLACK)

    third_of_height = (SCREEN_HEIGHT // 3)
    half_width = (SCREEN_WIDTH // 2) 
    # Divide the screen in 6 squares - one for each potential of your pokemons
    quadrants = {
        0: pygame.Rect(0, 0, half_width, third_of_height),
        1: pygame.Rect(half_width + 2, 0, half_width, third_of_height),# 2 for black between them
        2: pygame.Rect(0, third_of_height + 2, half_width, third_of_height),# 2 for black between them
        3: pygame.Rect(half_width + 2, third_of_height + 2, half_width, third_of_height),
        4: pygame.Rect(0, third_of_height * 2 + 4, half_width, third_of_height),
        5: pygame.Rect(half_width + 2, third_of_height * 2 + 4, half_width, third_of_height)
    }



    for i in range(len(quadrants.keys())):
        quad = quadrants[i]
        pygame.draw.rect(screen, LINEN, quad, border_radius=5)

        if i < len(my_pokemons):
            position_of_current_pokemon = (quad.left + 10 , quad.top + 25)
            screen.blit(render_pokemon(my_pokemons[i].name, (SCREEN_WIDTH,SCREEN_HEIGHT), enemy=False, pokemon_scaling=pokemon_scaling), position_of_current_pokemon)

            text_surface = font.render(f"{my_pokemons[i].name}", True, pokemon_typing_to_color(my_pokemons[i].type))
            screen.blit(text_surface, (position_of_current_pokemon[0] + half_width // 2, position_of_current_pokemon[1] + third_of_height // 3))
            text_surface = font.render(f"Lv. {my_pokemons[i].level}", True, BLACK)
            screen.blit(text_surface, (position_of_current_pokemon[0] + half_width // 2, position_of_current_pokemon[1] + third_of_height // 3 + 36))
        else: # Dont draw pokemons if they don't exist
            continue

    if isinstance(enemy_pokemon_options, list):
        # Pick random pokemon as the enemy pokemon
        chosen_pok: int = random.randint(0, len(enemy_pokemon_options)-1)
        enemy_pokemon: Pokemon = enemy_pokemon_options[chosen_pok].copy_pokemon_class()
    else:
        enemy_pokemon: Pokemon = enemy_pokemon_options.copy_pokemon_class()

    # Buttons
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit Pygame
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(my_pokemons)): # Loop through pokemon to find out which one was pressed
                quad = quadrants[i]
                if quad.collidepoint(event.pos):
                    print(my_pokemons[i].name, "picked!")
                    return True, my_pokemons[i], True, enemy_pokemon # True last as the battle is starting


    return False, None, False, enemy_pokemon



def create_new_save_file(screen: pygame.Surface, font: pygame.font, temp_save_name: str, saved_games_folder: str = "saved_games"):
    """
    Create a new save_file from scratch
    """
    starter_pokemon = [squirtle, bulbasaur, charmander]

    # filling out the screen - choose your starting pokemon
    screen.fill(LINEN)
    slightly_bigger_font = pygame.font.Font(None, int(TEXT_SIZE * 1.3))
    text_surface = slightly_bigger_font.render(f"Write your name then choose a Pokemon", True, BLACK)
    text_rect = text_surface.get_rect()
    # Get difference such that I can center
    text_on_each_side = (SCREEN_WIDTH - text_rect.width) // 2
    screen.blit(text_surface, (text_on_each_side, SCREEN_HEIGHT // 20))

    # Name of your save_game_file
    text_surface = font.render(f"Name: {temp_save_name}", True, BLACK)
    text_rect = text_surface.get_rect()
    # Get difference such that I can center
    text_on_each_side = (SCREEN_WIDTH - text_rect.width) // 2
    screen.blit(text_surface, (text_on_each_side, SCREEN_HEIGHT // 8))
    
    fourth_of_screen = SCREEN_WIDTH // 4
    fourth_of_fourth = fourth_of_screen // 4
    fourth_of_height = SCREEN_HEIGHT // 4
    quadrants = {  
        0: pygame.Rect(fourth_of_fourth, (SCREEN_HEIGHT // 2) + fourth_of_height // 2, fourth_of_screen, fourth_of_height), # Start a bit inwards
        1: pygame.Rect(fourth_of_fourth * 2 + fourth_of_screen, SCREEN_HEIGHT // 2, fourth_of_screen, fourth_of_height),
        2: pygame.Rect(fourth_of_fourth * 3 + fourth_of_screen * 2, (SCREEN_HEIGHT // 2) + fourth_of_height // 2, fourth_of_screen, fourth_of_height)
    }


    for i, pok in enumerate(starter_pokemon):
        quad = quadrants[i]
        screen.blit(render_pokemon(pok.name, (SCREEN_WIDTH, SCREEN_HEIGHT), enemy=False, pokemon_scaling=pokemon_scaling), (quad.x,quad.y))
        text_surface = font.render(f"{pok.name}", True, pokemon_typing_to_color(pok.type))
        text_rect = text_surface.get_rect()
        # Get difference such that I can center
        text_on_each_side = (quad.width - text_rect.width) // 2
        screen.blit(text_surface, (quad.x + text_on_each_side, quad.top + quad.height))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit Pygame
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(quadrants.keys())): # Loop through saves / potential new saves
                quad = quadrants[i]
                if quad.collidepoint(event.pos) and len(temp_save_name.strip()) != 0:
                    save_the_game(poks=[starter_pokemon[i]], game_name=temp_save_name.strip(), saved_folder=saved_games_folder)
                    return temp_save_name.strip(), temp_save_name.strip(), [starter_pokemon[i]]

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                temp_save_name =  temp_save_name[:-1]
            elif len(temp_save_name) < 16:
                temp_save_name += event.unicode

    return temp_save_name, None, []


def load_saved_game_screen(screen: pygame.Surface, font: pygame.font, new_game: bool, saved_games_folder: str = "saved_games", temp_save_name: str = ""):
    """
    @param new_game: Flag to tell whether to go to game creation instead - otherwise load a game
    """
    if new_game:
        # Go to create screen instead
        # return [], None, True
        temp_save_name, game_name, pokemons = create_new_save_file(screen=screen, font=font, temp_save_name=temp_save_name, saved_games_folder=saved_games_folder)
        return pokemons, game_name, True, temp_save_name

    # Display all the saved games found
    directory = os.fsencode(saved_games_folder)
    saves_all = []
    for i, file in enumerate(os.listdir(directory)):
        save_name = os.fsdecode(file).split(".")[-2] # Only the name of the game
        saves_all.append(save_name)
        if i == 5: # Maximum 6 saved games at a time
            break


    # filling out the screen
    screen.fill(BLACK)

    third_of_height = (SCREEN_HEIGHT // 3)
    half_width = (SCREEN_WIDTH // 2) 
    # Divide the screen in 6 squares - one for each potential of your pokemons
    quadrants = {
        0: pygame.Rect(0, 0, half_width, third_of_height),
        1: pygame.Rect(half_width + 2, 0, half_width, third_of_height),# 2 for black between them
        2: pygame.Rect(0, third_of_height + 2, half_width, third_of_height),# 2 for black between them
        3: pygame.Rect(half_width + 2, third_of_height + 2, half_width, third_of_height),
        4: pygame.Rect(0, third_of_height * 2 + 4, half_width, third_of_height),
        5: pygame.Rect(half_width + 2, third_of_height * 2 + 4, half_width, third_of_height)
    }

    for i in range(len(quadrants.keys())):
        quad = quadrants[i]
        pygame.draw.rect(screen, LINEN, quad, border_radius=5)

        if i < len(saves_all):

            text_surface = font.render(f"Save {i+1}: {saves_all[i]}", True, BLACK)
            text_rect = text_surface.get_rect()
            # Get difference such that I can center
            screen.blit(text_surface, (quad.left + (text_rect.width // 2), quad.top + 25 + third_of_height // 3))
        else: # new_game creation
            text_surface = font.render(f"Create New Game", True, BLACK)
            text_rect = text_surface.get_rect()
            # Get difference such that I can center
            screen.blit(text_surface, (quad.left + (text_rect.width // 2), quad.top + 25 + third_of_height // 3))
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit Pygame
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(6): # Loop through saves / potential new saves
                quad = quadrants[i]
                if quad.collidepoint(event.pos):
                    if i < len(saves_all):
                        loaded_game = load_game(saves_all[i], save_folder=saved_games_folder)
                        game_name = loaded_game.get_game_name()
                        pokemons = loaded_game.get_pokemons()
                        print(saves_all[i], "loaded!\nGame name initialized:", game_name)
                        return pokemons, game_name, new_game, temp_save_name
                    else:
                        load_saved_game_screen(screen=screen, font=font, new_game=True, saved_games_folder=saved_games_folder, temp_save_name=temp_save_name)
                        return [], None, True, temp_save_name

    return [], None, new_game, temp_save_name
                    