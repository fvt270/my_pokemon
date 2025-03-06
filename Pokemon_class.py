from Stats import *
import copy # To copy the class into a new class
import math
import random

class level_profile:
    """
    Class for handling how much dmg, hp, defense etc. is gained per level
    """
    def __init__(self, HP_per_level: float, dmg_per_level: float, defense_per_level: float, speed_per_level: float):
        """
        How much HP, dmg, defense, speed is gained per level for this profile
        """
        self.HP_per_level = HP_per_level
        self.dmg_per_level = dmg_per_level
        self.defense_per_level = defense_per_level
        self.speed_per_level = speed_per_level
    
    def test_legitimate_class(self):
        """
        Just a function to test whether this class can be called upon
        """
        return True

    def __find_which_table_attribute_belongs_to(self, attribute: float) -> int:
        for i in range(1,10):
            if math.isclose(1, attribute * i, rel_tol = 0.05, abs_tol = 0.05):
                return int(i)
        raise AttributeError("Error in handling attribute math table in which it belongs to.")

    def __float_to_int_calculation(self, attribute: float, level_to: int) -> int:
        if attribute < 1:
            # Less than one gain per level:
            tabel_den_passer_til = self.__find_which_table_attribute_belongs_to(attribute=attribute)
            if level_to % tabel_den_passer_til == 0:
                return 1 # Gain 1 attribute
            else:
                return 0
        elif attribute % 1 == 0: # A whole number
            return int(attribute)
        else: # Above 1, but not a whole number
            return int(1 + self.__float_to_int_calculation(attribute=attribute - 1, level_to=level_to)) # Recursively reduce the number
        

    def calculate_gain(self, level_to: int):
        """
        Calculate how much HP, dmg, defense, speed is gained on level up
        For instance: per level gain is 0.5 - meaning every second level, you get one whole
        """
        # Calculate health gain
        HP_gain = self.__float_to_int_calculation(self.HP_per_level, level_to=level_to)

        # Calculate dmg gain
        dmg_gain = self.__float_to_int_calculation(self.dmg_per_level, level_to=level_to)

        # Calculate defense gain:
        defense_gain = self.__float_to_int_calculation(self.defense_per_level, level_to=level_to)

        # Calculate speed gain:
        speed_gain = self.__float_to_int_calculation(self.speed_per_level, level_to=level_to)

        return HP_gain, dmg_gain, defense_gain, speed_gain



