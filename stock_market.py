import random
import time
from datetime import datetime, timedelta
import os
import threading
import keyboard


# hello
# hi


stocks = ["PLZA", "BLVD", "DRVE"]
current_index = 0
selected_stock = None
graph_display_mode = False
mode = None
transaction_amount = 0


# portfolio class will be owned by players
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
                stock_price = self.stock_market.get_stock_price(stock_ticker)  # fetch the latest price
                portfolio_lines.append(f"{stock_ticker}: {num_shares} shares, Price: ${stock_price:.5f}")
                has_stocks = True
        if not has_stocks:
            portfolio_lines.append("No stocks owned.")
        return portfolio_lines


# stock class will contain attributes for an individual stock including
# individual methods for updating the stock price that can be adjusted if
# the stock is a large/mid/small-cap stock
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
        if new_price <= 0.00001:
            new_price = 0.01
        return new_price

    def get_price(self):
        return self.price

    def shares_owned(self):
        return self.num_shares_owned

    def display_price(self):
        print(f"{self.ticker}: ${self.price:.5f}")


# stock market class that will centralize the broader stock market
# and allow for broader changes across stocks when certain in-game
# actions occur (ex: boardwalk is bought to every stock is subject to
# a certain type of change) and this class will hold individual stock objects
# in a dictionary
class stock_market:
    def __init__(self):
        self.stocks = {}
        self.players = []
        self.current_time = datetime(2024, 9, 16, 9, 0, 0)

    def add_stock(self, stock_ticker, stock_price, min_percent_change, max_percent_change):
        # stock is an instance of the stock class
        self.stocks[stock_ticker] = stock(stock_ticker, stock_price, min_percent_change, max_percent_change)

    def update_stock_prices(self):
        for each_stock in self.stocks.values():
            '''method in the stock class so each stock
           can individually update its price allowing
           for unique movements for each stock (ex:
           large-cap will have less volatility vs small-cap)'''
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
        # increment time by minutes. 5 real-world seconds = 1 hour (60 minutes in-game)
        self.current_time += timedelta(minutes=12)

    def display_time(self):
        # display current time in "Day HH:MM AM/PM" format
        return f"Current time: {self.current_time.strftime('%A %I:%M %p')}"


# general functions outside of classes
# function to clear the console
def clear_console():
    if os.name == 'nt':
        _ = os.system('cls')  # For Windows
    else:
        _ = os.system('clear')  # For macOS/Linux


def display_stock_prices(market):
    times_run = 0
    while True:
        print("\033[?25l", end="")
        # stock prices on the left
        times_run += 1
        stock_lines = market.display_stock_prices()
        if times_run % 2 == 0:
            market.update_time(times_run/2)
        current_time = market.display_time()

        # portfolio and user input on the right
        portfolio_lines = player1_portfolio.display_portfolio()

        # move the cursor to row 0, column 0 and print the current time
        print(f"\033[1;0H" + " " * 30)
        print(f"\033[1;0H\033[32m{current_time}\033[0m")

        for i in range(len(stock_lines)):
            if(i < 5):
                print(f"\033[{3 + i};0H" + " " * 30)
                print(f"\033[{3 + i};0H{stock_lines[i]}")
            elif i >= 5:
                print(f"\033[{3 + i };0H" + " " * 30)
                print(f"\033[{3 + i };0H{stock_lines[i]}")

        for i in range(len(portfolio_lines)):
            print(f"\033[{i + 17};41H{portfolio_lines[i]}")

        #update the stock prices
        market.update_stock_prices()

        # sleep to control the update rate
        time.sleep(0.5)
        print("\033[?25h", end="")






def build_graph():
    width, height = 35, 10  # adjusted for terminal size
    data = [random.randint(0, 100) for _ in range(50)]
    selected_stock_prices = []
    # creates array data with random values
    while True:  # infinite loop that:
        # clear_console()  # clears
        if selected_stock != None and graph_display_mode == True:
            stock_obj = market.stocks[selected_stock]
            selected_stock_prices.append(stock_obj.get_price())
            # add current price

            if len(selected_stock_prices) > width:  # maintain size
                selected_stock_prices.pop(0)  # deletes old value

            draw_graph(selected_stock_prices, width, height)  # draws graph
            time.sleep(0.5)  # pauses for 0.5 seconds
        else:
            draw_graph(data, width, height)  # draws graph
            data.append(random.randint(0, 100))  # adds value
            data.pop(0)  # deletes oldest value
            time.sleep(0.5)


