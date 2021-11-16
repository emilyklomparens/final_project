import random
from typing import TYPE_CHECKING

class ComputerPlayer:
    """
    This class is placed here as a placeholder so the function can work, it 
    represents the game status of a computer player.
    
    """
    def __init__(self, difficulty, money):
        """
        Computerplayer is a class that functions as another player in the game.
        There are varying levels of difficulty avaliable, and for initialization
        , you need money amount and the difficulty (0 or 1).
        
        Args:
            difficulty, a value from 0 (easy) to 1 (hard)
            
            money, the amount in dollars the computer player has
            
        Side effects:
            changes attributes of self object
        
        """
        self.difficulty = difficulty
        self.money = money

    def get_out_of_jail(self):
        """
        This function will determine whether the Computer should pay to get out 
        of jail (0 means no, 1 means yes). First, it rolls a pair of dice three
        times, and if any of them are a double, bail is free.
        
        
        
        The difficulty the user initialized will determine whether the bail 
        behavior is intelligent or random.
        
        Returns: 0 or 1, which are yes and no responses respectively for the
        Question- should I pay to get out of jail? May also return getting out
        of jail for free.
        
        
        
        """
        turns=0
        while turns < 3:
            dice1 = random.randint(1,6)
            dice2 = random.randint(1,6)
            if dice1 == dice2:
                return ("You rolled a double, get out of jail for free")
            elif dice1 != dice2:
                continue
            turns += 1
        
        if self.difficulty == 0:
            output = random.randint(0,1)
            return output
        elif self.difficulty == 1:
            if self.money > 50:
                output = 1
                self.money -= 50
                return output
            else:
                output = 0
                return output    
                    
                
            
            
            
            
        
            