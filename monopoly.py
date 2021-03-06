"""A module for playing a game of Monopoly.
"""

import random as rand
from math import isnan
import pandas as pd
from argparse import ArgumentParser
import sys

class GameState:
    """Written by Brian McMahon.
    A class that represents the Monopoly board, property cards, and chance/community chest cards. 
    It uses an updatable pandas dataframe to store all of this information.
    
    Attributes:
        board(Pandas DataFrame): An updatable Pandas DataFrame imported from an excel document. 
            This is used to hold all information relating to the Monopoly board and property cards.
        current_players(list of strings): Used to store the names of all the players currently playing.
        bankrupt_players(list of strings): Used to store the names of all player who have lost.
        chance(list of strings): A list of every chance card
        used_chance(list of strings): A list of chance cards that have been used this game.
        community_chest(list of strings): A list of every community chest card.
        used_community_chest(list of strings): A list of community chest cards that have been used this game.
    """ 
    def __init__(self):
        self.board = pd.read_csv("board.csv")
        
        #List of players currently in the game and a list of current players who lost
        self.current_players = []
        self.bankrupt_players = []
        
        #List of Chance cards, used cards are popped into the "used" list and returned when all cards have been used.
        self.chance = ["Advance to Boardwalk", "Advance to Go (Collect $200)", 
                       "Advance to Illinois Avenue. If you pass Go, collect $200", 
                       "Advance to St. Charles Place. If you pass Go, collect $200", 
                       "Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, "\
                           "pay owner twice the rental to which they are otherwise entitled", 
                       "Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, "\
                           "pay owner twice the rental to which they are otherwise entitled", 
                       "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, "\
                           "throw dice and pay owner a total ten times amount thrown", 
                       "Bank pays you dividend of $50", "Get Out of Jail Free", "Go Back 3 Spaces", 
                       "Go to Jail. Go directly to Jail, do not pass Go, do not collect $200", 
                       "Speeding fine $15", "Take a trip to Reading Railroad. If you pass Go, collect $200", 
                       "You have been elected Chairman of the Board. Pay other player $50", 
                       "Your building loan matures. Collect $150"]
        self.used_chance = []
        
        #List of community chest cards, used cards are popped into the "used" list and returned when all cards have been used.
        self.community_chest = ["Bank error in your favor. Collect $200"]
        self.used_community_chest = ["Advance to Go (Collect $200)", "Bank error in your favor. Collect $200", 
                                     "Doctor???s fee. Pay $50", "From sale of stock you get $50", 
                                "Get Out of Jail Free", "Go to Jail. Go directly to jail, do not pass Go, do not collect $200", 
                                "Holiday fund matures. Collect $100", 
                                "Income tax refund. Collect $20", "It is your birthday. Collect $10 from the other player", 
                                "Life insurance matures. Collect $100", 
                                "Pay hospital fees of $100", "Pay school fees of $50", "Collect $25 consultancy fee", 
                                "You have won second prize in a beauty contest. Collect $10",
                                "You inherit $100"]
        
        
    def get_property_overview(self, space_number):
        """Written by Brian McMahon.
        Accesses the DataFrame and returns an fstring representation of a property card.
        
        Args: 
            space_number(int): The space number of the property whos card will be returned.
        
        Returns:
            (string): An fstring representation of a property card.
        """
        if space_number in [12, 28]:#Utilities
            return f"{self.get_space_name(space_number)}\nIf one \"Utilitiy\" is owned rent is 4 times amount shown on "\
                "dice.\nIf both \"Utilities\" are owned rent is 10 times amount shown on dice.\nMortgage Value: $75\nCurrent "\
                    "Owner: {self.get_owner(space_number)}"
        elif space_number in [5,15,25,35]:#Railroad
            return f"{self.get_space_name(space_number)}\nRent: $25\nIf 2 Railroads are owned: $50\nIf 3 Railroads are owned: "\
                        "$100\nIf 4 Railroads are owned: $200\nMortgage Value: $100\nCurrent Owner: {self.get_owner(space_number)}"
        elif space_number in [4, 38]:#Fees
            return f"{self.get_space_name(space_number)}\nPay ${self.get_fee(space_number)}"
        elif self.checker(self.get_price(space_number)) == "NaN":#Every other space
            return f"{self.get_space_name(space_number)}"
        else:#Properties
            return f"{self.get_space_name(space_number)} ({self.get_color(space_number)})\nRent: "\
                        "${self.get_rent(space_number)}\nWith 1 House: ${self.get_1_house_rent(space_number)}\nWith 2 Houses: "\
                        "${self.get_2_house_rent(space_number)}\nWith 3 Houses: ${self.get_3_house_rent(space_number)}\nWith 4 "\
                        "Houses: ${self.get_4_house_rent(space_number)}\nWith Hotel: ${self.get_hotel_rent(space_number)}\nHouses "\
                        "cost ${self.get_house_cost(space_number)} each\nMortgage Vaue: ${self.get_mortgage_value(space_number)}\nCu"\
                        "rrent Owner: {self.get_owner(space_number)}"
   
    def get_current_rent(self, space_number, dice_roll=0):
        """Written by Brian McMahon.
        Calculates and returns the amount of rent that's due when landing on a specified space.
        Hotels, houses, railroad ownership, utility ownership, and fees are all taken into account.
        
        Args:
            space_number(int): The space number of the property whos rent will be returned.
            dice_roll(int): This optional arg represents the dice roll needed when calculating utility rent.
                If it equals 0, it's not used.
                
        Returns:
            (int): The amount of rent owed
            (string): If there is not rent to return, it returns a string.
        """
        if space_number in [12, 28]:#Calculates utility rent
            if dice_roll == 0:
                return "A dice roll(int) needs to be included as a second parameter to calculate utility rent."
            elif self.get_owner(12) == self.get_owner(28):
                return (dice_roll * 10)
            else:
                return (dice_roll * 4)
            
        elif space_number in [5,15,25,35]:#Calculates Railroad rent
            rr = [self.get_owner(5), self.get_owner(15), self.get_owner(25), self.get_owner(35)]
            myrr = self.get_owner(space_number)
            counter = 0
            if myrr == rr[0]:
                counter += 1
            if myrr == rr[1]:
                counter += 1
            if myrr == rr[2]:
                counter += 1
            if myrr == rr[3]:
                counter += 1
            if counter == 0:
                return "No Railroads owned."
            elif counter == 1:
                return 25
            elif counter == 2:
                return 50
            elif counter == 3:
                return 100
            elif counter == 4:
                return 200
        
        elif space_number == 4: #Income tax
            return 200
        
        elif space_number == 38: #Luxury Tax
            return 100
        
        else: #Calculates normal property rent
            house_num = self.board.loc[space_number, "NumOfHouses"]
            hotel_num = self.board.loc[space_number, "NumOfHotels"]
            house = 0
            hotel = 0
            if house_num == 0 and hotel_num == 0:
                house = self.checker(self.board.loc[space_number, "Rent"])
            elif house_num == 1:
                house = self.checker(self.board.loc[space_number, "1HouseRent"])
            elif house_num == 2:
                house = self.checker(self.board.loc[space_number, "2HouseRent"])
            elif house_num == 3:
                house = self.checker(self.board.loc[space_number, "3HouseRent"])
            elif house_num == 4:
                house = self.checker(self.board.loc[space_number, "4HouseRent"])
            
            if hotel_num == 1:
                hotel = self.checker(self.board.loc[space_number, "HotelRent"])
                
            return house + hotel

    def get_cell(self, space_number, column_name): 
        """Written by Brian McMahon.
        Fetches the contents of a cell in the DataFrame based on a given space number and a column name.
        
        Args:
            space_number(int): The space number of the cell to be returned.
            column_name(string): The name of the column with the needed cell.
            
        Returns:
            (int): Returns an int if the desired cell is an int or a float.
            (string): Returns a string if desired cell is a string or if its empty.
            
        Side effects:
            Prints a message if the given column name is spelled wrong, for testing.
        """
        if column_name not in self.board.columns:
            print("Invalid column name.")
        else:
            return self.checker(self.board.loc[space_number, column_name])

    def get_space_number(self, space_name): 
        """Written by Brian McMahon.
        Takes the name of a space and returns it's space_number.
        
        Args:
            space_name(string): The name of the property whos number while be returned.
            
        Returns:
            (int): The properties space_number
            (list of int): For multiple spaces with same name, returns all space numbers.
        """
        dex = self.board[self.board["SpaceName"]==space_name].index.values
        if len(dex) > 2:
            return list(dex)
        else:
            return int(dex)
        
    def get_owner(self, space_number):
        """Written by Brian McMahon.
        Fetches name of the owner of the property at space_number.
        
        Args:
            space_number(int): The space number of the property whos owner name will be returned.
            
        Returns:
            (string): The name of the owner of the property.
        """
        return self.checker(self.board.loc[space_number, "Owner"])
    
    def change_owner(self, space_number, player_name): 
        """Written by Brian McMahon.
        Changes the owner of the property in the DataFrame to the given name, owner is "bank" by default.
        
        Args:
            space_number(int): The space number of the property whos owner name will be changed.
            player_name(string): The name to change the owner value to.
            
        Side effects:
            Changes a value inside the board attribute.
            Prints a message if the cell is empty.
        """
        if self.checker(self.board.loc[space_number, "Owner"]) == "NaN":
            print("NaN: This space cannot have an owner, no changes were made.")
        else:
            self.board.loc[space_number, "Owner"] = player_name
        
    def change_houses(self, space_number, number_of_houses):
        """Written by Brian McMahon.
        Alters the value in the DataFrame of the number of houses.
            If removing houses, call with negative number.
            5 houses equals 1 hotel
        Args:
            space_number(int): The space number of the property.
            number_of_houses(int): The number of houses to be added or removed
            
        Side effects:
            Changes a value inside the board attribute.
            Prints a message if the cell is empty.
        """ 
        house_num =self.board.loc[space_number, "NumOfHouses"]
        if self.checker(house_num) == "NaN":
            print("NaN: This space cannot be given houses, no changes were made.")
        elif (house_num + number_of_houses) > 5 or (house_num + number_of_houses) < 0:
            print("Invalid number of houses: Properties can only have 0-5 houses, no changes were made.\n")
        else:
            self.board.loc[space_number, "NumOfHouses"] += number_of_houses
 
    def get_chance(self): 
        """Written by Brian McMahon.
        Fetches a random Chance card and moves card to the used_chance list
        
        Returns:
            (string): The card's text
            
        Side effects:
            Removes a card from the chance attribute
            Adds a card to the used_chance attribute
        """
        if len(self.chance) == 0:
            self.chance = self.used_chance
            self.used_chance = []
        card = self.chance.pop(self.chance.index(rand.choice(self.chance)))
        self.used_chance.append(card)
        return card
    
    def get_community_chest(self): 
        """Written by Brian McMahon.
        Fetches a random Community Chest card and moves card to the used list.
        
        Returns:
            (string): The card's text
            
        Side effects:
            Removes a card from the community_chest attribute
            Adds a card to the used_community_chest attribute
        """
        if len(self.community_chest) == 0:
            self.community_chest = self.used_community_chest
            self.used_community_chest = []
        card = self.community_chest.pop(self.community_chest.index(rand.choice(self.community_chest)))
        self.used_community_chest.append(card)
        return card

    def add_player(self, player_name): 
        """Written by Brian McMahon.
        Adds a player to the list of current players
        
        Args:
            player_name(string): The player name to be added
        
        Side effects:
            Adds a string to the current_player attribute
            Prints a message if the added name is "bank"
        """
        if player_name == "bank":
            print("Player name cannot be \"bank\"")
        self.current_players.append(player_name)
        
    def bankrupt_player(self, player_name): 
        """Written by Brian McMahon.
        Moves a player from the current player list to the bankrupt player list.
        
        Args:
            player_name(string): The player name to be added
        
        Side effects:
            Removes a string from the current_player attribute
            Adds a string to the bankrupt_player attribute
        """
        self.current_players.pop(self.current_players.index(player_name))
        self.bankrupt_players.append(player_name)
    
    def checker(self, cell):
        """Written by Brian McMahon.
        A method exclusively called by other methods to prevent NaN errors when trying to access empty cells
        
        Args:
            cell(string, int, float, or NaN): The value of a given cell
            
        Returns:
            (int): The cell value passed in
            (string): Either the cell value passed in or "NaN" if it's empty
        """
        if isinstance(cell, str) == False and isnan(cell):
            return "NaN"
        elif isinstance(cell, float):
            return int(cell)
        else:
            return cell

        
