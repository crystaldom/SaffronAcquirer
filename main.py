import curses
from curses import wrapper
#note that you can use the curses.nodelay() to set a timed input on a typed delay thing.
import time
import random
from threading import Thread

# Classes

# Variables for time and saffron
farmingLoop = True
poundsOfSaffron = 0;
saffronPerSecond = 0;
money = 0;
moneyPerSecond = 0;

#Variables involving the multithread checker
statprintMultiThreadLoopBool = True

#Time 1 slots
currenttime1 = 0
startLoopTime1 = 0
#Time 2 slots
currenttime2 = 0
startLoopTime2 = 0
#Time 3 slots
currenttime3 = 0
startLoopTime3 = 0

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
slaves = 3;
skilledSlaves = 0;
slaveEfficiency = 2; #The number of saffron pounds that the slaves produce every second
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

    def regularSlaveFarmingAlgorithm():
        global poundsOfSaffron
        global farmCapacity
        global saffronPerSecond
        projectedSaffronGain = slaves * slaveEfficiency
        saffronPerSecond = slaves * slaveEfficiency
        projectedNetSaffon = projectedSaffronGain + poundsOfSaffron
        if projectedNetSaffon > ogfarmCapacity:
            extraSaffron = projectedNetSaffon - ogfarmCapacity
            acceptableSaffronGain = projectedNetSaffon - extraSaffron
            acceptableSaffronGain = acceptableSaffronGain - poundsOfSaffron
            poundsOfSaffron = poundsOfSaffron + acceptableSaffronGain
            farmCapacity = farmCapacity - acceptableSaffronGain
        else:
            poundsOfSaffron = projectedSaffronGain + poundsOfSaffron
            farmCapacity = farmCapacity - projectedSaffronGain

    #Time 1
    def timecheck1(x): # Will check for a X second period
        fetchCurrentTime1()
        if currenttime1 >= x:
            resetStartLooptime1()
            return True;
        else:
            return False;

    def fetchCurrentTime1():
        global currenttime1;
        currenttime1 = time.time() - startLoopTime1

    def resetStartLooptime1():
        global startLoopTime1
        startLoopTime1 = time.time()

    #Time 2
    def timecheck2(x): # Will check for a X second period
        fetchCurrentTime2()
        if currenttime2 >= x:
            resetStartLooptime2()
            return True;
        else:
            return False;

    def fetchCurrentTime2():
        global currenttime2;
        currenttime2 = time.time() - startLoopTime2

    def resetStartLooptime2():
        global startLoopTime2
        startLoopTime2 = time.time()

    #Time 3
    def timecheck3(x): # Will check for a X second period
        fetchCurrentTime3()
        if currenttime3 >= x:
            resetStartLooptime3()
            return True;
        else:
            return False;

    def fetchCurrentTime3():
        global currenttime3;
        currenttime3 = time.time() - startLoopTime3

    def resetStartLooptime3():
        global startLoopTime3
        startLoopTime3 = time.time()


    #The multithread thingy
    def statprintAlwaysUpdater():
        resetStartLooptime1()
        while statprintMultiThreadLoopBool == True:
            if timecheck1(1) == True:
                regularSlaveFarmingAlgorithm()
            statprint()

    #Menu functions and shit

    def menu():
        curses.curs_set(False)
        runMenu = True
        curses.noecho()
        stdscr.nodelay(1)
        title("Main Menu")
        cprint("[1] Farm Saffron By Hand", 6, 28)
        cprint("[2] Purchase Slaves", 7, 28)
        cprint("[3] Hire Merchants", 8, 28)
        cprint("[4] Upgrades", 9, 28)
        cprint("[5] Sell your saffron", 10, 28)
        stdscr.addstr(23, 0, "Choose a number: ")
        while runMenu == True:
            if timecheck1(1) == True:
                regularSlaveFarmingAlgorithm()
            statprint()
            stdscr.move(23, 17)
            menuInput = stdscr.getch()
            if menuInput == ord('1'):
                runMenu = False;
                stdscr.clear()
                farm()
            elif menuInput == ord('q'):
                runMenu = False;
                stdscr.clear()
            elif menuInput == ord('5'):
                manualSell()

    def manualSell():
        global money
        global poundsOfSaffron
        global farmCapacity
        amountOfSaffronSelling = poundsOfSaffron
        if amountOfSaffronSelling == ogfarmCapacity:
            sellingPrince = upperSellingRange
        else:
            sellingPrice = random.randint(lowerSellingRange, upperSellingRange)
        money = money + (amountOfSaffronSelling * sellingPrice)
        poundsOfSaffron = poundsOfSaffron - amountOfSaffronSelling
        farmCapacity = ogfarmCapacity

    def farm():
        stdscr.nodelay(0)
        curses.halfdelay(5)
        global poundsOfSaffron
        global farmingLoop
        global farmCapacity
        global money
        while farmingLoop == True:
            title("FarmLand")
            statprint()
            curses.echo()
            if timecheck1(1) == True:
                regularSlaveFarmingAlgorithm()
            stdscr.move(23,0)
            getch = stdscr.getch()
            if getch == ord("s"):
                getchstr = "s"
                farmInput = getchstr + stdscr.getstr(10)
                if farmInput.lower() == "saffron" and (poundsOfSaffron + 1) <= ogfarmCapacity:
                    poundsOfSaffron = poundsOfSaffron + 1
                    farmCapacity = farmCapacity - 1
                    stdscr.clear()
                    farm()
                elif farmInput == "cheat1":
                    poundsOfSaffron = poundsOfSaffron + 100
                    stdscr.clear()
                elif farmInput == "quit":
                    farmingLoop = False
                elif farmInput.lower() == "sell":
                    manualSell()
                    stdscr.clear()
                    farm()
                elif farmInput.lower() == "menu":
                    stdscr.clear()
                    menu()
                elif farmInput.lower() =="err":
                    print ("SUCESS")
                else:
                    stdscr.clear()
                    farm()
            elif getch == ord("m"):
                getchstr = "m"
                farmInput = getchstr + stdscr.getstr(10)
                if farmInput.lower() == "menu":
                    stdscr.clear()
                    menu()
                else:
                    stdscr.clear()
                    farm()
            elif getch == ord("q"):
                getchstr = "q"
                farmInput = getchstr + stdscr.getstr(10)
                if farmInput.lower() == "quit":
                    farmingLoop = False
                    stdscr.clear()
            else:
                stdscr.clear()
                farm()

            #DO AN ELSE STATEMENT. IF GETCH IS Q, ASK FOR QUIT, ETC, ETC.


    menu()
wrapper(main)
