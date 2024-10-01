import random
import time
import sys
from datetime import datetime, timedelta
from os import system, name
from xml.etree.ElementTree import tostring




#hello


# hi


#first commit


#portfolio class will be owned by players
class portfolio:
    def __init__(self, player_name, stock_market):
        self.player_name = player_name
        self.stock_market = stock_market
        self.owned_stocks = {}


    def buy_stock(self, stock_ticker, num_shares):
        if stock_ticker in self.stock_market.stocks:
            self.owned_stocks[stock_ticker] += num_shares
            print(f"{self.player_name} bought {num_shares} shares of {stock_ticker}.")
        else:
            print(f"Stock {stock_ticker} not found!")


    def sell_stock(self, stock_ticker, num_shares):
        if stock_ticker in self.owned_stocks and self.owned_stocks[stock_ticker] >= num_shares:
            self.owned_stocks[stock_ticker] -= num_shares
            print(f"{self.player_name} sold {num_shares} shares of {stock_ticker}.")
        else:
            print(f"{self.player_name} doesn't have enough shares of {stock_ticker} to sell.")

    def display_portfolio(self):
        print(f"{self.player_name}'s Portfolio:")
        for stock_ticker, num_shares in self.owned_stocks.items():
            stock_price = self.stock_market.get_stock_price(stock_ticker)  # Fetch the latest price
            print(f"{stock_ticker}: {num_shares} shares, Current Price: ${stock_price:.2f}")




#stock class will contain attributes for an individual stock including
#individual methods for updating the stock price that can be adjusted if
#the stock is a large/mid/small-cap stock
class stock:
   def __init__(self, ticker, initial_price, min_percent_change, max_percent_change):
       self.ticker = ticker
       self.price = initial_price
       self.percentage_change = 0
       self.num_shares_owned = 0
       self.min_percent_change = min_percent_change
       self.max_percent_change = max_percent_change
       self.is_owned = False


   def update_price(self):
       self.price = self.fluctuate_stock_price(self.price)


   def fluctuate_stock_price(self, current_stock_price):
       rand_num = random.uniform(self.min_percent_change, self.max_percent_change)
       self.percentage_change = rand_num
       new_price = current_stock_price + current_stock_price * (rand_num / 100)
       return new_price


   def get_price(self):
       return self.price


   def shares_owned(self):
       return self.num_shares_owned


   def display_price(self):
           print(f"{self.ticker}: ${self.price:.2f}")








#stock market class that will centralize the broader stock market
#and allow for broader changes across stocks when certain in-game
#actions occur (ex: boardwalk is bought to every stock is subject to
#a certain type of change) and this class will hold individual stock objects
#in a dictionary
class stock_market:
   def __init__(self):
       self.stocks = {}
       self.players = []
       self.current_time = datetime(2024, 9, 16, 9, 0, 0)




   def add_stock(self, stock_ticker, stock_price, min_percent_change, max_percent_change):
       #stock is an instance of the stock class
       self.stocks[stock_ticker] = stock(stock_ticker, stock_price, min_percent_change, max_percent_change)


   def update_stock_prices(self):
       for each_stock in self.stocks.values():
           #method in the stock class so each stock
           #can individually update its price allowing
           #for unique movements for each stock (ex:
           #large-cap will have less volatility vs small-cap)
           each_stock.update_price()


   def get_stock_price(self, ticker):
       return self.stocks[ticker].get_price()


   def display_stock_prices(self):
       for each_stock in self.stocks.values():
           each_stock.display_price()




   def update_time(self, seconds_passed):
       # Increment time by minutes. 5 real-world seconds = 1 hour (60 minutes in-game)
       minutes_to_add = (60 / 5) * seconds_passed  # Calculate how many minutes to add for each second passed
       self.current_time += timedelta(minutes=minutes_to_add)


   def display_time(self):
       # Display current time in "Day HH:MM AM/PM" format
       print("Current market time:", self.current_time.strftime("%A %I:%M %p"))







if __name__ == '__main__':

   market = stock_market()

   market.add_stock("PLZA", 20.00, -5, 5)
   market.add_stock("BLVD", 5.00, -10, 10)
   market.add_stock("DRVE", 0.01, -15, 15)
    #put an escape code in front of this \033
   user_input = input("Please select one of the following: 1: BUY 2: SELL \n")

   if (user_input == "BUY"):
       # print("buy executed")
       ticker_name = input("Please enter name of ticker you want to buy: \n")
       for each_stock in market.stocks:
           if (each_stock == ticker_name):
               amount = input("Enter number of stocks: \n")
               choice = input("LIMIT or BUY NOW \n")
               if (choice == "LIMIT"):
                   limit = input("Enter amount:\n")
                   break
               if (choice == "BUY NOW"):
                   print("You have bought " + ticker_name + "!\n")
                   break
       print("Invalid ticker!")



   if (user_input == "SELL"):
       # print("sell executed")
       ticker_name = input("Please enter name of ticker you want to sell: \n")
       for each_stock in market.stocks:
           if (each_stock == ticker_name):
               amount = input("Enter number of stocks: \n")
               choice = input("STOPLOSS or SELL NOW \n")
               if (choice == "STOPLOSS"):
                   stop_loss = input("Enter amount: \n")
                   break
               if (choice == "SELL NOW"):
                   print("You have sold " + ticker_name + "! \n")
                   break
       print("Invalid ticker!")

   # print (sys.argv)

   condition = True
   counter = 0
   last_time = time.time()


   while not condition:


       current_time = time.time()
       seconds_passed = current_time - last_time
       last_time = current_time


       market.display_time()
       market.display_stock_prices()


       market.update_time(seconds_passed)
       market.update_stock_prices()



       time.sleep(1)






       #just temporary so the loop doesn't go forever
       if(counter == 10):
           condition = False
       counter += 1


       print(f"\a")



