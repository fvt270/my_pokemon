from Pokemon_class import Pokemon
import pickle
import os

class saved_game:
    def __init__(self, pokemons: list[Pokemon], game_name: str, saved_path: str | None = None):
        self.pokemons = pokemons
        self.game_name = game_name
        if saved_path is None:
            self.saved_path = "saved_games"
        else:
            self.saved_path = saved_path

    def save_game(self):
        saved_path = os.path.join(self.saved_path, self.game_name + ".pkl")
        with open(saved_path, 'wb') as file:
            pickle.dump(self, file)

    def get_pokemons(self) -> list[Pokemon]:
        return self.pokemons

    def get_game_name(self) -> str:
        return self.game_name
    
    def get_pokemon_names(self) -> str:
        pokes = ""
        for i, pok in enumerate(self.pokemons):
            if i + 1 == len(self.pokemons):
                ending = ""
            else:
                ending = ", "
            pokes += pok.name + ending
        return pokes
        

def save_the_game(poks: list[Pokemon], game_name: str, saved_folder: str | None):
    """
    Save the game with the saved_game() class
    """
    saved_game(poks, game_name, saved_path=saved_folder).save_game()

def load_game(game_name: str, save_folder: str = "saved_games") -> saved_game:
    # Load the class instance from the file
    saved_path = os.path.join(save_folder, game_name + ".pkl")
    with open(saved_path, 'rb') as file:
        loaded_instance = pickle.load(file)
    print(type(loaded_instance))
    return loaded_instance