class Player():
    """A parent class that represents one Player of monopoly and their attributes;
        HumanPlayer and ComputerPlayer are child classes that inherit from this 
        class.
    
    Attributes:
        name (string): the name of the player.
        money (int): the amount of money the player has.
        jail (boolean): whether the player is in jail or not.
        props_owned (list of strings): a list of strings comprising the names of
            each property the player owns.
        jail_turn_counter (int): how long the player has been in jail.
        position (int): what space number the player is on with respect to the
            board.
        jail_cards (int): number of get out of jail free cards a player has.
    """
    
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.jail = False
        self.props_owned = []
        self.jail_turn_counter = 0
        self.position = 0
        self.jail_cards = 0
        
    def o_spaces(self, state, other):
        """Written by Ady Weng.
        Handles Player interactions with 'special' spaces like
        Community Chest, Chance, and Income Tax.
        
        Args:
            state (GameState): a GameState object that represents the board
                and state of the game (e.g., what cards remain).
            other (Player): a Player object that represents the other player.
            
        Side effects:
            Prints what community chest or chance card a player has drawn.
            Edits the Player's 'position' and 'money' attribute based on the
                effects of the drawn card.
            Prints the Player's current position and money following the
                effects of the drawn card.
            Edits the Player's 'jail' attribute based on the effects of the
                drawn card.
            Edits the opposing Player's 'money' attribute based on the effects 
                of the drawn card.
            Enables the Player to amend the 'props_owned' attribute by
                allowing them to purchase some properties in accordance with 
                a drawn card.
        """
        
        if state.get_cell(self.position, "SpaceName") == "Chance":
            card = state.get_chance()
            print(f"{self.name} has drawn: {card}.")
            if card == "Advance to Boardwalk":
                self.position = 39
            elif card == "Advance to Go (Collect $200)":
                self.position = 0
                self.money += 200
            elif card == "Advance to Illinois Avenue. If you pass Go, collect $200":
                if self.position > 25:
                    self.money += 200
                self.position = 24
            elif card ==  "Advance to St. Charles Place. If you pass Go, collect $200":
                if self.position > 12:
                    self.money += 200
                self.position = 11
            elif card == "Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay owner twice the rental to which they are otherwise entitled":
                sn = self.position
                while "Railroad" not in state.get_cell(sn, "SpaceName") and "Short Line" not in state.get_cell(sn, "SpaceName"):
                    sn += 1
                    if sn > 39:
                        sn = sn % 39
                self.position = sn
                if state.get_owner(self.position) == self.name:
                    print("This is a railroad you own.")
                elif state.get_owner(self.position) == other.name:
                    print("This is a railroad your opponent owns. Pay twice.")
                    self.money -= 2 * state.get_current_rent(self.position)
                    other.money += 2 * state.get_current_rent(self.position)
                else:
                    print(f"{state.get_cell(self.position, 'SpaceName')} is for sale for ${state.get_cell(self.position, 'Price')}.")
                    if self.name != "Computer":
                        buy = input(f"\n{self.name}, would you like to buy Y or N? \n")
                        if (buy.upper() == 'Y'):
                            self.props_owned.append(state.get_cell(self.position, "SpaceName"))
                            self.money -= int(state.get_cell(self.position, "Price"))
                            state.change_owner(self.position, self.name)
                    else:
                        ran = rand.randint(0, 1)
                        if ran == 0:
                            self.props_owned.append(state.get_cell(self.position, "SpaceName"))
                            self.money -= int(state.get_cell(self.position, "Price"))
                            state.change_owner(self.position, self.name)
                        else:
                            print("Computer chose not to buy.")
            elif card == "Advance token to nearest Utility. If unowned, you may buy it from the Bank. "\
                        "If owned, throw dice and pay owner a total ten times amount thrown":
                sn = self.position
                while "Electric" not in state.get_cell(sn, "SpaceName") and "Water" not in state.get_cell(sn, "SpaceName"):
                    sn += 1
                self.position = sn
                if state.get_owner(self.position) == self.name:
                    print("This is an utility you own.")
                elif state.get_owner(self.position) == other.name:
                    print("This is an utility your opponent owns. Throw dice and pay owner 10x the amount thrown.")
                    mt = rand.randint(1, 12)
                    print(f"You rolled {mt}.")
                    self.money -= mt * 10
                    other.money += mt * 10
                else:
                    print(f"{state.get_cell(self.position, 'SpaceName')} is for sale for ${state.get_cell(self.position, 'Price')}.")
                    if self.name != "Computer":
                        buy = input(f"\n{self.name}, would you like to buy Y or N? \n")
                        if (buy.upper() == 'Y'):
                            self.props_owned.append(state.get_cell(self.position, "SpaceName"))
                            self.money -= int(state.get_cell(self.position, "Price"))
                            state.change_owner(self.position, self.name)
                    else:
                        ran = rand.randint(0, 1)
                        if ran == 0:
                            self.props_owned.append(state.get_cell(self.position, "SpaceName"))
                            self.money -= int(state.get_cell(self.position, "Price"))
                            state.change_owner(self.position, self.name)
                        else:
                            print("Computer chose not to buy.")
            elif card == "Bank pays you dividend of $50":
                self.money += 50
            elif card == "Get Out of Jail Free":
                self.jail_cards += 1
            elif card == "Go Back 3 Spaces":
                self.position -= 3
            elif card == "Go to Jail. Go directly to Jail, do not pass Go, do not collect $200":
                self.jail = True
                self.position = 10
                print("Yeah, that's rough buddy :/")
            elif card == "Speeding fine $15":
                self.money -= 15
            elif card == "Take a trip to Reading Railroad. If you pass Go, collect $200":
                if self.position > 6:
                    self.money += 200
                self.position = 5
            elif card == "You have been elected Chairman of the Board. Pay other player $50":
                self.money -= 50
                other.money += 50
            elif card == "Your building loan matures. Collect $150":
                self.money += 150
                
        if state.get_cell(self.position, "SpaceName") == "Community Chest":
            card = state.get_community_chest()
            print(f"{self.name} has drawn: {card}.")
            if card == "Advance to Go (Collect $200)":
                self.position = 0
                self.money += 200
            elif card == "Get Out of Jail Free":
                self.jail_cards += 1
                print(f"{self.name} now has {self.jail_cards} jail cards.")
            elif card == "Go to Jail. Go directly to jail, do not pass Go, do not collect $200":
                self.jail = True
                self.position = 10
                print("Yeah, that's rough buddy :/")
            elif card == "It is your birthday. Collect $10 from the other player":
                other.money -= 10
                self.money += 10
            else:
                amt = []
                for i in card:
                    if i.isdigit():
                        amt.append(i)
                if "Collect" in card or "collect" in card or "get" in card or "inherit" in card:
                    self.money += int("".join(amt))
                else:
                    self.money -= int("".join(amt))
                    
        if state.get_cell(self.position, "SpaceName") == "Income Tax":
            self.money -= 200

        print(f"{self.name} is now on {state.get_cell(self.position, 'SpaceName')} and has ${self.money}.")
        
    def mp_check(self, state, col):
        """Written by Ady Weng.
        Function to check whether a player has a monopoly over one color of
        properties.

        Args:
            player (Player): instance of Player class representing the player whose
                property was landed on.
            state (GameState): instance of the GameState class representing the
                board and its current state.
            col (string): a string representing the color of the landed-on property.

        Returns:
            boolean: whether the Player has a monopoly over the color property
                they are currently positioned on (true or false).
        """
        
        COLORS = {
            "brown": 2,
            "lightblue": 3,
            "pink": 3,
            "orange": 3,
            "red": 3,
            "yellow": 3,
            "green": 3,
            "darkblue": 2,
        }
        
        col_count = {
            "brown": 0,
            "lightblue": 0,
            "pink": 0,
            "orange": 0,
            "red": 0,
            "yellow": 0,
            "green": 0,
            "darkblue": 0,
        }
        
        self.col_mp = {
            "brown": False,
            "lightblue": False,
            "pink": False,
            "orange": False,
            "red": False,
            "yellow": False,
            "green": False,
            "darkblue": False,            
        }
        
        if col != "NaN":
            for i in self.props_owned:
                if state.get_cell(state.get_space_number(i), "Color") == col:
                    col_count[col] += 1
                
            if COLORS[col] == col_count[col]:
                self.col_mp[col] = True
            
            return self.col_mp[col]

