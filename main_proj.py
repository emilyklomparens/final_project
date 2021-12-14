import random as rand
from math import isnan
import pandas as pd

class Player():
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.jail = False
        self.props_owned = []
        self.jail_turn_counter = 0
        self.position = 0
        self.jail_cards = 0

    def turn():
        """Take a turn.
        
        Args:
            state (GameState): a snapshot of the current state of the game.
        
        Returns:
            str: the player's guess (a letter or a word).
        """
        raise NotImplementedError

class HumanPlayer(Player):
    def turn(self, state, other):
        print(f"{self.name} has ${self.money}")
        if (self.jail == False):
            print("Press enter to roll.")
            input()
            roll = rand.randint(1,12)
            print(f"{self.name} now has ${self.money}.")
            print (f"{self.name} rolled {roll}.")
            #Calculate new postion
            if self.position + roll > 39:
                self.position = (self.position + roll) % 39
                self.money += 200
            else:
                self.position += roll
            print (f"{self.name} landed on {state.get_cell(self.position, 'SpaceName')}.\n")
            #Check if sold
            if (state.get_cell(self.position, "Owner") == other.name):
                self.money - state.get_current_rent(self.position)
                print(f"{other.name} owns this property, you owe ${state.get_current_rent(self.position)}. \nPress enter to pay rent.")
                input()
                self.money -= state.get_current_rent(self.position)
                print(f"{self.name} now has ${self.money}.")
            elif (state.get_cell(self.position, "Owner") == self.name):
                print(f"{self.name} already own this property.")
            elif (state.get_cell(self.position, "Owner") == "bank"):
                print(f"This property is for sale for ${state.get_cell(self.position, 'Price')}.")
                buy = input(f"\n{self.name}, would you like to buy Y or N? \n")
                if (buy == 'Y'):
                    self.props_owned.append(state.get_cell(self.position, "SpaceName"))
                    self.money -= state.get_cell(self.position, "Price")
                    state.change_owner(self.position, self.name)
            else:
                if(state.get_cell(self.position, "SpaceName") == "Community Chest"):
                    # update when community chest is built
                    input()
                elif(state.get_cell(self.position, "SpaceName") == "Go To Jail"):
                    self.jail = True
                else:
                    #update when chance is built
                    input()
        else:
            self.get_out_of_jail()
    
    def get_out_of_jail(self):
        print(f"\n{self.name}, You are in jail.\nPress enter.")
        input()
        # 3 options 
        if (self.jail_cards >= 1):
            action = input(f"You have 3 options.\n1. Pay the $50 fine and get out of jail.\n2. Attempt to roll doubles. \n3. Use a Get Out Of Jail Free Card. (You have {self.jail_cards} Get Out Of Jail Free Card(s))\nEnter 1, 2, or 3\n")
        else:
            action = input(f"You have 2 options.\n1. Pay the $50 fine and get out of jail.\n2. Attempt to roll doubles.\nEnter 1 or 2.\n")
        # Pay fine
        if (action == '1'):
            print(f"You will pay the $50 fine and are now out of jail.")
            self.jail = False
            self.jail_turn_counter = 0
            self.money -= 50
            print(f"{self.name} now has ${self.money}.")
        # Roll
        elif (action == '2'):
            print("Press enter to roll. You have to roll doubles to get out of jail.")
            input()
            roll1 = rand.randint(1,6)
            roll2 = rand.randint(1,6)
            print(f"You rolled a {roll1} and a {roll2} \n")
            self.jail_turn_counter += 1
            if (roll1 == roll2):
                print(f"You rolled doubles! You are now out of jail.")
                self.jail= False
                self.jail_turn_counter = 0
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

#import random