class Pokemon:
    def __init__(self, name: str, HP: int, MAX_HP: int, dmg: int, defense: int, speed: int, level:int, type: str, moves: list, level_profile: level_profile, xp: int = 0):
        self.name = name
        self.HP = HP
        self.MAX_HP = MAX_HP
        self.dmg = dmg
        self.defense = defense
        self.speed = speed
        self.level = level
        self.type = type
        self.moves = moves
        assert level_profile.test_legitimate_class() == True, "level_profile needs to be a level_profile class"
        self.level_profile = level_profile
        self.xp = xp

    def find_advantage(self, pokemon2, move_type) -> bool | None:
        # All equal to
        if move_type == "Fire" and pokemon2.type == "Grass":
            return True
        elif move_type == "Grass" and pokemon2.type == "Water":
            return True
        elif move_type == "Water" and pokemon2.type == "Fire":
            return True
        else:
            return None

    def type_handling(self, pokemon2, move_type):
        if self.find_advantage(pokemon2=pokemon2, move_type=move_type) is True:
            return 1.5 # Advantage
        elif self.find_advantage(pokemon2=pokemon2, move_type=move_type) is False:
            return 0.5 # Weakness
        else: #Returning None from self.find_advantage
            return 1 # Normal typing
        
    def print_typing_effectiveness(self, pokemon2, move_type: str, mvtype: str):
        """
        Return a str of whether the move is effective or not
        @param pokemon2: The pokemon being attacked
        @param move_type: The type of the move being used (Water, Fire, Grass etc.)
        @param mvtype: Type of move being used (Attack, Debuff, Buff etc.)
        @returns: String with \\n + the effectiveness 
        """
        advantage = self.find_advantage(pokemon2=pokemon2, move_type=move_type)
        if mvtype.lower() != "attack" or advantage is None:
            return ""
        elif advantage:
            return "\nIt was very effective!"
        elif not advantage:
            return "\nIt wasn't very effective..."
        else:
            raise ValueError



    def find_mv_type(self, pokemon2, move: dict):
        if move["mvtype"].lower() == "attack":
            dmg = move["dmg"]
            mv_type = move["type"]
            self.attack_move(pokemon2, dmg, mv_type)
        elif move["mvtype"].lower() == "debuff":
            dmg = move["dmg"]
            status = move["status"]
            self.debuff_move(pokemon2, dmg, status)

    def buff_move(self, dmg, status):
        """Buff user"""
        if status.lower() == "defense":
            # Lower defense by dmg, but not less that 0!
            if self.defense <= 0:
                self.defense = 0
                print(f"{self.name} tried to increase its defense, but it won't go any higher...")
            else:
                self.defense = max(self.defense + dmg, 0) # Never below 0!!!
                print(f"{self.name} increased its defense!")
        else:
            print("STATUS UNKOWN")

    def debuff_move(self, pokemon2, dmg, status):
        """Debuff enemy"""
        if status.lower() == "defense":
            # Lower defense by dmg, but not less that 0!
            if pokemon2.defense <= 0:
                pokemon2.defense = 0
                print(f"{self.name} tried to lower {pokemon2.name}'s defense, but it won't go any lower...")
            else:
                pokemon2.defense = max(pokemon2.defense - dmg, 0) # Never below 0!!!
                print(f"{self.name} lowered {pokemon2.name}'s defense!")
        else:
            print("STATUS UNKOWN")

    def attack_move(self, pokemon2, move_multiplier, move_typing):
        type_multiplier = self.type_handling(pokemon2, move_typing)
        dmg_func = max((self.dmg * type_multiplier * move_multiplier) - pokemon2.defense, 1) # At least one damage always!
        pokemon2.HP = pokemon2.HP - dmg_func
        if type_multiplier > 1:
            effectiveness = "\nIt was very effective!"
        elif type_multiplier < 1:
            effectiveness = "\nIt wasn't very effective..."
        else:
            effectiveness = ""
        print(f"{pokemon2.name} took {dmg_func} damage!{effectiveness}\n{pokemon2.name} has {pokemon2.HP} remaining HP!")

    def see_moves(self):
        print("Your moves:")
        for i, move in enumerate(self.moves):
            print(f"{i+1}: {move}")
        chosen = int(input("Choose your move!\n"))
        if chosen not in range(0, len(self.moves)+1):
            print("Invalid move choice")
            self.see_moves()
        else:
            return chosen - 1
    # def choose_move(self, move_number):
    #     used_move = self.moves[move_number]
    #     print(f"{self.name} used {used_move}!")
    #     return (all_moves[used_move]["dmg"], all_moves[used_move]["type"])
    def choose_move(self, move_number):
        used_move = self.moves[move_number]
        print(f"{self.name} used {used_move}!")
        return all_moves[used_move]

    def __increase_xp(self, xp):
        self.xp += xp

    def __calculate_xp(self, enemy_level):
        return 50 * enemy_level

    def gain_xp(self, enemy_pokemon):
        xp_gained = self.__calculate_xp(enemy_pokemon.level)
        self.__increase_xp(xp_gained)
        if self.xp >= 100*self.level:
            level_up = True
            self.__level_up()
        else:
            level_up = False
        return xp_gained, level_up

    def __level_up(self):
        self.xp = self.xp - (self.level * 100)
        self.level += 1
        HP_gain, dmg_gain, defense_gain, speed_gain = self.level_profile.calculate_gain(level_to=self.level)
        print(f"Your {self.name} gained HP_gain, dmg_gain, defense_gain, speed_gain: {HP_gain, dmg_gain, defense_gain, speed_gain}")
        self.MAX_HP += HP_gain
        self.HP += HP_gain
        self.dmg += dmg_gain
        self.defense += defense_gain
        self.speed += speed_gain


    def test_speed(self, other_pokemon):
        """
        Determine which pokemon is faster
        Does a coinflip to determine ties
        @returns: True if this pokemon is faster - false if the other is faster
        """
        if self.speed > other_pokemon.speed:
            return True
        elif other_pokemon.speed > self.speed:
            return False
        else:
            # Coinflip
            coin_flip = random.randint(1, 100)
            if coin_flip > 50:
                return True
            else:
                return False

    def copy_pokemon_class(self):
        return copy.deepcopy(self)
    
    def print_pokemon_stats(self):
        print(f"""{self.name}
HP: {self.HP}/{self.MAX_HP}
DMG: {self.dmg}
DEF: {self.defense}
LV: {self.level}
SPEED: {self.speed}""")
        