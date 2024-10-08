import random
import time
import sys
from datetime import datetime, timedelta
import os
from xml.etree.ElementTree import tostring
import threading

from setuptools.package_index import PyPIConfig


#hello


# hi

#portfolio class will be owned by players
class portfolio:
    def __init__(self, player_name, stock_market):
        self.player_name = player_name
        self.stock_market = stock_market
        self.owned_stocks = {"BLVD": 0, "PLZA": 0, "DRVE": 0}

    def buy_stock(self, stock_ticker, num_shares):
        if stock_ticker in self.stock_market.stocks:
            self.owned_stocks[stock_ticker] += num_shares

    def sell_stock(self, stock_ticker, num_shares):
        if stock_ticker in self.owned_stocks and self.owned_stocks[stock_ticker] >= num_shares:
            self.owned_stocks[stock_ticker] -= num_shares

    def display_portfolio(self):
        portfolio_lines = [f"{self.player_name}'s Portfolio:"]
        has_stocks = False
        for stock_ticker, num_shares in self.owned_stocks.items():
            if num_shares > 0:
                stock_price = self.stock_market.get_stock_price(stock_ticker)  # Fetch the latest price
                portfolio_lines.append(f"{stock_ticker}: {num_shares} shares, Price: ${stock_price:.5f}")
                has_stocks = True
        if not has_stocks:
            portfolio_lines.append("No stocks owned.")
        return portfolio_lines

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
           print(f"{self.ticker}: ${self.price:.5f}")

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
       stock_lines = []
       for ticker, stock_obj in self.stocks.items():
           price_change = stock_obj.percentage_change
           price_color = "\033[32m" if price_change >= 0 else "\033[31m"
           stock_lines.append(f"{ticker}: {price_color}${stock_obj.get_price():.5f} ({price_change:+.5f}%)\033[0m")
       return stock_lines

   def update_time(self, seconds_passed):
       # Increment time by minutes. 5 real-world seconds = 1 hour (60 minutes in-game)
       minutes_to_add = (60 / 5) * seconds_passed  # Calculate how many minutes to add for each second passed
       self.current_time += timedelta(minutes=minutes_to_add)

   def display_time(self):
       # Display current time in "Day HH:MM AM/PM" format
       return f"Current market time: {self.current_time.strftime('%A %I:%M %p')}"



#general functions outside of classes

# Function to clear the console
def clear_console():
    if os.name == 'nt':
        _ = os.system('cls')  # For Windows
    else:
        _ = os.system('clear')  # For macOS/Linux




def display_stock_prices(market):
    while True:
        # Stock prices on the left
        stock_lines = market.display_stock_prices()
        current_time = market.display_time()

        # Portfolio and user input on the right
        portfolio_lines = player1_portfolio.display_portfolio()

        # Move the cursor to row 0, column 0 and print the current time
        print(f"\033[0;0H\033[32m{current_time}\033[0m")

        # Determine maximum number of rows to print
        max_lines = max(len(stock_lines), len(portfolio_lines))

        # Start printing from row 1 (row 0 is used for time)
        for i in range(max_lines):
            # Print stock prices on the left starting at row (i+1), column 0
            if i < len(stock_lines):
                left_side = stock_lines[i]
                # Move cursor to row i+1, column 0 and print stock price
                print(f"\033[{i+2};0H{left_side}")
            else:
                # Clear line if there's no stock data for this row
                print(f"\033[{i+2};0H{' ' * 40}")

            # Print portfolio on the right starting at row (i+1), column 40
            if i < len(portfolio_lines):
                right_side = portfolio_lines[i]
                # Move cursor to row i+1, column 40 and print portfolio data
                print(f"\033[{i+2};40H{right_side}")
            else:
                # Clear line if there's no portfolio data for this row
                print(f"\033[{i+2};40H{' ' * 40}")

        # Update stock prices
        market.update_stock_prices()


        # Sleep to control the update rate
        time.sleep(20)