class HumanPlayer(Player):
    """ This class represents a Human Player of the game. This class is the child 
    class of the Player Class.
    
        Args: (same as Player Class)
        name (string): the name of the player.
        money (int): the amount of money the player has.
        jail (boolean): whether the player is in jail or not.
        props_owned (list of strings): a list of strings comprising the names of
        each property the player owns.
        jail_turn_counter (int): how long the player has been in jail.
        position (int): what space number the player is on with respect to the board.
        jail_cards (int): number of get out of jail free cards a player has.
    """
    
    def turn(self, state, other):
        """
        Written by Emily Klomparens. 
        This method represents one player turn.
        
        Args:
        state (object): the state of the game
        other (object): the other player of the game
                        
        Side effects:
        Changes attributes of both players depending on actions in the turn.
        """
        # Checks if player is in jail at the start of the turn
        if (self.jail == False):
            print(f"{self.name}, press enter to roll.")
            input()
            # Simulates one roll
            roll1 = rand.randint(1,6)
            roll2 = rand.randint(1,6)
            roll =  roll1 + roll2
            # Prints roll outcome
            print(f"{self.name} has has ${self.money}.")
            print (f"{self.name} rolled {roll}.")
            #Calculates new postion
            if self.position + roll > 39:
                self.position = (self.position + roll) % 39
                self.money += 200
            else:
                self.position += roll
            print (f"{self.name} landed on {state.get_cell(self.position, 'SpaceName')}.\n")
            # Checks type of space
            # Space is owned by opponent
            if (state.get_cell(self.position, "Owner") == other.name):
                print(f"{other.name} owns this property, you owe ${state.get_current_rent(self.position)}. \nPress enter to pay rent.")
                input()
                self.money -= state.get_current_rent(self.position)
                other.money += state.get_current_rent(self.position)
                print(f"{self.name} now has ${self.money}.")
            # Space is already owned by the player 
            elif (state.get_cell(self.position, "Owner") == self.name):
                print(f"{self.name} already own this property.")
                if self.mp_check(state, state.get_cell(self.position, "Color")) == True:
                    buy = input("Would you like to buy a house or hotel for this property? Y or N? \n")
                    if buy.upper() == 'Y':
                        self.buy_hs(state)
            elif (state.get_cell(self.position, "Owner") == "bank"):
                print(f"{state.get_cell(self.position, 'SpaceName')} is for sale for ${state.get_cell(self.position, 'Price')}.")
                buy = input(f"\n{self.name}, would you like to buy Y or N? \n")
                # The player buys the property landed on
                if (buy.upper() == 'Y'):
                    self.props_owned.append(state.get_cell(self.position, "SpaceName"))
                    self.money -= int(state.get_cell(self.position, "Price"))
                    state.change_owner(self.position, self.name)
                    print(f"{self.name} now has ${self.money}.")
                    if state.get_cell(self.position, "Color") != "NaN":
                        if self.mp_check(state, state.get_cell(self.position, "Color")) == True:
                            buy = input("Would you like to buy a house or hotel for this property? Y or N? \n")
                            if buy.upper() == 'Y':
                                self.buy_hs(state)
                elif (buy == 'N'):
                        print ("The choice is made to not purchase.")
                else:
                    print("Try again.")
                    buy = input(f"\n{self.name}, would you like to buy Y or N? \n")
            # Space is special
            else:
                if (state.get_cell(self.position, "SpaceName") == "Community Chest" or state.get_cell(self.position, "SpaceName") == "Chance" or
                  state.get_cell(self.position, "SpaceName") == "Income Tax"):
                    self.o_spaces(state, other)
                elif (state.get_cell(self.position, "SpaceName") == "Go To Jail"):
                    self.jail = True
                    self.position = 10
                elif (state.get_cell(self.position, "SpaceName") == "Free Parking" or state.get_cell(self.position, "SpaceName") == "Jail"):
                    pass
            
            # Sell your own property to the bank: A similar method to mortgaging. Written by Anshu 
            if (state.get_cell(self.position, "Owner")== self.name) and (state.get_cell(self.position, "MortgageValue") != None):
                ques = input("Would you like to sell your property? Y or N \n")
                if ques.upper() == "Y":
                    self.money += int(state.get_cell(self.position, "MortgageValue"))
                    state.change_owner(self.position, "Bank")
                    print(f"{self.name} now has ${self.money}.")
                elif ques.upper() != "N":
                    print("Try again.")
                    ques = input("Would you like to sell your property? Y or N \n")
        # Player is in jail
        else:
            self.get_out_of_jail()
            
    def buy_hs(self, state):
        """Written by Ady Weng.
        A class for allowing the HumanPlayer to purchase properties.
        
        Args:
            state (GameState): an instance of the GameState object representing
                the board and its current state.
        
        Side effects:
            Prints information concerning the prerequisites for buying hotels.
            Edits the Player's 'money' attribute to reflect that a house or
                hotel was purchased (when applicable).
            Prints out how many houses/hotel a Player has on a property.
            Prints out how much money a Player has following a purchase.
            Prints out reasoning as to why a purchase may have been rejected.
            Prints an "invalid input" statement when the program does not
                recognize an input to a prompt.
        """
        if (state.get_cell(self.position, "NumOfHouses")) != "NaN":
            print("Hotels replace houses on a property. You must have a house to buy a hotel.")
            which = input("Would you like to buy a house/house(s) for this property or a hotel? 1 for house, 2 for hotel. \n")
            if which == "1":
                num = input(f"How many houses would you like to buy (1-4)? House Price: {state.get_cell(self.position, 'HouseCost')} \n")
                calc_price = int(state.get_cell(self.position, 'HouseCost')) * int(num)
                confirm = input(f"Are you sure you'd like to buy {num} houses for ${calc_price} Y/N? \n")
                if confirm == 'Y' and self.money - calc_price > 0 and int(num) < 5:
                    state.change_houses(self.position, int(num))
                    self.money -= calc_price
                    print(f"You now have {state.get_cell(self.position, 'NumOfHouses')} houses for {state.get_cell(self.position, 'SpaceName')}.")
                    print(f"{self.name} now has ${self.money}.")
                else:
                    print("You don't have enough money; alternatively, too many houses! \n")
                    pass
            elif which == "2":
                print(state.get_cell(self.position, "NumOfHouses"))
                print(state.get_cell(self.position, "NumOfHotels"))
                if state.get_cell(self.position, "NumOfHouses") > 0 and state.get_cell(self.position, "NumOfHotels") == 0:
                    confirm = input(f"Are you sure you'd like to buy a hotel for ${state.get_cell(self.position, 'HouseCost')} Y/N? \n")
                    if confirm == "Y":
                        state.change_hotels(self.position, 1)
                        self.money -= state.get_cell(self.position, 'HouseCost')
                        state.change_houses(self.position, -1)
                        print(f"You now have a new hotel for {state.get_cell(self.position, 'SpaceName')}.")
                        print(f"{self.name} now has ${self.money}.")
                else:
                    print("Not enough houses; alternatively, only one hotel allowed! \n")
                    pass
            else:
                print("Invalid input!")
    
    def get_out_of_jail(self):
        """
        Written by Emily Klomparens. 
        This method represents being in jail. The player interacts with this method
        until released from jail. The player has the option to use a get out of jail free card 
        if avaiable, pay the $50 fine, or attempt to roll doubles. If the player does not 
        roll doubles in 3 turns the player has to print the fine automatically.
    
        Side effects:
        Changes attributes of both players depending on actions chosen.
        """
        print(f"\n{self.name} is in jail.\nPress enter.")
        input()
        
        # 3 options if player has a get out of jail free card
        if (self.jail_cards >= 1):
            action = input(f"You have 3 options.\n1. Pay the $50 fine and get out of jail.\n2. Attempt to roll doubles. \n3. "\
                "Use a Get Out Of Jail Free Card. (You have {self.jail_cards} Get Out Of Jail Free Card(s))\nEnter 1, 2, or 3\n")
        # 2 options otherwise
        else:
            action = input(f"You have 2 options.\n1. Pay the $50 fine and get out of jail.\n2. Attempt to roll doubles.\nEnter 1 or 2.\n")  
        # Pay fine
        if (action == '1'):
            print(f"You will pay the $50 fine and are now out of jail.")
            self.jail = False
            self.jail_turn_counter = 0
            self.money -= 50
            print(f"{self.name} now has ${self.money}.")
        # Roll doubles
        elif (action == '2'):
            print("Press enter to roll. You have to roll doubles to get out of jail.")
            input()
            roll1 = rand.randint(1,6)
            roll2 = rand.randint(1,6)
            print(f"You rolled a {roll1} and a {roll2} \n")
            self.jail_turn_counter += 1
            # Player rolls doubles
            if (roll1 == roll2):
                print(f"You rolled doubles! You are now out of jail.")
                self.jail = False
                self.jail_turn_counter = 0
            # Player does not roll doubles
            else: 
                print(f"You did not roll doubles. You are still in jail. You have {3-self.jail_turn_counter} attempts to roll left.")
                if (self.jail_turn_counter == 3):
                    print(f"Since you did not roll doubles in 3 turns, you have to pay the $50 fine.")
                    self.jail = False
                    self.jail_turn_counter = 0
                    self.money -= 50
                    print(f"{self.name} now has ${self.money}.")        
        # Use get out of jail free card
        else:
            print(f"You are using your Get Out Of Jail Free Card.")
            self.jail = False
            self.jail_cards -= 1
            print(f"You now have {self.jail_cards} Get Out Of Jail Free Card(s)")
            self.jail_turn_counter = 0

