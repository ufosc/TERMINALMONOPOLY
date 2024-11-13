import random
import time
from datetime import datetime, timedelta
import os
import threading
import keyboard
import heapq


# hello
# hi


# portfolio class will be owned by players
class portfolio:
    def __init__(self, player_name, stock_market):
        self.player_name = player_name
        self.stock_market = stock_market
        self.owned_stocks = {}
        self.portfolio_stock_names = stock_market.stock_names  # Store all stock names as a list
        for stock_name in self.portfolio_stock_names:  # Iterate through the stock names
            self.owned_stocks.update({stock_name: 0})  # Initialize owned stocks with 0 shares for each stock
        self.current_index_for_arrow = 0
        #default stock is the first one in the list - PLZA
        self.current_selected_stock = "PLZA"
        self.graph_selected_stock = "PLZA"
        self.current_mode = None
        self.current_transaction_amount = 0
        self.total_portfolio_value = 0

    def buy_stock(self, stock_ticker, num_shares):
        count = 0
        if stock_ticker in self.stock_market.stocks.items():
            for key, value in self.owned_stocks:
                if value > 0:
                    count += 1
        if count <= 5:
            self.owned_stocks[stock_ticker] += num_shares

    def sell_stock(self, stock_ticker, num_shares):
        if stock_ticker in self.owned_stocks and self.owned_stocks[stock_ticker] >= num_shares:
            self.owned_stocks[stock_ticker] -= num_shares

    def display_portfolio(self):
        portfolio_lines = [f">> \033[1m{self.player_name}'s Portfolio: ${self.total_portfolio_value:.2f}\033[0m <<"]
        self.total_portfolio_value = 0
        has_stocks = False
        for stock_ticker, num_shares in self.owned_stocks.items():
            if num_shares > 0:
                stock_price = self.stock_market.get_stock_price(stock_ticker)  # fetch the latest price
                self.total_portfolio_value = self.total_portfolio_value + (num_shares * stock_price)
                portfolio_lines.append(f"{stock_ticker}: {num_shares} shares, Equity: ${num_shares * stock_price:.2f}")
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
        self.historical_prices = []
        self.prices_per_day = []
        self.mover_change = 0
        for i in range(35):
            self.historical_prices.append(initial_price)

    def update_price(self):
        self.price = self.fluctuate_stock_price(self.price)
        self.historical_prices.append(round(self.price, 5))
        self.prices_per_day.append(self.price)
        if len(self.prices_per_day) == 5:
            # 240 times per game day   ^^^  (adjust here and at other comment for faster update)
            last_element = self.prices_per_day[-1]
            first_element = self.prices_per_day[0]
            self.mover_change = (last_element - first_element) / first_element * 100
            # self.prices_per_day.clear()

        if len(self.historical_prices) > 35:
            self.historical_prices.pop(0)

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
        self.stock_names = []
        self.stocks = {}
        self.players = []
        self.top_three_movers = []
        heapq.heapify(self.top_three_movers)
        self.current_time = datetime(2024, 9, 16, 9, 0, 0)

    def add_stock(self, stock_ticker, stock_price, min_percent_change, max_percent_change):
        # stock is an instance of the stock class
        self.stocks[stock_ticker] = stock(stock_ticker, stock_price, min_percent_change, max_percent_change)
        self.stock_names.append(stock_ticker)

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
            arrow = "▲" if price_change >= 0 else "▼"  # Green up or red down arrow

            # Place the arrow right before the parentheses with percentage change
            stock_lines.append(
                f"{ticker}: {price_color}${stock_obj.get_price():.5f} {arrow} ({price_change:+.2f}%)\033[0m")

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


def display_stock_prices(market, players_portfolio):
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
        print(f"\033[1;1H" + " " * 40)
        print(f"\033[1;1H\033[32m{current_time}\033[0m")

        for i in range(len(stock_lines)):
            if(i < 5):
                print(f"\033[{2 + i};1H" + " " * 30)
                print(f"\033[{2 + i};1H{stock_lines[i]}")
            elif i >= 5:
                print(f"\033[{2 + i };1H" + " " * 30)
                print(f"\033[{2 + i };1H{stock_lines[i]}")


        if len(market.stocks['BLVD'].prices_per_day) == 5:
            # 240 times per game day                    ^^^  (adjust here and at other comment for faster update)
            top_movers(market)
            for s in market.stocks:
                market.stocks[s].prices_per_day.clear()


        for i in range(len(portfolio_lines)):
            #print(f"\033[{i + 17}:41H" + " " * 40)
            print(f"\033[{i + 17 -1};41H{portfolio_lines[i]}")

        width, height = 35, 10  # adjusted for terminal size
        draw_graph(market.stocks[players_portfolio.graph_selected_stock].historical_prices, width, height,
                   players_portfolio, market)  # draws graph
        #the print below prints out the list of historical prices so we can visually make sure
        #the prices being pulled are live and accurate
        #print(f"\033[20;1H{market.stocks[players_portfolio.graph_selected_stock].historical_prices}")

        #update the stock prices
        market.update_stock_prices()

        # sleep to control the update rate
        time.sleep(0.5)
        print("\033[?25h", end="")






