from random import randint
from math import isnan
import pandas as pd

class GameState:
    def __init__(self):
        self.board = pd.read_csv("board.csv")
   	 
    	#List of players currently in the game and a list of current players who lost
        self.current_players = []
        self.bankrupt_players = []
    
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





class Player():

    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.jail = False
        self.props_owned = []
        self.turn_counter = 0
        self.position = 0
        
    def turn():
        pass

class HumanPlayer(Player):

    def turn(self, state, other):
        print(state.board.head()
              )
        print(f"{self.name} has ${self.money}")
        print("Press enter to roll.")
        input()
        roll = 3
        print (f"{self.name} rolled {roll}")
        #Calculate new postion
        if self.position + roll > 39:
            self.position = (self.position + roll) % 39
        else:
            self.position += roll
        print (f"{self.name} landed on {state.get_cell(self.position, 'SpaceName')}")
        #Check if sold
        if (state.get_cell(self.position, "Owner") == other.name):
            self.money - state.get_current_rent(self.position)
            print(f"{other.name} owns this property, you owe ${state.get_current_rent(self.position)}\nPress enter to pay rent.")
            input()
            self.money -= state.get_current_rent(self.position)
            print(f"{self.name} now has ${self.money}")
        elif (state.get_cell(self.position, "Owner") == self.name):
            print(f"{self.name} already own this property.")
        elif (state.get_cell(self.position, "Owner") == "bank"):
            print(f"This property is for sale for ${state.get_cell(self.position, 'Price')}")
            buy = input(f"\n{self.name}, would you like to buy Y or N \n")
            if (buy == 'Y'):
                self.props_owned.append(state.get_cell(self.position, "SpaceName"))
                self.money -= state.get_cell(self.position, "Price")
            state.change_owner(self.position, self.name)
        else:
            if(state.get_cell(self.position, "SpaceName") == "Community Chest"):
                print(f"{self.name} landed on Community Chest")
            elif(state.get_cell(self.position, "SpaceName") == "Jail"):
                print(f"{self.name} landed on Jail")
            else:
                print(f"{self.name} landed on Chance")

        self.turn_counter = self.turn_counter + 1
        print(f"\n{state.board.head()}\n")
        
def Game():

    rounds = 0

    g = GameState()
    h1 = HumanPlayer("Player 1")
    h2 = HumanPlayer("Player 2")

    while rounds < 1:
        
        rounds += 1
        h1.turn(g, h2)
        h2.turn(g, h1)
    
    print("\nThe round limit was reached.")
    
    if h1.money > h2.money:
        print(f"{h1.name} has won!\n")
    elif h1.money < h2.money:
        print(f"{h2.name} has won!\n")
    else:
        print("The two players have tied.")
        
if __name__ == '__main__':
    Game()

