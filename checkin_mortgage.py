import random;
class Tester:
    """This is a class to test the code I've written. It has all its variables temporarily hardcoded,
    just so my two functions can work as if they were in our program.
    
    Attributes:
        easy(boolean): Whether the computer is on easy mode (True) or not (False).
        """
    def __init__(self, easy):
        self.easy = easy
        self.money = 1000 #The amount of money this player has
        
        #Temporarily hardcoded, {"Property_name" : mortgage_cost}
        self.properties = {"Prop1" : 80, "Prop2" : 100, "Prop4" : 70} #Properties owned that are not mortgaged
        self.mortgaged = {"Prop3": 120} #Properties owned that are already morgaged
        

def mortgage(player):
    """This function decides which property a computer player is going to mortgage.
     
    Args:
        player(object of a computer player): The computer player needing to mortgage."""

    if player.easy == True: #If it's in easy mode, it picks at random.
        property = random.choice(list(player.properties.keys()))
    else: #If it's hard mode, it picks highest valued mortgage.
        max_val = max(player.properties.values())
        property = list(player.properties.keys())[list(player.properties.values()).index(max_val)]

    #The property is added to mortgaged dictionary, 
    #the money is added, and the property is deleted from the properties list.
    player.mortgaged[property] = player.properties[property]
    player.money += player.properties[property]
    del player.properties[property]


def unmortgage(player):
    """This function decides which property a computer player is going to unmortgage.
     
    Args:
        player(object of a computer player): The computer player needing to mortgage."""
    
    #This function does the opposite of the above function.
    if player.easy == True:
        property = random.choice(list(player.mortgaged.keys()))
    else:
        max_val = max(player.mortgaged.values())
        property = list(player.mortgaged.keys())[list(player.mortgaged.values()).index(max_val)]
        
    player.properties[property] = player.mortgaged[property] 
    player.money -= player.properties[property]
    del player.mortgaged[property]