class ComputerPlayer:
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
        self.money = 1500
        self.name = "Computer"
        self.jail = False
        self.props_owned = []
        self.turn_counter = 0
        self.position = 0
        self.jail_cards=0
        
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
        print(f"\n{self.name}, is in jail.")
        # 3 options 
        if (self.jail_cards >= 1):
            action = '3'
        else:
            if self.difficulty == 0:
                output = rand.randint(0,1)
                if output == 1:
                    action = '2'
                elif output == 0:
                    action = '1'
            elif self.difficulty == 1:
                if self.money > 50 and len(self.props_owned) > 1:
                    action = '1'
                else:
                    action = '2'
                
        # Pay fine
        if (action == '1'):
            print(f"You will pay the $50 fine and are now out of jail.")
            self.jail = False
            self.jail_turn_counter = 0
            self.money -= 50
            print(f"{self.name} now has ${self.money}.")
        # Roll
        elif (action == '2'):
            print("Press enter to roll. You have to roll doubles to get out of jail.")
            input()
            roll1 = rand.randint(1,6)
            roll2 = rand.randint(1,6)
            print(f"You rolled a {roll1} and a {roll2} \n")
            self.jail_turn_counter += 1
            if (roll1 == roll2):
                print(f"You rolled doubles! You are now out of jail.")
                self.jail= False
                self.jail_turn_counter = 0
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
            
              
            
    def turn(self, state, other):
        print(f"{self.name} has ${self.money}")
        if (self.jail == False):
            roll = rand.randint(1,12)
            print(f"{self.name} now has ${self.money}.")
            print (f"{self.name} rolled {roll}.")
            #Calculate new postion
            if self.position + roll > 39:
                self.position = (self.position + roll) % 39
                self.money += 200
            else:
                self.position += roll
            print (f"{self.name} landed on {state.get_cell(self.position, 'SpaceName')}.\n")
            #Check if sold
            if (state.get_cell(self.position, "Owner") == other.name):
                self.money - state.get_current_rent(self.position)
                print(f"{other.name} owns this property, you owe ${state.get_current_rent(self.position)}. \nPress enter to pay rent.")
                input()
                self.money -= state.get_current_rent(self.position)
                print(f"{self.name} now has ${self.money}.")
            elif (state.get_cell(self.position, "Owner") == self.name):
                print(f"{self.name} already own this property.")
            elif (state.get_cell(self.position, "Owner") == "bank"):
                print(f"This property is for sale for ${state.get_cell(self.position, 'Price')}.")
                
           #ai computerplayer makes a choice to buy the property or not
           if self.difficulty == 0:
               decision = rand.randint(0,1)
               if decision == 1:
                   buy = 'Y'
               elif decision == 0:
                   buy = 'N'
                    
           elif self.difficulty ==1:
               if state.get_cell(self.position, 'Price') < self.money and len(self.props_owned) > 0:
                   buy = 'Y'
               else:
                   buy = 'N'
                    
           if (buy == 'Y'):
                self.props_owned.append(state.get_cell(self.position, "SpaceName"))
                self.money -= state.get_cell(self.position, "Price")
                state.change_owner(self.position, self.name)
        else:
            self.get_out_of_jail()


    
