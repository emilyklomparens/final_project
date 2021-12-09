import random
from typing import TYPE_CHECKING

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
        while self.turn_counter < 3:
            dice1 = random.randint(1,6)
            dice2 = random.randint(1,6)
            if dice1 == dice2:
                print ("You rolled a double, get out of jail for free")
                self.jail = False
            
            
            if self.difficulty == 0:
                output = random.randint(0,1)
                if output == 1:
                    self.jail = False
                    self.money -= 50
                    print("Paid to get out of jail")
                    
            elif self.difficulty == 1:
                if self.money > 50 and len(self.props_owned) > 1:
                    self.money -= 50
                    self.jail = False
                    print("Paid to get out of jail")
            
            self.turn_counter += 1