def draw_graph(data, width, height):
    max_value = max(data)
    min_value = min(data)
    start_of_graph_row = 16
    scaled_data = []

    # print("\n" * 10)
    if selected_stock != None:
        scale_factor = 10000
        scaled_data = [(value * scale_factor) for value in data]
        max_value = max(scaled_data)
        min_value = min(scaled_data)

    # draw the top axis
    print(f"\033[1;35H" + "     +" + "-" * width + "+")
    # width is the total number of columns available for graph

    # iterates from height to 0 to print each line of the graph
    counter = 0
    for y in range(height, -1, -1):
        counter += 1
        label = f"{y:.1f}"
        line = f"{label:>4} |"  # formats y-axis labels with width of 2 char
        for x in range(width):  # iterates over each column of the graph from 0 to width - 1

            if selected_stock == None:
                value_index = int(x * len(data) / width)
                # scales column index to range of data list and converts to int
                value = data[value_index]  # index in data list that corresponds to current column x
            else:
                value_index = int(x * len(scaled_data) / width)
                value = scaled_data[value_index]

            if max_value == min_value:
                graph_y = height
            else:
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
        print(f"\033[{1 + counter};35H{line}")  # prints the whole line of the graph

    # draw the bottom axis
    print(f"\033[{1 + counter + 1};35H" + "     +" + "-" * width + "+")

    # draw the x-axis labels
    x_labels = "     "
    for i in range(width):
        if i % 10 == 0:
            x_labels += f"{i // 10:>2}"  # labels added every 10 units
        else:
            x_labels += " "
    print(f"\033[{1 + counter + 2};35H{x_labels}")


    # print("\nX-axis: Time")
    # print("Y-axis: Price")
    # sys.stdout.write("\033[7;0H" + "> " + "\033[0m")

    # print(f"\033[6;0H> ")


# keyboard functionality

def move_up():
    global current_index, transaction_amount
    if mode:
        transaction_amount += 1
    else:
        if current_index > 0:
            current_index -= 1
    print_menu()


def move_down():
    global current_index, transaction_amount
    if mode:
        if transaction_amount > 0:
            transaction_amount -= 1
    else:
        if current_index < len(stocks) - 1:
            current_index += 1
    print_menu()

def select_stock():
    global selected_stock, transaction_amount, mode, graph_display_mode
    if mode:
        print(f"\n{mode.capitalize()}ing {transaction_amount} shares of {selected_stock}.")
        if mode == "buy":
            player1_portfolio.buy_stock(selected_stock, transaction_amount)
            print("\a")
        if mode == "sell":
            player1_portfolio.sell_stock(selected_stock, transaction_amount)
            print("\a")
        selected_stock = None
        transaction_amount = 0
        mode = None
        print_menu()
    else:
        selected_stock = stocks[current_index]
        graph_display_mode = False
        print_menu()

def display_graph():
    global selected_stock, graph_display_mode
    if selected_stock:
        graph_display_mode = True
        print(f"\033[15;0HDisplaying graph for: {selected_stock}")
        build_graph()



def print_menu():
    for i in range(17, 24):
        print(f"\033[{i};0H{' ' * 30}")

    print("\033[17;0H" + "Select a stock:")
    for i, stock in enumerate(stocks):
        if i == current_index:
            print(f"\033[{18 + i};0H> {stock}")
        else:
            print(f"\033[{18 + i};0H  {stock}")
    if selected_stock:
        print(f"\033[{18 + len(stocks)};0H" + f"You selected: {selected_stock}")
        if mode == "buy" or mode == "sell":
            print(f"\033[{19 + len(stocks)};0H" + f"Transaction amount: {transaction_amount}")

def buy_mode():
    global mode
    if selected_stock:
        mode = "buy"
        print_menu()

def sell_mode():
    global mode
    if selected_stock:
        mode = "sell"
        print_menu()

def listen_for_keys():
    print_menu()
    keyboard.add_hotkey('w', move_up)
    keyboard.add_hotkey('s', move_down)
    keyboard.add_hotkey('enter', select_stock)
    keyboard.add_hotkey('g', display_graph)
    keyboard.add_hotkey('ctrl+b', buy_mode)
    keyboard.add_hotkey('ctrl+s', sell_mode)
    keyboard.wait('esc')


if __name__ == '__main__':
    clear_console()
    # columns, rows = os.get_terminal_size()
    # print(f"Terminal size: {columns} columns and {rows} rows")

    # initialize market and portfolios
    market = stock_market()
    market.add_stock("PLZA", 20.00, -5, 5)
    market.add_stock("BLVD", 5.00, -10, 10)
    market.add_stock("DRVE", 0.01, -15, 15)

    market.add_stock("DMMY1", 20.00, -5, 5)
    market.add_stock("DMMY2", 5.00, -10, 10)
    market.add_stock("DMMY3", 0.01, -15, 15)
    market.add_stock("DMMY4", 20.00, -5, 5)
    market.add_stock("DMMY5", 5.00, -10, 10)
    market.add_stock("DMMY6", 0.01, -15, 15)
    market.add_stock("DMMY7", 0.01, -15, 15)

    player_name = "Name"
    player1_portfolio = portfolio("Player1", market)
    player2_portfolio = portfolio(player_name, market)
    player3_portfolio = portfolio(player_name, market)
    player4_portfolio = portfolio(player_name, market)

    # create threads
    graph_chart_thread = threading.Thread(target=build_graph, args=())
    stock_display_thread = threading.Thread(target=display_stock_prices, args=(market,))
    keyboard_listener_thread = threading.Thread(target=listen_for_keys, args=())

    # start threads
    graph_chart_thread.start()
    stock_display_thread.start()
    keyboard_listener_thread.start()

    # join threads to keep the program running
    graph_chart_thread.join()
    stock_display_thread.join()
    keyboard_listener_thread.join()

#    print(f"\a") beep?
