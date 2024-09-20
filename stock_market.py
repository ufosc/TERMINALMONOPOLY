import random
import time
from datetime import datetime, timedelta
from os import system, name
from xml.etree.ElementTree import tostring




#hello


# hi


#first commit






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


   condition = True
   counter = 0
   last_time = time.time()


   while condition:


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


