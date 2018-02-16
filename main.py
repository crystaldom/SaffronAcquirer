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
ftmprice = 400
ftmEfficiency = 100
reallyFarTravelingMerchants = 0;
rftmprice = 1000
rftmEfficiency = 500
salesPerSecond = 0;
merchantEfficiency = 1;
merchantPrice = 100

#Slave Vars BTW this is a work in progress
slaves = 0;
slavePrice = 100
skilledSlaves = 0;
slaveEfficiency = 2; #The number of saffron pounds that the slaves produce every second
# Functions that simplify curses commands
workers = 0
workerPrice = 130
workerEfficiency = 3

#Unlocks
spanishUnlock = False
plague = False
india = False
persianFarms = False
christianityDyes = False

MerchantMoneyThatWillBeMade = 0;
ftMerchantmoneyThatWillBeMade = 0;
rftMerchantMoneyThatWillBeMade = 0;

u1check = False
u2check = False
u3check = False
u4check = False
u5check = False
u6check = False



def main(stdscr):
    def refresh():
        stdscr.refresh();

    def cprint(text, y, x):
        stdscr.addstr(y, x, text);

    def title(text):
        stdscr.addstr(0,0,str(text).center(80),curses.A_REVERSE)
        refresh()

    def statprint():
        stdscr.addstr(1,0,("Pounds Of Saffron "+str(poundsOfSaffron)+" | Saffron Per Second " + str(saffronPerSecond)).center(80),curses.A_REVERSE)
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
        saffronPerSecond = slaves * slaveEfficiency + (workers * workerEfficiency)
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

    def workerFarmingAlgorithm():
        global poundsOfSaffron
        global farmCapacity
        global saffronPerSecond
        projectedSaffronGain = workers * workerEfficiency
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

    def regularMerchantSellingAlgorithm():
        global MerchantMoneyThatWillBeMade
        global poundsOfSaffron
        global salesPerSecond
        global moneyPerSecond
        global money
        global farmCapacity
        saffronToSell = merchants * merchantEfficiency
        if poundsOfSaffron < saffronToSell:
            saffronToSell = poundsOfSaffron
        MerchantMoneyThatWillBeMade = random.randint(lowerSellingRange, upperSellingRange) * saffronToSell
        poundsOfSaffron = poundsOfSaffron - saffronToSell
        farmCapacity = farmCapacity + saffronToSell
        money = money + MerchantMoneyThatWillBeMade
        moneyPerSecond = MerchantMoneyThatWillBeMade + (ftMerchantmoneyThatWillBeMade / 10) + (rftMerchantMoneyThatWillBeMade / 100)

    def ftMerchantSellingAlgorithm():
        global ftMerchantmoneyThatWillBeMade
        global poundsOfSaffron
        global moneyPerSecond
        global money
        global farmCapacity
        global poundsOfSaffron
        global salesPerSecond
        global moneyPerSecond
        global money
        global farmCapacity
        saffronToSell = farTravelingMerchants * ftmEfficiency
        if poundsOfSaffron < saffronToSell:
            saffronToSell = poundsOfSaffron
        ftMerchantmoneyThatWillBeMade = random.randint(lowerSellingRange + 2, upperSellingRange + 2) * saffronToSell
        poundsOfSaffron = poundsOfSaffron - saffronToSell
        farmCapacity = farmCapacity + saffronToSell
        money = money + ftMerchantmoneyThatWillBeMade
        moneyPerSecond = (ftMerchantmoneyThatWillBeMade / 10) + MerchantMoneyThatWillBeMade + (rftMerchantMoneyThatWillBeMade / 100)

    def rftMerchantSellingAlgorithm():
        global rftMerchantMoneyThatWillBeMade
        global poundsOfSaffron
        global moneyPerSecond
        global money
        global farmCapacity
        global poundsOfSaffron
        global salesPerSecond
        global moneyPerSecond
        global money
        global farmCapacity
        saffronToSell = farTravelingMerchants * ftmEfficiency
        if poundsOfSaffron < saffronToSell:
            saffronToSell = poundsOfSaffron
        rftMerchantMoneyThatWillBeMade = random.randint(lowerSellingRange + 7, upperSellingRange + 7) * saffronToSell
        poundsOfSaffron = poundsOfSaffron - saffronToSell
        farmCapacity = farmCapacity + saffronToSell
        money = money + rftMerchantMoneyThatWillBeMade
        moneyPerSecond = (ftMerchantmoneyThatWillBeMade / 10) + MerchantMoneyThatWillBeMade + (rftMerchantMoneyThatWillBeMade / 100)



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

    def manualSell():
        global money
        global poundsOfSaffron
        global farmCapacity
        amountOfSaffronSelling = poundsOfSaffron
        if amountOfSaffronSelling == ogfarmCapacity:
            sellingPrice = upperSellingRange
        else:
            sellingPrice = random.randint(lowerSellingRange, upperSellingRange)
        money = money + (amountOfSaffronSelling * sellingPrice)
        poundsOfSaffron = poundsOfSaffron - amountOfSaffronSelling
        farmCapacity = ogfarmCapacity

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
                regularMerchantSellingAlgorithm()
                workerFarmingAlgorithm()
            if timecheck2(10) == True:
                ftMerchantSellingAlgorithm()
            if timecheck3(100) == True:
                rftMerchantSellingAlgorithm()
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
            elif menuInput == ord('2'):
                runMenu = False
                stdscr.clear()
                buySlaves()
            elif menuInput == ord('3'):
                runMenu = False
                stdscr.clear()
                buyMerchants()
            elif menuInput == ord('4'):
                runMenu = False
                stdscr.clear()
                purchaseUpgrades()




    def farm():
        stdscr.nodelay(0)
        curses.halfdelay(5)
        global poundsOfSaffron
        global farmingLoop
        global farmCapacity
        global money
        farmingLoop = True
        while farmingLoop == True:
            title("Farm Saffron")
            statprint()
            curses.echo()
            if timecheck1(1) == True:
                regularSlaveFarmingAlgorithm()
                regularMerchantSellingAlgorithm()
                workerFarmingAlgorithm()
            if timecheck2(10) == True:
                ftMerchantSellingAlgorithm()
            if timecheck3(100) == True:
                rftMerchantSellingAlgorithm()
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
                    farmingLoop == False
                    stdscr.clear()
                    menu()
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

    def purchaseUpgrades():
        upgradeLoop = True
        global money
        global merchantEfficiency
        global slaveEfficiency
        global workerEfficiency
        global ogfarmCapacity
        global u1check
        global u2check
        global u3check
        global u4check
        global u5check
        global u6check
        global upperSellingRange
        global lowerSellingRange
        global spanishUnlock
        global india
        global slaves
        global workers
        while upgradeLoop == True:
            if timecheck1(1) == True:
                regularSlaveFarmingAlgorithm()
                regularMerchantSellingAlgorithm()
                workerFarmingAlgorithm()
            if timecheck2(10) == True:
                ftMerchantSellingAlgorithm()
            if timecheck3(100) == True:
                rftMerchantSellingAlgorithm()
            title("Upgrades")
            statprint()
            cprint("[1] Increase farm capacity by one acre (200)", 6, 2)
            if u1check == False:
                cprint("[2] Sail to cilicia (600) + 1 value of saffron", 7, 2)
            if u2check == False:
                cprint("[3] Expansion into spain (1,000) +2 value of saffron MU", 8, 2)
            if u3check == False:
                cprint("[4] Catholic Church (1,500) + 1 value of saffron", 9, 2)
            if u4check == False:
                cprint("[5] Trade with persians (2,000) x2 workers and slaves, -1 saffron value", 10, 2)
            if u5check == False:
                cprint("[6] Persians restock indian gardens with saffron (3,000) + 3 saffron value MU", 11, 2)
            if u6check == False:
                cprint("[7] Research into saffron medicinal purposes (6,000) + 8 saffron value", 12, 2)
            U_INP = stdscr.getch()
            if U_INP == ord("1") and money >= 200:
                money = money - 200
                ogfarmCapacity = ogfarmCapacity + 1
            elif (U_INP == ord ("2") and money >= 600) and u1check == False:
                lowerSellingRange = lowerSellingRange + 1
                upperSellingRange = upperSellingRange + 1
                money = money - 600
                u1check = True
            elif (U_INP == ord ("3") and money >= 1000) and u2check == False:
                lowerSellingRange = lowerSellingRange + 2
                upperSellingRange = upperSellingRange + 2
                money = money - 1000
                spanishUnlock = True
                u2check = True
            elif (U_INP == ord ("4") and money >= 1500) and u3check == False:
                lowerSellingRange = lowerSellingRange + 1
                upperSellingRange = upperSellingRange + 1
                money = money - 1500
                u3check = True
            elif (U_INP == ord ("5") and money >= 2000) and u4check == False:
                lowerSellingRange = lowerSellingRange - 1
                upperSellingRange = upperSellingRange - 1
                money = money - 2000
                slaves = slaves * 2
                workers = workers * 2
                u4check = True
            elif (U_INP == ord ("6") and money >= 3000) and u5check == False:
                lowerSellingRange = lowerSellingRange + 1
                upperSellingRange = upperSellingRange + 1
                money = money - 3000
                india = True
                u5check = True
            elif (U_INP == ord ("7") and money >= 6000) and u6check == False:
                lowerSellingRange = lowerSellingRange + 8
                upperSellingRange = upperSellingRange + 8
                money = money - 3000
                u6check = True
            elif U_INP == ord ("m"):
                upgradeLoop = False
                stdscr.clear()
                menu()




    def buySlaves():
        global money
        global slaves
        global workers
        curses.halfdelay(10)
        buySlaveScreenLoop = True
        while buySlaveScreenLoop == True:
            title("slaves")
            statprint()
            if timecheck1(1) == True:
                regularSlaveFarmingAlgorithm()
                regularMerchantSellingAlgorithm()
                workerFarmingAlgorithm()
            if timecheck2(10) == True:
                ftMerchantSellingAlgorithm()
            if timecheck3(100) == True:
                rftMerchantSellingAlgorithm()
            cprint("[1] Purchase a slave (30)", 6, 28)
            cprint("[2] Hire a worker (120)", 7, 28)
            buySlaveInput = stdscr.getch()
            if buySlaveInput == ord("1"):
                if ( money - slavePrice ) > 0 :
                    money = money - slavePrice
                    slaves = slaves + 1
            elif buySlaveInput == ord("2"):
                if ( money - workerPrice ) > 0 :
                    money = money - workerPrice
                    workers = workers + 1
            elif buySlaveInput == ord("m"):
                buySlaveScreenLoop = False
                stdscr.clear()
                menu()

    def buyMerchants():
        buyMerchantScreenLoop = True
        global money
        global merchants
        global farTravelingMerchants
        global reallyFarTravelingMerchants
        while buyMerchantScreenLoop == True:
            if timecheck1(1) == True:
                regularSlaveFarmingAlgorithm()
                regularMerchantSellingAlgorithm()
                workerFarmingAlgorithm()
            if timecheck2(10) == True:
                ftMerchantSellingAlgorithm()
            if timecheck3(100) == True:
                rftMerchantSellingAlgorithm()
            title("Merchants")
            statprint()
            cprint("[1] Buy Merchants (100)", 6, 28)
            if spanishUnlock == True:
                cprint("[2] Buy Far Traveling Merchants", 7, 28)
            if india == True:
                cprint("[3] Buy REALLY Far Traveling Merchants", 8, 28)
            buyMerchantsInput = stdscr.getch()
            if buyMerchantsInput == ord("1") and money >= merchantPrice:
                merchants = merchants + 1
                money = money - merchantPrice
            elif (buyMerchantsInput == ord("2") and spanishUnlock == True) and money >= ftmprice:
                farTravelingMerchants = farTravelingMerchants + 1
                money = money - rftmprice
            elif (buyMerchantsInput == ord("3") and india == True) and money >= rftmprice:
                reallyFarTravelingMerchants = reallyFarTravelingMerchants + 1
                money = money - rftmprice
            elif buyMerchantsInput == ord("m"):
                buyMerchantScreenLoop = False
                stdscr.clear()
                menu()




    menu()
wrapper(main)
