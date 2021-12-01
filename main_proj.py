class Player():
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.jail = False
        self.props_owned = 0
        self.turn_counter = 0

    def turn():
        #roll 
        #check jail
        #land on property
        # check who owns it 
        # buy or pay or not buy
        # update turn counter 

def jail(): 

class HumanPlayer(Player):
# user input for name

class ComputerPlayer(Player):
    def __init__(self, difficulty):
        self.name = "Computer"
        self.difficulty = difficulty
    


class Properties():

class GameState():
    #print each players money amount
    #number of turns left 
    # who is in jail
    # list proerties all proprties in order and indicate if sold 
