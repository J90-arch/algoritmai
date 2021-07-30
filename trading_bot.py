import sys
import os
import dotenv
import selenium
from dotenv import load_dotenv
import dotenv
from Trading212 import Invest
from Trading212 import CFD
import yahoo_fin.stock_info as si
import datetime
import schedule
import time


#from open_hours import *
from predictions_for_trading import AI_prediction


load_dotenv()

#stock = "SPDR Portfolio S&P 500 Value" #"SPDR S&P 500" # PARAMETER   PUT THE NAME AS IT APPEARS ON TRADING212!!! E.G Apple instead of AAPL
#stock_short_name = "SPYV"# "SPY" #PARAMETER 4 letter name of the stock
stock = os.getenv("STOCK")
stock_short_name = os.getenv("STOCK_SHORT_NAME")
parameter_max_transaction_sum = int(os.getenv("PARAMETER_MAX_TRANSACTION_SUM")) # PARAMETER    what % of the portfolio total value can be used in 1 transaction
buy_sell_frequency = int(os.getenv("BUY_SELL_FREQUENCY")) # PARAMETER    in seconds how frequently does the algorithm make a decisions to buy or sell
allocated_cash = int(os.getenv("ALLOCATED_CASH")) # PARAMETER   allocate the cash the algorithm can use
free_cash = allocated_cash # how much remaining cash the algo has to buy stocks with
open_position_num = int(float(os.getenv("OPEN_POSITION_NUM"))) # how many shares have we got (change before starting if > 0)
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

### Enabled if using relative price change
#predicted_price_main = si.get_live_price(stock_short_name)
#was price rising
portfolio_state = False
invest = True

print("\033[93m {}\033[00m" .format("\n\n\tLogging in...\n"))

def login(invest = True):
    if invest:
        trading = Invest(email, password, headless=False)# For practice account
    else:
        trading = CFD(email, password, headless=False) # For practice
    return trading



try:
    trading = login(invest)
    print("\033[92m {}\033[00m" .format("\tSuccesufuly logged in\n"))
except selenium.common.exceptions.InvalidSessionIdException:
    print("\033[91m {}\033[00m" .format("\tTime out, did not log in"))
    sys.exit()


# from open_hours import is_open # uncomment after testing

def is_open(): # remove this after testing #  doesn't work, left it in
    return True


def buy(stock, amount):
    global trading
    print (f"buying {amount} stocks (only simulated)")
    with open("log.txt", "a") as f:
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' Bought {amount} of {stock}\n')
    try:    
        trading.buy_stock(stock, amount)
    except:
        print("Exception, relogging in")
        trading.close()
        trading = login(invest)
        trading.buy_stock(stock, amount)


def close(stock, amount):
    global trading
    print (f"closing position (only simulated)")
    with open("log.txt", "a") as f:
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' Closed position {amount} of {stock}\n')
    try:
        trading.close_position(stock)
    except:
        print("Exception, relogging in")
        trading.close()
        trading = login(invest)
        trading.close_position(stock)


if not invest:
    def shortsell(stock, amount):
        global trading
        print (f"borrowing {amount} stocks (only simulated)")
        with open("log.txt", "a") as f:
            f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' Borrowed {amount} of {stock}\n')
        try:    
            trading.sell_stock(stock, amount)
        except:
            print("Exception, relogging in")
            trading.close()
            trading = login(invest)
            trading.sell_stock(stock, amount)

def has_stock(stock):
    global open_position_num

    if open_position_num > 0:
        return True
    else:
        return False


def get_stock_price(stock_short_name): # function to get Stock price
    stock_price = si.get_live_price(stock_short_name)
    return stock_price


parameter_max_transaction_sum /= 100 # converts initial mts % to numbers


def get_max_transaction_sum(stock_price):
    global parameter_max_transaction_sum
    global portfolio_value # just for testing

    portfolio_value = free_cash + open_position_num * stock_price
    max_transaction_sum = parameter_max_transaction_sum * portfolio_value
    return max_transaction_sum


def algo_decision(): # decides whether to buy or to sell the shares it has and how many
    global portfolio_value # just for testing
    global stock
    global stock_short_name
    global free_cash
    global open_position_num
    global portfolio_state

    if is_open(): # checks whether or not regular market is open
        algo_ans = AI_prediction() # algorithm output
        algo_ans = algo_ans[0]
        stock_price = get_stock_price(stock_short_name)
        max_transaction_sum = get_max_transaction_sum(stock_price)

        print(f'algo {algo_ans}, portfolio {portfolio_state}')
        # algo = should price go up in the future?
        # portfolio_state = did price go up in the past?
        # shortselling = is bot currently shortselling?
        if algo_ans and not portfolio_state:  
            portfolio_state = True
            #if shortselling:
            #    close(stock, amount)
            amount = free_cash // stock_price
            if amount * stock_price > max_transaction_sum:
                amount = max_transaction_sum // stock_price
                if free_cash < amount * stock_price:
                    amount = free_cash // stock_price
            free_cash -= amount * stock_price
            buy(stock, amount)
            dotenv.set_key('.env', "OPEN_POSITION_NUM", str(open_position_num+amount))
            open_position_num += amount
            
            #timestamp = datetime.datetime.now()
            #bought.append([amount, stock_price, timestamp])

            # # can't make mistakes when buying
            # transaction_type = "bought"
            # if is_mistake(transaction_type, stock_price):
            #     mistake = mistakes(transaction_type, amount, stock_price, timestamp)
            #         f = open("mistakes.txt", "a")
            #         f.write(mistake)
            #         f.close()
            

        elif portfolio_state and not algo_ans: # if algo outputs False (price should go down)
            portfolio_state = False
            if has_stock(stock):
                amount = open_position_num
                if amount * stock_price > max_transaction_sum:
                    amount = max_transaction_sum // stock_price
                free_cash += amount * stock_price
                close(stock, amount)
                dotenv.set_key('.env', "OPEN_POSITION_NUM", "0")
                open_position_num = 0

                #timestamp = datetime.datetime.now()
                #sold.append([amount, stock_price, timestamp])

                #transaction_type = "sold"
                '''
                if is_mistake(transaction_type, stock_price):
                    mistake = mistakes(transaction_type, amount, stock_price, timestamp)
                    f = open("mistakes.txt", "a")
                    f.write(mistake)
                    f.close()
                '''

            elif not has_stock(stock): # if we have nothing to sell
                print("nothing to sell")
                with open("log.txt", "a") as f:
                    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' nothing to sell\n') # maybe remove the print() and do nothing

        elif algo_ans == '0': # fringe case if price doesnt change
            print("no change in price")
            #with open("log.txt", "a") as f:
            #    f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f' no change in price\n')


schedule.every(buy_sell_frequency).seconds.do(algo_decision)

while 1:
    schedule.run_pending()
    time.sleep(1)