def build_graph(players_portfolio, market):
    width, height = 35, 10  # adjusted for terminal size
    data = [random.randint(0, 100) for _ in range(50)]
    # creates array data with random values
    while True:  # infinite loop that:
        # clear_console()  # clears
        draw_graph(market.stocks[players_portfolio.graph_selected_stock].historical_prices, width, height, players_portfolio, market)  # draws graph
        print(f"\033[20;1H{market.stocks[players_portfolio.graph_selected_stock].historical_prices}")
        time.sleep(0.5)  # pauses for 0.5 seconds



def draw_graph(data, width, height, players_portfolio, market):
    max_value = max(data)
    min_value = min(data)
    start_of_graph_row = 16
    scaled_data = []

    # print("\n" * 10)
    if players_portfolio.current_selected_stock != None:
        scale_factor = 10000
        scaled_data = [(value * scale_factor) for value in data]
        max_value = max(scaled_data)
        min_value = min(scaled_data)

    # draw the top axis
    print(f"\033[2;35H" + "     +" + "─" * width + "+")
    # width is the total number of columns available for graph

    # iterates from height to 0 to print each line of the graph
    counter = 0
    for y in range(height, -1, -1):
        counter += 1
        label = f"{market.get_stock_price(players_portfolio.current_selected_stock)- 4 + y:.1f}"
        line = f"{label:>4} │"  # formats y-axis labels with width of 2 char
        for x in range(width):  # iterates over each column of the graph from 0 to width - 1

            value = data[x]

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
        line += '│'  # adds the vertical axis
        print(f"\033[{2 + counter};35H{line}")  # prints the whole line of the graph

    # draw the bottom axis
    print(f"\033[{2 + counter + 1};35H" + "     +" + "─" * width + "+")

    # draw the x-axis labels
    x_labels = "     "
    for i in range(width):
        if i % 10 == 0:
            x_labels += f"{i // 10:>2}"  # labels added every 10 units
        else:
            x_labels += " "
    print(f"\033[{2 + counter + 2};35H{x_labels}")

    print(f"\033[1;45HDisplaying graph for: {players_portfolio.graph_selected_stock}")

# keyboard functionality
def move_up(players_portfolio):
    if players_portfolio.current_mode:
        players_portfolio.current_transaction_amount += 10
    else:
        players_portfolio.current_index_for_arrow -= 1
        if players_portfolio.current_index_for_arrow < 0:
            players_portfolio.current_index_for_arrow = len(players_portfolio.portfolio_stock_names) - 1
    print_menu(players_portfolio)


def move_down(players_portfolio):
    if players_portfolio.current_mode:
        if players_portfolio.current_transaction_amount > 0:
            players_portfolio.current_transaction_amount -= 10
    else:
        players_portfolio.current_index_for_arrow += 1
        if players_portfolio.current_index_for_arrow > len(players_portfolio.portfolio_stock_names) - 1:
            players_portfolio.current_index_for_arrow = 0
    print_menu(players_portfolio)

def select_stock(players_portfolio):
    if players_portfolio.current_mode:
        if players_portfolio.current_mode == "buy":
            players_portfolio.buy_stock(players_portfolio.current_selected_stock, players_portfolio.current_transaction_amount)
            print("\a")
        if players_portfolio.current_mode == "sell":
            players_portfolio.sell_stock(players_portfolio.current_selected_stock, players_portfolio.current_transaction_amount)
            print("\a")
        #players_portfolio.current_selected_stock = None
        players_portfolio.current_transaction_amount = 0
        players_portfolio.current_mode = None
        print_menu(players_portfolio)
    else:
        players_portfolio.current_selected_stock = players_portfolio.portfolio_stock_names[players_portfolio.current_index_for_arrow]
        print_menu(players_portfolio)

def display_graph(players_portfolio, market):
    #making the graph selected stock equal to the current selected stock ensure the
    #graph can only be changed when the player has hit enter on a certain stock. Ex:
    #moving the arrow to a stock and hitting g without hitting enter first to select
    #that stock will now do nothing
    players_portfolio.graph_selected_stock = players_portfolio.current_selected_stock

