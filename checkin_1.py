"""A module for identifying rent multipliers when an individual has a monopoly
or more than one railroad/utility.

Attributes:
    COLORS (dictionary of colors and counts): number of properties of each color
        (and railroads and utilities).
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
    "railroads": 4,
    "utilities": 2
}

class Property():
    """Temporary class for an object representing one property.
    
    Attributes:
        color (string): the color of the property; or railroad/utility.
    """
    
    def __init__(self, color):
        """Sets attributes of the Property class upon initialization.
        
        Arguments:
            color (string): the color of the property; or railroad/utility.
        Side effects:
            Modifies color attribute to specified color.
        """
        
        self.color = color

class Player():
    """An object representing one player and their characteristics.
    
    Attributes:
        prop_owned (list of Property): list comprising all properties a player
            owns.
    """
    
    def __init__(self, prop_owned):
        """Sets attributes of the Player class upon initialization.
        
        Arguments:
            prop_owned (list of Property): list comprising all properties a 
            player owns.
        Side effects:
            Modifies prop_owned attribute to specified properties.
        """
        
        self.prop_owned = prop_owned

def mp_check(player, col):
    """Function to check whether a player has a monopoly over one color of
    properties; or more than one of either railroads or utilities. Then, finds
    the appropriate rent multiplier for the opposing player.
    
    Arguments:
        player (Player): instance of Player class representing the player whose
            property was landed on.
        col (string): a string representing the color of the landed-on property.
    
    Returns:
        int: rent multiplier for the player who landed on the property.
    """
    
    properties = player.prop_owned
    col_count = {
        "brown": 0,
        "lightblue": 0,
        "pink": 0,
        "orange": 0,
        "red": 0,
        "yellow": 0,
        "green": 0,
        "darkblue": 0,
        "railroads": 0,
        "utilities": 0
    }
    
    for i in properties:
        if i.color == col:
            col_count[i.color] += 1
   
    if col != "railroads" and col != "utilities":
        if col_count[col] == COLORS[col]:
            return 2
        else:
            return 1
    elif col == "railroads":
        if col_count[col] > 1:
            return col_count[col]
        else:
            return 1
    elif col == "utilities":
        if col_count[col] == 1:
            return 4
        elif col_count[col] == 2:
            return 10
        else:
            return 1
        
if __name__ == "__main__":
    ParkLane = Property(color="darkblue")
    Boardwalk = Property(color="darkblue")
    MedAve = Property(color="brown")
    PallMall = Property(color="pink")
    PennRail = Property(color="railroads")
    BORail = Property(color="railroads")
    ElecComp = Property(color="utilities")
    WaterWorks = Property(color="utilities")
    
    Ady = Player(prop_owned=[ParkLane, Boardwalk, MedAve, PallMall, 
                             PennRail, BORail, ElecComp, WaterWorks])
    
    mp_check(Ady, "darkblue")
    mp_check(Ady, "railroads")
    mp_check(Ady, "utilities")