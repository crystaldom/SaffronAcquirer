import curses
from curses import wrapper
#note that you can use the curses.nodelay() to set a timed input on a typed delay thing. 

# Classes

# Global Variables
poundsOfSaffron = 0 #Represents the current amount of saffron (limited by the capacity of the farm))
saffronPerSecond = 0 #Represents the amount of saffron aquired per second
money = 0 #Represents the player's money
farmCapacity = 0 #Represents the capacity of the player's farm (limits the amount of saffron)
farmLevel = 1 #Represents the farm version that the player has

# Functions

# Functions that simplify curses commands

def main(stdscr):



wrapper(main)