# Function to handle user input for buying or selling stocks in a separate thread
def handle_user_input(player_portfolio):
    while True:
        stock_lines = market.display_stock_prices()
        line_to_print = len(stock_lines) + 3
        #clear_console()
        #\033[ < line >; < col > H
        #\033[0;0H" to print row 0 column 0
        print(f"\033[{line_to_print};0H" + ' ' * 80)
        print(f"\033[{line_to_print};0H" + "Please select one of the following: BUY or SELL")
        print(f"\033[{line_to_print + 1};0H" + ' ' * 80)
        user_input = input(f"\033[{line_to_print + 1};0H" + "> ")
        if user_input.upper() == "BUY":
            print(f"\033[{line_to_print};0H" + ' ' * 80)
            print(f"\033[{line_to_print};0H" + "Enter ticker to buy")
            print(f"\033[{line_to_print + 1};0H" + ' ' * 80)
            ticker_name = input(f"\033[{line_to_print + 1};0H" + "> ")
            if ticker_name in player_portfolio.stock_market.stocks:
                print(f"\033[{line_to_print};0H" + ' ' * 80)
                print(f"\033[{line_to_print};0H" + "Enter number of shares")
                print(f"\033[{line_to_print + 1};0H" + ' ' * 80)
                amount = input(f"\033[{line_to_print + 1};0H" + "> ")
                if amount.isdigit():
                    player_portfolio.buy_stock(ticker_name, int(amount))
                    #print(f"\033[{line_to_print + 4};0H" + f"You have bought {amount} shares of {ticker_name}!")
                else:
                    print(f"\033[{line_to_print};0H" + ' ' * 80)
                    user_redo = input(f"\033[{line_to_print};0H" + "Input was not a number!" + "\nPress any key to continue")
            else:
                print(f"\033[{line_to_print};0H" + ' ' * 80)
                user_invalid_ticker = input(f"\033[{line_to_print};0H" + "Invalid ticker!" + "\nPress any key to continue")
        elif user_input.upper() == "SELL":
            print(f"\033[{line_to_print};0H" + ' ' * 80)
            print(f"\033[{line_to_print};0HEnter ticker to sell")
            print(f"\033[{line_to_print + 1};0H" + ' ' * 80)
            ticker_name = input(f"\033[{line_to_print + 1};0H" + "> ")
            if ticker_name in player_portfolio.stock_market.stocks:
                print(f"\033[{line_to_print};0H" + ' ' * 80)
                print(f"\033[{line_to_print};0H" + "Enter number of shares")
                print(f"\033[{line_to_print + 1};0H" + ' ' * 80)
                amount = input(f"\033[{line_to_print + 1};0H" + "> ")
                if amount.isdigit():
                    player_portfolio.sell_stock(ticker_name, int(amount))
                else:
                    print(f"\033[{line_to_print};0H" + ' ' * 80)
                    input(f"\033[{line_to_print};0H" + "Input was not a number!" + "\nPress any key to continue")
            else:
                print(f"\033[{line_to_print};0H" + ' ' * 80)
                input(f"\033[{line_to_print};0HInvalid ticker!" + "\nPress any key to continue")
        print("\033[2B")  # Move cursor down two rows


        #
        # elif user_input.upper() == "SELL":
        #     ticker_name = input("Enter ticker to sell: \n")
        #     if ticker_name in player_portfolio.stock_market.stocks:
        #         amount = int(input("Enter number of shares: \n"))
        #         player_portfolio.sell_stock(ticker_name, amount)
        #         print(f"You have sold {amount} shares of {ticker_name}!\n")
        #     else:
        #         print("Invalid ticker!")



def build_graph():
    width, height = 50, 7  # adjusted for terminal size
    data = [random.randint(0, 100) for _ in range(50)]
    # creates array data with random values
    while True:  # infinite loop that:
        clear_console()  # clears
        draw_graph(data, width, height)  # draws graph
        data.append(random.randint(0, 100))  # adds value
        data.pop(0)  # deletes oldest value
        time.sleep(0.5)  # pauses for 0.5 seconds



def draw_graph(data, width, height):
    max_value = max(data)
    min_value = min(data)

    print("\n" * 10)

    # draw the top axis
    print("     +" + "-" * width + "+")  # width is the total number of columns available for graph

    # iterates from height to 0 to print each line of the graph
    for y in range(height, -1, -1):
        label = f"{y:.1f}"
        line = f"{label:>4} |"  # formats y-axis labels with width of 2 char
        for x in range(width): # iterates over each column of the graph from 0 to width - 1
            value_index = int(x * len(data) / width)
            # scales column index to range of data list and converts to int
            value = data[value_index]  # index in data list that corresponds to current column x
            graph_y = height - int((value - min_value) / (max_value - min_value) * height)
            # converts the data value to a y-coordinate in the graph
            # normalizes the data to range between 0 and 1 and then normalizes it to the graph height
            # inverts y-coord because the terminal's origin is at the top-left
            # graph_y is the row in the graph where the data point should be plotted
            if y == graph_y:
                line += '*'
            else:
                line += ' '
        line += '|'  # adds the vertical axis
        print(line)  # prints the whole line of the graph

    # draw the bottom axis
    print("     +" + "-" * width + "+")

    # draw the x-axis labels
    x_labels = "     "
    for i in range(width):
        if i % 10 == 0:
            x_labels += f"{i // 10:>2}"  # labels added every 10 units
        else:
            x_labels += " "
    print(x_labels)

    # print("\nX-axis: Time")
    # print("Y-axis: Price")









if __name__ == '__main__':
    clear_console()
    #columns, rows = os.get_terminal_size()
    #print(f"Terminal size: {columns} columns and {rows} rows")

    # Initialize market and portfolios
    market = stock_market()
    market.add_stock("PLZA", 20.00, -5, 5)
    market.add_stock("BLVD", 5.00, -10, 10)
    market.add_stock("DRVE", 0.01, -15, 15)

    player_name = "Name"
    player1_portfolio = portfolio("Player1", market)
    player2_portfolio = portfolio(player_name, market)
    player3_portfolio = portfolio(player_name, market)
    player4_portfolio = portfolio(player_name, market)

    # Create threads
    graph_chart_thread = threading.Thread(target=build_graph, args=())
    stock_display_thread = threading.Thread(target=display_stock_prices, args=(market,))
    user_input_thread = threading.Thread(target=handle_user_input, args=(player1_portfolio,))


    # Start threads
    graph_chart_thread.start()
    stock_display_thread.start()
    user_input_thread.start()

    # Join threads to keep the program running
    graph_chart_thread.join()
    stock_display_thread.join()
    user_input_thread.join()



   # while not condition:
   #     current_time = time.time()
   #     seconds_passed = current_time - last_time
   #     last_time = current_time
   #
   #
   #     market.display_time()
   #     market.display_stock_prices()
   #
   #
   #     market.update_time(seconds_passed)
   #     market.update_stock_prices()
   #     time.sleep(1)
   #     #just temporary so the loop doesn't go forever
   #     if(counter == 10):
   #         condition = False
   #     counter += 1
   #     print(f"\a")



