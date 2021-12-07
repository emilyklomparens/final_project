from random import rand
class Player():
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.jail = False
        self.props_owned = []
        self.turn_counter = 0
        self.position = 0

    def turn():
        #roll 
        #check jail
        #land on property
        # check who owns it 
        # buy or pay or not buy
        # update turn counter 

def jail(): 
    

class HumanPlayer(Player):

    def turn(self, state):
        print(state)
        roll = rand.int(1,12)
        print (f"You rolled", {roll})
        #Calculate new postion 
        # wrap around 39 to 0
        #Check if sold 
        if ("property is sold to computer"):
            self.money - property.rent 
        elif ("player owns property"):
            print("You already own this property.")
        else:
            print(f"This property is for sale for", {property.price})
            buy = input(f"{self.name}, would you like to buy Y or N")
            if (buy == 'Y'):
                self.props_owned.add(property.name)
                self.money -= property.cost
        self.turn_counter = self.turn_counter + 1
    


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
