# final_project

#Files

board.csv: A CSV file that represents a physical Monopoly board. Contains information about each property (e.g., how much purchasing it, buying houses and hotels, and rent costs). Is copied into the program as a DataFrame that is mutable, allowing us to change/track who owns properties, how many houses/hotels are on a property, etc.

main_proj.py: The Python file of the Monopoly game. Contains all code necessary to run a full game of Monopoly directly from the command line.

#Running the program from the command line

Open the main_proj.py file.
Have the main_proj.py file and the board.csv in the same folder.
Run the line “python3 monopoly.py {difficulty} {playername}” in the command line.
Difficulty can assume either the value 0 or the value 1. 0 represents an easier, fully randomized ComputerPlayer opponent; 1 represents a more difficult, smarter ComputerPlayer opponent.
Playername is simply what the HumanPlayer would like to be called.
This line should be run sans the brackets above ({}).

#Using the program

Please carefully follow the instructions and prompts as they appear in the console. Some small details to note include:

Press enter to roll when prompted.
Ensuring that when responding to a prompt that asks for a ‘Y’ or ‘N’ response, the player carefully enters either ‘Y’ or ‘N’ in its exactness.

The computer player will play automatically, and its actions are separated from the human player’s actions by dashed lines.

#Attribution

Functions/Methods:
o_spaces: Ady Weng
mp_check: Ady Weng
buy_hs: Ady Weng
Game: Ady Weng

turn: Emily Klomparens
Get_out_jail: Emily Klomparens

Computerclass decision making AI, with varying difficulties, for get_out_jail (as written by Emily): Anshu Saini
Computerclass decision making for buying property (with varying computer difficulty): Anshu Saini
parse_args: Anshu Saini
Playerclass and Computerclass: option to sell property: Anshu Saini

The GameState class and the 13 methods in it: Brian McMahon
The board csv file: Brian McMahon

#Bibliography

Monopoly Wiki. (2021). Fandom. https://monopoly.fandom.com/wiki/Main_Page
This source was used to populate the board csv file and the Chance/Community Chest lists.