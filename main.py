import curses
from curses import wrapper
#note that you can use the curses.nodelay() to set a timed input on a typed delay thing.
import time
import random

# Classes

# Global Variables
farmingLoop = True
poundsOfSaffron = 0;
saffronPerSecond = 0;
money = 0;
moneyPerSecond = 0;

#Farm Variables
farmCapacity = 30;
ogfarmCapacity = 30
farmLevel = 1
numberOfAcres = None;

#Selling Variables
lowerSellingRange = 2
upperSellingRange = 5
#Merhant Vars
merchants = 0;
regionalMerchants = 0;
farTravelingMerchants = 0;
reallyFarTravelingMerchants = 0;
salesPerSecond = 0;

#Slave Vars BTW this is a work in progress
slaves = 0;
skilledSlaves = 0;
# Functions that simplify curses commands


def main(stdscr):
    def refresh():
        stdscr.refresh();

    def cprint(text, y, x):
        stdscr.addstr(y, x, text);

    def title(text):
        stdscr.addstr(0,0,str(text).center(80),curses.A_REVERSE)
        refresh()

    def statprint():
        stdscr.addstr(1,0,("Pounds Of Saffron "+str(poundsOfSaffron)+" | Saffron Per Second " + str(salesPerSecond)).center(80),curses.A_REVERSE)
        stdscr.addstr(2,0,(" Money "+ str(money) + " | Money/Sales Per Second " + str(moneyPerSecond)).center(80),curses.A_REVERSE)
        stdscr.addstr(3,0, ("Farm Capacity Left: "+ str(farmCapacity)).center(80), curses.A_REVERSE)
        refresh()

    def noecho():
        curses.noecho()

    def automaticSaffonFarmingAlgorith:
        projectedSaffronGain = 
    def farm():
        global poundsOfSaffron
        global farmingLoop
        global farmCapacity
        global money
        while farmingLoop == True:
            title("Saffron Aquirer")
            statprint()
            noecho()
            curses.echo()
            stdscr.move(23,0)
            farmInput = stdscr.getstr(10)
            if farmInput.lower() == "saffron" and (poundsOfSaffron + 1) <= ogfarmCapacity:
                poundsOfSaffron = poundsOfSaffron + 1
                farmCapacity = farmCapacity - 1
                stdscr.clear()
            elif farmInput == "cheat1":
                poundsOfSaffron = poundsOfSaffron + 100
                stdscr.clear()
            elif farmInput == "quit":
                farmingLoop = False
            elif farmInput.lower() == "sell":
                amountOfSaffronSelling = poundsOfSaffron
                sellingPrice = random.randint(lowerSellingRange, upperSellingRange)
                money = money + (amountOfSaffronSelling * sellingPrice)
                poundsOfSaffron = poundsOfSaffron - amountOfSaffronSelling
                stdscr.clear()
            else:
                stdscr.clear()


    farm()

wrapper(main)