class ComputerPlayer(Player):
    """
    It represents the game status of a computer player.
    
    """
    def __init__(self, difficulty):
        """
        Computerplayer is a class that functions as another player in the game.
        There are varying levels of difficulty avaliable, and for initialization
        , you need money amount and the difficulty (0 or 1).
        
        Args:
            difficulty, a value from 0 (easy) to 1 (hard)
                        
        Side effects:
            changes attributes of self object
        """
                
        self.difficulty = difficulty
        self.name = "Computer"
        self.money = 1500
        self.jail = False
        self.props_owned = []
        self.jail_turn_counter = 0
        self.position = 0
        self.jail_cards = 0
        
    def turn(self, state, other):
        """
        A modification of the turn method, except during the game, 
        the computerplayer automatically makes decisions on whether or not to sell/buy property
        
        Args:
        State: The gamestate of the file
        Other: The other player
        """
        if (self.jail == False):
            roll1 = rand.randint(1,6)
            roll2 = rand.randint(1,6)
            roll =  roll1 + roll2
            print(f"{self.name} has ${self.money}.")
            print(f"{self.name} rolled {roll}.")
            
            #Calculate new postion
            if self.position + roll > 39:
                self.position = (self.position + roll) % 39
                self.money += 200
            else:
                self.position += roll
            print (f"{self.name} landed on {state.get_cell(self.position, 'SpaceName')}.")
            
            #Check if sold
            if (state.get_cell(self.position, "Owner") == other.name):
                print(f"{other.name} owns this property, {self.name} owes ${state.get_current_rent(self.position)}.")
                self.money -= int(state.get_current_rent(self.position))
                other.money += int(state.get_current_rent(self.position))
                print(f"{self.name} now has ${self.money}.")
            elif (state.get_cell(self.position, "Owner") == self.name):
                print(f"{self.name} already own this property.")
                if state.get_cell(self.position, "Color") != "NaN":
                    if self.mp_check(state, state.get_cell(self.position, "Color")) == True:
                        self.buy_hs(state)
            elif (state.get_cell(self.position, "Owner") == "bank"):
                print(f"{state.get_cell(self.position, 'SpaceName')} is for sale for ${state.get_cell(self.position, 'Price')}.") 
                if self.difficulty == 0:
                    decision = rand.randint(0,1)
                    if decision == 1:
                        print(f"{self.name} bought this property.")
                        self.props_owned.append(state.get_cell(self.position, "SpaceName"))
                        self.money -= int(state.get_cell(self.position, "Price"))
                        state.change_owner(self.position, self.name)
                        print(f"{self.name} now has ${self.money}.")
                        self.buy_hs(state)
                    else:
                        print(f"{self.name} did not buy this property.")
                elif self.difficulty == 1:               
                    if self.money > 2*int(state.get_cell(self.position, "Price")):
                        print(f"{self.name} bought this property.")
                        self.props_owned.append(state.get_cell(self.position, "SpaceName"))
                        self.money -= int(state.get_cell(self.position, "Price"))
                        state.change_owner(self.position, self.name)
                        print(f"{self.name} now has ${self.money}.")
                        self.buy_hs(state)
                    else:
                        print(f"{self.name} did not buy this property.")
                            
                else:
                    print("There was no difficulty specified")   
                    #else:
                        #print(f"{self.name} did not buy this property.")
            else:
                if(state.get_cell(self.position, "SpaceName") == "Community Chest" or state.get_cell(self.position, "SpaceName") == "Chance" or
                  state.get_cell(self.position, "SpaceName") == "Income Tax"):
                    self.o_spaces(state, other)
                elif(state.get_cell(self.position, "SpaceName") == "Go To Jail"):
                    self.jail = True
                    self.position = 10
                elif (state.get_cell(self.position, "SpaceName") == "Free Parking" or state.get_cell(self.position, "SpaceName") == "Jail"):
                    pass
                
            #The computer sells property to the bank if low on money
            if (state.get_cell(self.position, "Owner")== self.name) and (state.get_cell(self.position, "MortgageValue") != None):
                if self.money < 200:
                    self.money += int(state.get_cell(self.position, "MortgageValue"))
                    state.change_owner(self.position, "Bank")
                    print(f"{self.name} now has ${self.money}.")
                    print(f"""{state.get_cell(self.position, "Owner")} is the new property owner""")
        else:
            self.get_out_of_jail()
            
    def buy_hs(self, state):
        """Written by Ady Weng.
        A class for allowing the ComputerPlayer to purchase properties.
        
        Args:
            state (GameState): an instance of the GameState object representing
                the board and its current state.
        
        Side effects:
            Prints information concerning the prerequisites for buying hotels.
            Edits the Player's 'money' attribute to reflect that a house or
                hotel was purchased (when applicable).
            Prints out how many houses/hotel a Player has on a property.
            Prints out how much money a Player has following a purchase.
            Prints out reasoning as to why a purchase may have been rejected.
            Prints an "invalid input" statement when the program does not
                recognize an input to a prompt.
        """

        if self.difficulty == 0:
            ch = rand.randint(0, 1)
            if ch == 0:
                if (state.get_cell(self.position, "NumOfHouses")) != "NaN":
                    num = rand.randint(1, 4)
                    calc_price = int(state.get_cell(self.position, 'HouseCost')) * int(num)
                    if self.money - calc_price > 0 and int(num) < 5:
                        state.change_houses(self.position, int(num))
                        self.money -= calc_price
                        print(f"Computer bought {state.get_cell(self.position, 'NumOfHouses')} houses for {state.get_cell(self.position, 'SpaceName')}.")
                        print(f"{self.name} now has ${self.money}.")
            elif ch == 1:
                if (state.get_cell(self.position, "NumOfHouses")) != "NaN" and (state.get_cell(self.position, "NumOfHotels")) != "NaN":
                    if int(state.get_cell(self.position, "NumOfHouses")) > 0 and int(state.get_cell(self.position, "NumOfHotels")) == 0:
                        state.change_hotels(self.position, 1)
                        self.money -= state.get_cell(self.position, 'HouseCost')
                        state.change_houses(self.position, -1)
                        print(f"Computer bought a new hotel for {state.get_cell(self.position, 'SpaceName')}.")
                        print(f"{self.name} now has ${self.money}.")
                    else:
                        print("Computer doesn't have enough money; alternatively, too many houses! \n")
                    pass
        elif self.difficulty == 1:
            if (state.get_cell(self.position, "NumOfHouses")) != "NaN" and (state.get_cell(self.position, "NumOfHotels")) != "NaN":
                if int(state.get_cell(self.position, "NumOfHouses")) > 0 and int(state.get_cell(self.position, "NumOfHotels")) == 0:
                    if int(state.get_cell(self.position, "NumOfHouses")) == 4:
                        state.change_hotels(self.position, 1)
                        self.money -= int(state.get_cell(self.position, 'HouseCost'))
                        state.change_houses(self.position, -1)
                        print(f"Computer bought a new hotel for {state.get_cell(self.position, 'SpaceName')}.")
                        print(f"{self.name} now has ${self.money}.")
                    else:
                        num = rand.randint(1, 4)
                        calc_price = int(state.get_cell(self.position, 'HouseCost')) * int(num)
                        if self.money - calc_price > 0 and int(num) < 5:
                            state.change_houses(self.position, int(num))
                            self.money -= calc_price
                            print(f"Computer bought {state.get_cell(self.position, 'NumOfHouses')} houses for {state.get_cell(self.position, 'SpaceName')}.")
                            print(f"{self.name} now has ${self.money}.")
                else:
                    print("Not enough houses; alternatively, only one hotel allowed! \n")
                    pass
        else:
            print("Invalid input!")
        
    def get_out_of_jail(self):
        """
        This function will determine whether the Computer should pay to get out 
        of jail . First, it rolls a pair of dice three
        times, and if any of them are a double, bail is free.
        
        The difficulty the user initialized will determine whether the bail 
        behavior is intelligent or random.
        
        Returns: Output of whether computer should pay to get out of jail.
        May also return getting out of jail for free.
        
        """
        print(f"\n{self.name} is in jail.")
        
        # 3 options 
        if (self.jail_cards >= 1):
            print(f"{self.name} are using your Get Out Of Jail Free Card.")
            self.jail = False
            self.jail_cards -= 1
            print(f"{self.name} now have {self.jail_cards} Get Out Of Jail Free Card(s)")
            self.jail_turn_counter = 0
        else:
            if self.difficulty == 0:
                output = rand.randint(0,1)
                if output == 1:
                    roll1 = rand.randint(1,6)
                    roll2 = rand.randint(1,6)
                    print(f"{self.name} rolled a {roll1} and a {roll2}.\n")
                    self.jail_turn_counter += 1
                    if (roll1 == roll2):
                        print(f"{self.name} rolled doubles! {self.name} is now out of jail.")
                        self.jail= False
                        self.jail_turn_counter = 0
                    else: 
                        print(f"{self.name} did not roll doubles. {self.name} is still in jail. {self.name} has {3-self.jail_turn_counter} attempts to roll left.")
                        if (self.jail_turn_counter == 3):
                            print(f"Since {self.name} did not roll doubles in 3 turns, {self.name} have to pay the $50 fine.")
                            self.jail = False
                            self.jail_turn_counter = 0
                            self.money -= 50
                            print(f"{self.name} now has ${self.money}.")
                elif output == 0:
                    print(f"{self.name} paid the $50 fine and is now out of jail.")
                    self.jail = False
                    self.jail_turn_counter = 0
                    self.money -= 50
                    print(f"{self.name} now has ${self.money}.")
            elif self.difficulty == 1:
                if self.money > 50 and len(self.props_owned) > 1:
                    print(f"{self.name} paid the $50 fine and is now out of jail.")
                    self.jail = False
                    self.jail_turn_counter = 0
                    self.money -= 50
                    print(f"{self.name} now has ${self.money}.")
                else:
                    roll1 = rand.randint(1,6)
                    roll2 = rand.randint(1,6)
                    print(f"{self.name} rolled a {roll1} and a {roll2}.\n")
                    self.jail_turn_counter += 1
                    if (roll1 == roll2):
                        print(f"{self.name} rolled doubles! {self.name} is now out of jail.")
                        self.jail= False
                        self.jail_turn_counter = 0
                    else: 
                        print(f"{self.name} did not roll doubles. {self.name} is still in jail. {self.name} has {3-self.jail_turn_counter} attempts to roll left.")
        if (self.jail_turn_counter == 3):
            print(f"Since {self.name} did not roll doubles in 3 turns, {self.name} have to pay the $50 fine.")
            self.jail = False
            self.jail_turn_counter = 0
            self.money -= 50
            print(f"{self.name} now has ${self.money}.")

