import random

class Computer:
    
    def __init__(self, name, difficulty):
        """Initializes a computer player object.

        Args:
        name (str): name of the computer player.
        """ 
        self.name = name
        self.money = 1500
        self.jail = False
        self.props_owned = 0
        self.turn_counter = 0
        self.difficulty = difficulty

    def rent(self, computer1, price):
        """The computer's descison to rent a property based on difficulty.

        Args:
        computer1 (obj): a computer player object
        price (int) : price of rent for the property

        Returns:
        bool: True or False if the Computer will purchase the property landed
        on.
        """ 
        if (computer1.diffuclity == 0):
            # Random choice 
            num = random.randint(1)
            if (num == 0):
                return False
            else:
                return True
        # Computer diffculty is 1 = high
        else:
            # Evaluate based on money the computer has 
            if (computer1.money > price*2):
                return True
            else:
                return False