class GameState:
    def __init__(self):
        self.board = pd.read_csv("board.csv")
        
        #List of players currently in the game and a list of current players who lost
        self.current_players = []
        self.bankrupt_players = []
        
        #List of Chance cards, used cards are popped into the "used" list and returned when all cards have been used.
        self.chance = ["Advance to Boardwalk", "Advance to Go (Collect $200)", "Advance to Illinois Avenue. If you pass Go, collect $200", 
                       "Advance to St. Charles Place. If you pass Go, collect $200", 
                       "Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled", 
                       "Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled", 
                       "Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times amount thrown.", 
                       "Bank pays you dividend of $50", "Get Out of Jail Free", "Go Back 3 Spaces", "Go to Jail. Go directly to Jail, do not pass Go, do not collect $200", 
                       "Make general repairs on all your property. For each house pay $25. For each hotel pay $100", "Speeding fine $15",
                       "Take a trip to Reading Railroad. If you pass Go, collect $200", "You have been elected Chairman of the Board. Pay each player $50", 
                       "Your building loan matures. Collect $150"]
        self.used_chance = []
        
        #List of community chest cards, used cards are popped into the "used" list and returned when all cards have been used.
        self.community_chest = ["Advance to Go (Collect $200)", "Bank error in your favor. Collect $200", "Doctor’s fee. Pay $50", "From sale of stock you get $50", 
                                "Get Out of Jail Free", "Go to Jail. Go directly to jail, do not pass Go, do not collect $200", "Holiday fund matures. Receive $100", 
                                "Income tax refund. Collect $20", "It is your birthday. Collect $10 from every player", "Life insurance matures. Collect $100", 
                                "Pay hospital fees of $100", "Pay school fees of $50", "Receive $25 consultancy fee", 
                                "You are assessed for street repair. $40 per house. $115 per hotel", "You have won second prize in a beauty contest. Collect $10",
                                "You inherit $100"]
        self.used_community_chest = []

    
    def get_property_overview(self, space_number): #Returns an fstring that represents a property card
        if space_number in [12, 28]:#Utilities
            return f"{self.get_space_name(space_number)}\nIf one \"Utilitiy\" is owned rent is 4 times amount shown on dice.\nIf both \"Utilities\" are owned rent is 10 times amount shown on dice.\nMortgage Value: $75\nCurrent Owner: {self.get_owner(space_number)}"
        elif space_number in [5,15,25,35]:#Railroad
            return f"{self.get_space_name(space_number)}\nRent: $25\nIf 2 Railroads are owned: $50\nIf 3 Railroads are owned: $100\nIf 4 Railroads are owned: $200\nMortgage Value: $100\nCurrent Owner: {self.get_owner(space_number)}"
        elif space_number in [4, 38]:#Fees
            return f"{self.get_space_name(space_number)}\nPay ${self.get_fee(space_number)}"
        elif self.checker(self.get_price(space_number)) == " NaN: This cell doesn't have a value :( ":#Every other space
            return f"{self.get_space_name(space_number)}"
        else:#Properties
            return f"{self.get_space_name(space_number)} ({self.get_color(space_number)})\nRent: ${self.get_rent(space_number)}\nWith 1 House: ${self.get_1_house_rent(space_number)}\nWith 2 Houses: ${self.get_2_house_rent(space_number)}\nWith 3 Houses: ${self.get_3_house_rent(space_number)}\nWith 4 Houses: ${self.get_4_house_rent(space_number)}\nWith Hotel: ${self.get_hotel_rent(space_number)}\nHouses cost ${self.get_house_cost(space_number)} each\nMortgage Vaue: ${self.get_mortgage_value(space_number)}\nCurrent Owner: {self.get_owner(space_number)}"
    
             
    #Calculates and returns the amount of rent that's due when landing on that space.
    #Hotels, houses, railroad ownership, utility ownership, and fees are all taken into account.
    #include a dice roll as the third param if calculating utility rent
    def get_current_rent(self, space_number, dice_roll=0):
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
                return "No Railroads owned"
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
            if house_num == 0:
                return self.checker(self.board.loc[space_number, "Rent"])
            elif house_num == 1:
                return self.checker(self.board.loc[space_number, "1HouseRent"])
            elif house_num == 2:
                return self.checker(self.board.loc[space_number, "2HouseRent"])
            elif house_num == 3:
                return self.checker(self.board.loc[space_number, "3HouseRent"])
            elif house_num == 4:
                return self.checker(self.board.loc[space_number, "4HouseRent"])
            elif house_num == 5:
                return self.checker(self.board.loc[space_number, "HotelRent"])
        

    def get_cell(self, space_number, column_name): #Returns the contents of a cell when given a space number(int) and a column name(string) 
        if column_name not in self.board.columns:
            print("Invalid column name.")
        else:
            return self.checker(self.board.loc[space_number, column_name])


    def get_space_number(self, space_name): #Give this method a SpaceName and it returns it's SpaceNumber
        dex = self.board[self.board["SpaceName"]==space_name].index.values
        if len(dex) > 2:
            return list(dex)
        else:
            return int(dex)
    
    
    def change_owner(self, space_number, player_name): #Changes the owner of the property to the given name. Owner is "bank" by default
        if self.checker(self.board.loc[space_number, "Owner"]) == " NaN: This cell doesn't have a value :( ":
            print("NaN: This space cannot have an owner, no changes were made.")
        else:
            self.board.loc[space_number, "Owner"] = player_name
    
    
    #When someone buys a house, call this to add to the property's "NumOfHouses"
    #if removing a house, call with a negative number to subtract
    # 5 houses = a hotel
    def change_houses(self, space_number, number_of_houses): 
        house_num =self.board.loc[space_number, "NumOfHouses"]
        if self.checker(house_num) == " NaN: This cell doesn't have a value :( ":
            print("NaN: This space cannot be given houses, no changes were made.")
        elif (house_num + number_of_houses) > 5 or (house_num + number_of_houses) < 0:
            print("Invalid number of houses: Properties can only have 0-5 houses, no changes were made.\n")
        else:
            self.board.loc[space_number, "NumOfHouses"] += number_of_houses
    

    def get_chance(self): #Returns a random Chance card
        if len(self.chance) == 0:
            self.chance = self.used_chance
            self.used_chance = []
        card = self.chance.pop(self.chance.index(random.choice(self.chance)))
        self.used_chance.append(card)
        return card
    
    def get_community_chest(self): #Returns a random Community Chest card
        if len(self.community_chest) == 0:
            self.community_chest = self.used_community_chest
            self.used_community_chest = []
        card = self.community_chest.pop(self.community_chest.index(random.choice(self.community_chest)))
        self.used_community_chest.append(card)
        return card
        

    def add_player(self, player_name): #Adds a player to the list of current players
        if player_name == "bank":
            print("Player name cannot be \"bank\"")
        self.current_players.append(player_name)
        
    def bankrupt_player(self, player_name): #Moves a player from the current player list to the bankrupt player list.
        self.current_players.pop(self.current_players.index(player_name))
        self.bankrupt_players.append(player_name)
    
    
    def checker(self, cell): #Won't be called outside of this class. This is used to prevent errors.
        if isinstance(cell, str) == False and isnan(cell):
            return " NaN: This cell doesn't have a value :( "
        elif isinstance(cell, float):
            return int(cell)
        else:
            return cell

def Game():
    
    rounds = 0
    
    g = GameState()
    h1 = HumanPlayer("Player 1")
    h2 = ComputerPlayer(0)
    
    while rounds < 10:
        rounds += 1
        h1.turn(g,h2)
        h2.turn(g,h1)
        
    if h1.money > h2.money:
        print(f"{h1.name} has won!")
    elif h1.money < h2.money:
        print(f"{h2.name} has won!")
    else:
        print("The two players have tied.")

if __name__ == '__main__':
    Game()
