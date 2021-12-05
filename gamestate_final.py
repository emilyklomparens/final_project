from numpy import NaN, number
import pandas as pd

class GameState:
    def __init__(self):
        self.board = pd.read_csv(r"C:\Users\bman0\Documents\College\INST326\final_project\Board.csv")
        
    
    
    #call these methods with the player's current space number to get that space's info
    def get_space_name(self, space_number):
        return self.board.loc[space_number, "SpaceName"]
    
    def get_price(self, space_number):
        return self.board.loc[space_number, "Price"]
            
    def get_rent(self, space_number):
        return self.board.loc[space_number, "Rent"]
    

    #When someone buys a property, call this to add their name to the "Owner" column
    def change_owner(self, space_number, player_name):
        self.board.loc[space_number, "Owner"] = player_name
    
    #When someone buys a house, call this to add to the property's "NumOfHouses"
    #if removing a house, call with a negative number to subtract
    # 5 houses = a hotel
    def change_houses(self, space_number, number_of_houses):
        if (self.board.loc[space_number, "NumOfHouses"] + number_of_houses) > 5 or (
                self.board.loc[space_number, "NumOfHouses"] + number_of_houses) < 0:
            print("Invalid number of houses: Properties can only have 0-5 houses. No changes were made.\n")
        else:
            self.board.loc[space_number, "NumOfHouses"] += number_of_houses
    
        
        


test = GameState()

test.change_owner(1, "Player1")
test.change_houses(1, 4)
test.change_houses(1, -2)

print(test.board)