def print_menu(players_portfolio):
    for i in range(17, 24):
        print(f"\033[{i};1H{' ' * 30}")

    #print("\033[17;1H" + "Select a stock:")
    #print(f"\033[17;1H" + "Selected stock: "  + f"{players_portfolio.current_selected_stock}")
    wrap_stocks_col1 = 10
    wrap_stocks_col2 = 20
    for i, s in enumerate(players_portfolio.portfolio_stock_names):
        if i == players_portfolio.current_index_for_arrow:
            #the if statements are for each column where <= 2 if for the first
            #column and when there are more than three stocks the 3,4,5th stocks
            #will be on the next column at position 10 when 2 < i < 6
            if i <= 2:
                print(f"\033[{17 + i};1H>  {s}")
            elif 2 < i < 6:
                print(f"\033[{17 + i - 3};{wrap_stocks_col1}H>  {s}")
            elif 6 <= i <= 9:
                print(f"\033[{17 + i - 6};{wrap_stocks_col2}H>  {s}")
        else:
            if i <= 2:
                print(f"\033[{17 + i};1H  {s}")
            elif 2 < i < 6:
                print(f"\033[{17 + i - 3};{wrap_stocks_col1}H  {s}")
            elif 6 <= i <= 9:
                print(f"\033[{17 + i - 6};{wrap_stocks_col2}H  {s}")

    if players_portfolio.current_selected_stock:
        print(f"\033[{11 + len(players_portfolio.portfolio_stock_names)};1H" + f"You selected: {players_portfolio.current_selected_stock}")
        if players_portfolio.current_mode == "buy" or players_portfolio.current_mode == "sell":
            print(f"\033[{11 + len(players_portfolio.portfolio_stock_names)};20H" + f"| Amount: {players_portfolio.current_transaction_amount}")
        else:
            print(
                f"\033[{12 + len(players_portfolio.portfolio_stock_names)};1H" + " " * 15)


def buy_mode(players_portfolio):
    if players_portfolio.current_selected_stock:
        players_portfolio.current_mode = "buy"
        print_menu(players_portfolio)

def sell_mode(players_portfolio):
    if players_portfolio.current_selected_stock:
        players_portfolio.current_mode = "sell"
        print_menu(players_portfolio)

def listen_for_keys(players_portfolio, market):
    print_menu(players_portfolio)
    keyboard.add_hotkey('w', lambda:move_up(players_portfolio))
    keyboard.add_hotkey('s', lambda:move_down(players_portfolio))
    keyboard.add_hotkey('enter', lambda:select_stock(players_portfolio))
    keyboard.add_hotkey('g', lambda:display_graph(players_portfolio, market))
    keyboard.add_hotkey('shift+b', lambda:buy_mode(players_portfolio))
    keyboard.add_hotkey('shift+s', lambda:sell_mode(players_portfolio))
    keyboard.wait('esc')


def add_mover(market, mover, change, k):
    if len(market.top_three_movers) < k:
        heapq.heappush(market.top_three_movers, (change, mover))
    else:
        if change > market.top_three_movers[0][0]:
            heapq.heapreplace(market.top_three_movers, (change, mover))

def top_movers(market):
    k = 3
    counter = 0
    for s in market.stocks:
        add_mover(market, market.stocks[s].ticker, market.stocks[s].mover_change, k)

    top_movers_sorted = sorted(market.top_three_movers, reverse=True)
    print(f"\033[12;1H Top Movers:")
    for change, mover in top_movers_sorted:
        #prints out the stock ticker with the current stock's price
        print(f"\033[{13 + counter};1H {mover}: ${market.get_stock_price(mover):.3f}")
        #prints out the green arrow with the percent change in green
        print(f"\033[{13 + counter};15H \033[32m▲ +{change:.2f}%\033[0m")
        counter += 1




if __name__ == '__main__':
    clear_console()
    # columns, rows = os.get_terminal_size()
    # print(f"Terminal size: {columns} columns and {rows} rows")


    # initialize market and portfolios
    market = stock_market()
    market.add_stock("PLZA", 20.00, -5, 5)
    market.add_stock("FISH", 20.00, -5, 5)
    market.add_stock("RCKT", 20.00, -5, 5)
    market.add_stock("BLVD", 5.00, -10, 10)
    market.add_stock("TRIS", 5.00, -10, 10)
    market.add_stock("UTIL", 5.00, -10, 10)
    market.add_stock("DRVE", 0.01, -15, 15)
    market.add_stock("CYBR", 0.01, -15, 15)
    market.add_stock("SYNC", 0.01, -15, 15)

    player_name = "Name"
    player1_portfolio = portfolio("H&S", market)
    player2_portfolio = portfolio(player_name, market)
    player3_portfolio = portfolio(player_name, market)
    player4_portfolio = portfolio(player_name, market)

    # create threads
    #graph_chart_thread = threading.Thread(target=build_graph, args=(player1_portfolio, market,))
    stock_display_thread = threading.Thread(target=display_stock_prices, args=(market, player1_portfolio))
    keyboard_listener_thread = threading.Thread(target=listen_for_keys, args=(player1_portfolio, market,))

    # start threads
    #graph_chart_thread.start()
    stock_display_thread.start()
    keyboard_listener_thread.start()

    # join threads to keep the program running
#    graph_chart_thread.join()
    stock_display_thread.join()
    keyboard_listener_thread.join()