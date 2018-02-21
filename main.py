import curses
from curses import wrapper
#note that you can use the curses.nodelay() to set a timed input on a typed delay thing.
import time
import random
from threading import Thread

unlockRegionalMerchants = False
unlockFarTravelingMerchants = False
unlockInternationalMerchants = False
# Variables for time and saffron
poundsOfSaffron = 0;
total_farmers = 0;
money = 0;
total_merchants = 0;


#Farm Variables
farmCapacity = 30;
ogfarmCapacity = 30

u1check = False
u2check = False
u3check = False
u4check = False
u5check = False
u6check = False
u7check = False
u8check = False
lowerSellingRange = 1
upperSellingRange = 5

def main(stdscr): #The function that runs all of the other functions
    class merchant(object):
        def __init__(self, efficiency, price, saffronLowerSellRange, saffronUpperSellRange, sellFrequency):
            self.efficiency = efficiency; #The amount of saffron it sells per time instance
            self.price = price; #The price the player has to pay in order to purchase a merchant
            self.number = 0; #The number of merchants there are
            self.saffronLowerSellRange = saffronLowerSellRange #The lowest number that saffron can be sold for
            self.saffronUpperSellRange = saffronUpperSellRange #The highest number that saffron can be sold for
            self.sellFrequency = sellFrequency #The amount of seconds between each merchant sale
            self.startTime = time.time() #The starting time (Can't really explain this but it is necessary if I dont want to use recursion)

        def buyMerchant(self): #Function that buys a merchant if player can afford it
            global money
            global total_merchants
            if money >= self.price:
                money = money - self.price;
                self.number = self.number + 1
                total_merchants = total_merchants + 1

        def merchantRoutine(self): #Sells saffron if there is anything to sell
            global poundsOfSaffron
            global money
            global farmCapacity
            projectedSale = self.number * self.efficiency
            saffronSellPrice = random.randint(self.saffronLowerSellRange, self.saffronUpperSellRange)
            if projectedSale >= poundsOfSaffron:
                finalSale = poundsOfSaffron;
            else:
                finalSale = projectedSale
            poundsOfSaffron = poundsOfSaffron - finalSale
            money = money + (self.number * self.efficiency * saffronSellPrice)
            farmCapacity = farmCapacity + finalSale

        def checkTime(self): #Checks to see if the time has elapsed since last sale, and then proceeds to sell the stuff if this is true
            currentTime = time.time() - self.startTime
            if currentTime >= self.sellFrequency:
                self.merchantRoutine()
                self.resetStartTime()
                return True
            else:
                return False

        def resetStartTime(self): #Sets the start time to the current time
            self.startTime = time.time()

    class farmer(object): #Includes slaves, workers, skilled artisans, etc
        def __init__(self, efficiency, price, frequency):
            self.efficiency = efficiency
            self.price = price
            self.number = 0
            self.frequency = frequency
            self.startTime = time.time()

        def buyFarmer(self): #The function that is run when the user wants to buy a new farmer
            global money
            global total_farmers
            if money >= self.price:
                money = money - self.price
                self.number = self.number + 1
                total_farmers = total_farmers + 1

        def farmerRoutine(self): #The function that is run every second or so
            global poundsOfSaffron
            global farmCapacity
            expectedSaffronHarvest = self.number * self.efficiency
            if expectedSaffronHarvest >= farmCapacity:
                expectedSaffronHarvest = farmCapacity
                finalHarvest = expectedSaffronHarvest
            else:
                finalHarvest = expectedSaffronHarvest
            poundsOfSaffron = poundsOfSaffron + finalHarvest
            farmCapacity = ogfarmCapacity - poundsOfSaffron

        def checkTime(self): #Checks if a certain time has elapsed since last harvest, and then harvests if this is true
            currentTime = time.time() - self.startTime
            if currentTime >= self.frequency:
                self.farmerRoutine()
                self.resetStartTime()
                return True
            else: # The true and false are not really used, they just fill in gaps in the code.
                return False

        def resetStartTime(self): #Function that resets the start time
            self.startTime = time.time()

    def checkTimeAll():
        regularMerchant.checkTime()
        regionalMerchant.checkTime()
        farTravelingMerchant.checkTime()
        internationalMerchant.checkTime()
        slave.checkTime()
        worker.checkTime()
        skilledWorker.checkTime()

    def refresh():
        stdscr.refresh();

    def cprint(text, y, x):
        stdscr.addstr(y, x, text);

    def title(text):
        stdscr.addstr(0,0,str(text).center(80),curses.A_REVERSE)
        refresh()

    def statprint():
        stdscr.addstr(1,0,("Pounds Of Saffron "+str(poundsOfSaffron)+" | Farmers " + str(total_farmers)).center(80),curses.A_REVERSE)
        stdscr.addstr(2,0,(" Money "+ str(money) + " | Merchants " + str(total_merchants)).center(80),curses.A_REVERSE)
        stdscr.addstr(3,0, ("Farm Capacity Left: "+ str(farmCapacity) + "/" + str(ogfarmCapacity)).center(80), curses.A_REVERSE)
        refresh()

    def noecho():
        curses.noecho()

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

    #FARMER: EFFICIENCY, PRICE, FREQUENCY
    #MERCHANT: EFFICICENCY, PRICE, RANGELOWER, RANGEUPPER, FREQUENCY
    #Merchants
    regularMerchant = merchant(1, 150, 1, 3, 1)
    regionalMerchant = merchant(2, 300, 2, 5, 2)
    farTravelingMerchant = merchant(4, 700, 5, 8, 5)
    internationalMerchant = merchant(10, 1600, 20, 30, 60)
    #Farmers
    slave = farmer(1, 150, 1)
    worker = farmer(2, 300, 1)
    skilledWorker = farmer(3, 500, 1)
    # Room functions

    def menu():
        curses.curs_set(False)
        runMenu = True
        curses.noecho()
        stdscr.nodelay(1)
        title("Main Menu")
        cprint("[1] Farm Saffron By Hand", 6, 28)
        cprint("[2] Acquire Farmers", 7, 28)
        cprint("[3] Hire Merchants", 8, 28)
        cprint("[4] Upgrades", 9, 28)
        cprint("[5] Sell your saffron", 10, 28)
        stdscr.addstr(23, 0, "Choose a number: ")
        while runMenu == True:
            checkTimeAll()
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
        farmingLoop = True
        stdscr.nodelay(0)
        curses.halfdelay(5)
        global poundsOfSaffron
        global farmCapacity
        global money
        while farmingLoop == True:
            title("Farm Saffron")
            statprint()
            curses.echo()
            checkTimeAll()
            stdscr.move(23,0)
            getch = stdscr.getch()
            if getch == ord("s"):
                getchstr = "s"
                farmInput = getchstr + stdscr.getstr(10)
                if farmInput.lower() == "saffron" and (poundsOfSaffron + 1) <= ogfarmCapacity:
                    poundsOfSaffron = poundsOfSaffron + 1
                    farmCapacity = farmCapacity - 1
                    stdscr.clear()
                elif farmInput == "scheat":
                    poundsOfSaffron = poundsOfSaffron + 500
                    money = 1000000
                    stdscr.clear()
                elif farmInput.lower() == "sell":
                    manualSell()
                    stdscr.clear()
                else:
                    stdscr.clear()
            elif getch == ord("m"):
                getchstr = "m"
                farmInput = getchstr + stdscr.getstr(10)
                if farmInput.lower() == "menu":
                    farmingLoop = False
                    stdscr.clear()
                    menu()
                else:
                    stdscr.clear()
            elif getch == ord("q"):
                getchstr = "q"
                farmInput = getchstr + stdscr.getstr(10)
                if farmInput.lower() == "quit":
                    farmingLoop = False
                    stdscr.clear()
                else:
                    stdscr.clear()
            else:
                stdscr.clear()


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
        global u7check
        global unlockRegionalMerchants
        global unlockFarTravelingMerchants
        global unlockInternationalMerchants
        global upperSellingRange
        global lowerSellingRange
        global spanishUnlock
        global india
        global slaves
        global workers
        while upgradeLoop == True:
            def bruh():
                title("Upgrades")
                checkTimeAll()
                statprint()
                cprint("[1] Increase farm capacity by one acre (500)", 6, 2)
                if u1check == False:
                    cprint("[2] Sail to cilicia (1,000)", 7, 2)
                if u2check == False:
                    cprint("[3] Expansion into spain (1,500)", 8, 2)
                if u3check == False:
                    cprint("[4] Catholic Church Dyes (1,500)", 9, 2)
                if u4check == False:
                    cprint("[5] Trade with Persians (2,500)", 10, 2)
                if u5check == False:
                    cprint("[6] India expansion/yellow robe dyes (3,000)", 11, 2)
                if u6check == False:
                    cprint("[7] Research into saffron medicinal purposes (4,500)", 12, 2)
                if u7check == False:
                    cprint("[8] Bubonic plague hits, market saffron as cure (10,000)", 13, 2)
            bruh()
            U_INP = stdscr.getch()
            if U_INP == ord("1") and money >= 500:
                money = money - 500
                ogfarmCapacity = ogfarmCapacity + 1
            elif (U_INP == ord ("2") and money >= 1000) and u1check == False:
                regularMerchant.saffronLowerSellRange += 1
                regularMerchant.saffronUpperSellRange += 1
                money = money - 1000
                u1check = True
                stdscr.clear()
                bruh()
                refresh()
            elif (U_INP == ord ("3") and money >= 1500) and u2check == False:
                regionalMerchant.saffronLowerSellRange += 1
                regionalMerchant.saffronUpperSellRange += 1
                money = money - 1500
                unlockRegionalMerchants = True
                u2check = True
                stdscr.clear()
                bruh()
                refresh()
            elif (U_INP == ord ("4") and money >= 1500) and u3check == False:
                regionalMerchant.saffronLowerSellRange += 1
                regionalMerchant.saffronUpperSellRange += 1
                money = money - 1500
                u3check = True
                stdscr.clear()
                bruh()
                refresh()
            elif (U_INP == ord ("5") and money >= 2500) and u4check == False:
                farTravelingMerchant.saffronLowerSellRange -= 1
                farTravelingMerchant.saffronUpperSellRange -= 1
                money = money - 2500
                slave.number *= 2
                worker.number *= 2
                skilledWorker.number *= 2
                unlockFarTravelingMerchants = True
                u4check = True
                stdscr.clear()
                bruh()
                refresh()
            elif (U_INP == ord ("6") and money >= 3000) and u5check == False:
                internationalMerchant.saffronLowerSellRange += 2
                internationalMerchant.saffronUpperSellRange += 2
                money = money - 3000
                unlockInternationalMerchants = True
                u5check = True
                stdscr.clear()
                bruh()
                refresh()
            elif (U_INP == ord ("7") and money >= 4500) and u6check == False:
                internationalMerchant.saffronLowerSellRange += 1
                internationalMerchant.saffronUpperSellRange += 1
                money = money - 4500
                u6check = True
                stdscr.clear()
                bruh()
                refresh()
            elif (U_INP == ord("8") and money >= 10000) and u7check == False:
                internationalMerchant.saffronLowerSellRange += 4
                internationalMerchant.saffronUpperSellRange += 4
                money -= 10000
                u7check = True
                stdscr.clear()
                bruh()
                refresh()
            elif U_INP == ord ("m"):
                upgradeLoop = False
                stdscr.clear()
                menu()





    def buySlaves():
        global money
        global slaves
        global workers
        curses.halfdelay(5)
        buySlaveScreenLoop = True
        while buySlaveScreenLoop == True:
            title("Acquire Farmers")
            statprint()
            checkTimeAll()
            cprint("[1] Purchase a slave (150)", 6, 28)
            cprint("[2] Hire a worker (300)", 7, 28)
            cprint("[3] Hire a skilled worker (500)", 8, 28)
            buySlaveInput = stdscr.getch()
            if buySlaveInput == ord("1"):
                slave.buyFarmer()
            elif buySlaveInput == ord("2"):
                worker.buyFarmer()
            elif buySlaveInput == ord("3"):
                skilledWorker.buyFarmer()
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
            checkTimeAll()
            title("Hire Merchants")
            statprint()
            cprint("[1] Hire Merchants (150)", 6, 28)
            if unlockRegionalMerchants == True:
                cprint("[2] Trade With Regional Merchants (300)", 7, 28)
            if unlockFarTravelingMerchants == True:
                cprint("[3] Trade With Far Traveling Merchants (700)", 8, 28)
            if unlockInternationalMerchants == True:
                cprint("[4] Trade With International Merchants (1600)", 9, 28)
            buyMerchantsInput = stdscr.getch()
            if buyMerchantsInput == ord("1"):
                regularMerchant.buyMerchant()
            elif (buyMerchantsInput == ord("2") and unlockRegionalMerchants == True):
                regionalMerchant.buyMerchant()
            elif (buyMerchantsInput == ord("3") and unlockFarTravelingMerchants == True):
                farTravelingMerchant.buyMerchant()
            elif (buyMerchantsInput == ord("4") and unlockInternationalMerchants == True):
                internationalMerchant.buyMerchant()
            elif buyMerchantsInput == ord("m"):
                buyMerchantScreenLoop = False
                stdscr.clear()
                menu()




    menu()
wrapper(main)