def Game(difficulty, playername):
    """Written by Ady Weng.
    A class enabling the game to be set up and run.
    
    Args:
        difficulty (int): how intelligent the ComputerPlayer will be (assumes
            values of 0 or 1 for random and intelligent, respectively).
        playername (string): the name of the HumanPlayer.
        
    Side effects:
        Prints which player has won or tied.
    """

    rounds = 0
    
    g = GameState()
    h1 = HumanPlayer(playername)
    h2 = ComputerPlayer(difficulty)
    
    while rounds < 10:
        rounds += 1
        h1.turn(g,h2)
        print('\n------------------------------------------\n')
        print(g.board.head())
        h2.turn(g,h1)
        print('\n------------------------------------------\n')
        
    if h1.money > h2.money:
        print(f"{h1.name} has won!")
    elif h1.money < h2.money:
        print(f"{h2.name} has won!")
    else:
        print("The two players have tied.")

def parse_args(arglist):
    """ Parse command-line arguments.
    
    Expect these mandatory arguments:
        -ComputerDifficulty
        -PlayerName
    
    Args:
        arglist (list of str): arguments from the command line.
    
    Returns:
        namespace: the parsed arguments, as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument("ComputerDifficulty", type=int, help="Enter 0 or 1 for computer difficulty")
    parser.add_argument("PlayerName", type=str, help="Enter your name here")
    return parser.parse_args(arglist)

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    Game(args.ComputerDifficulty, playername=args.PlayerName)
