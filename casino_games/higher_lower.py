# BLACKJACK
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import player
import random
import screenspace as ss
from style import get_graphics
from style import COLORS 


game_title = "🃑 Higher Lower"
#Templates for the cards
            # 0         1         2      3      4
card_temp = ["┌───┐", "│   │", "│ ", " │", "└───┘"] # This is not in ASCII.txt due to its strange composition.
cards = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "1 0": 10, "A": 1, "J": 11, "K": 13, "Q": 12}

header = "─" * ((75 - len(game_title)) // 2) + game_title + "─" * ((75 - len(game_title)) // 2)
#Renders the hand given, if there are 0s, it renders empty hands
def render_hand(active_terminal, hand = '0', previous = '0'): 
    dealer_hand_str = "═" * ((75 - 13) // 2) + "Next Hand" + "═" * ((75 - 13) // 2) +"\n"
    for i in range(0,4):
        dealer_hand_str += " " * ((75 - (1 * 6)) // 2)
        if(i == 2):
            if(previous == "1 0"):
                dealer_hand_str += card_temp[i].replace(" ", "") + previous + card_temp[i+1].replace(" ", "") + " "
            elif(previous != '0'):
                dealer_hand_str += card_temp[i] + previous + card_temp[i+1] + " "
            else:
                dealer_hand_str += card_temp[i] + " " + card_temp[i+1] + " "
        elif(i == 3):
            dealer_hand_str += card_temp[i+1] + " "
        else:
            dealer_hand_str += card_temp[i] + " "
        dealer_hand_str += "\n"
    hand_str = "═" * ((75 - 9) // 2) + "Your Hand" + "═" * ((75 - 9) // 2) +"\n"
    for i in range(0,4):
        hand_str += " " * ((75 - (1 * 6)) // 2)
        if(i == 2):
            if(hand == "1 0"):
                hand_str += card_temp[i].replace(" ", "") + hand + card_temp[i+1].replace(" ", "") + " "
            elif(hand != '0'):
                hand_str += card_temp[i] + hand + card_temp[i+1] + " "
            else:
                hand_str += card_temp[i] + " " + card_temp[i+1] + " "
        elif(i == 3):
            hand_str += card_temp[i+1] + " "
        else:
            hand_str += card_temp[i] + " "
        hand_str += "\n"

    
    ss.update_quadrant(active_terminal, header + f"\n\n{dealer_hand_str}" + '\n' * 5 + f"{hand_str}" + '\n')
#This finds the multiplyer for a bet that is won.
def findMult(hand, choice):
    if(choice =='l'):
        diff = cards[hand] - 1
        if(diff < 4):
            return 5
        elif(diff <6):
            return 2
        else:
            return 1.75
    else:
        diff = 13 - cards[hand]
        if(diff < 4):
            return 5
        elif(diff <6):
            return 2
        else:
            return 1.75

#Draws a random card
def draw():
    card_type = random.choice(list(cards.keys()))
    return card_type
#This is one turn of higher lower
def turn(active_terminal, turn, bankroll, previous = "0"):
    if(previous == "0"):
        previous = draw() 
    render_hand(active_terminal, previous)
    print(f'Bankroll: {bankroll}')
    choice = input(f"\rPlayer {turn}: is the next card higher or lower? (h/l) or q to quit     ") 
    booly = (choice == 'h' or choice == 'l' or choice == 'q')
    while(not(booly)):
        print("\033[H\033[J", end="")
        render_hand(active_terminal, previous)
        print(f'Bankroll: {bankroll}')
        choice = input(f"\rPlayer {turn}: is the next card higher or lower? (h/l) or q to quit     ") 
        booly = (choice == 'h' or choice == 'l' or choice == 'q')


    if(choice == 'q'): 
        return("q", previous)
    ss.overwrite("\r" + " " * 40)
    next = draw()      
    render_hand(active_terminal,previous,next)
    result = ''
    if(cards[next] < cards[previous]):
        result = 'l'
    elif(cards[next] > cards[previous]):
        result = 'h'

    if(next == previous):
        input(f"\rPlayer {turn}: TIE!")
        ss.overwrite("\r" + " " * 40)
        return (1,next)
    elif(choice == result):
        input(f"\rPlayer {turn}: Correct!")
        ss.overwrite("\r" + " " * 40)
        return (findMult(previous, result), next) 
    else:
        input(f"\rPlayer {turn}: Wrong!")
        ss.overwrite("\r" + " " * 40)
        return (0,next)
    
#Actual game logic
def play(active_terminal, bet, bankroll):
    """
    Higher/Lower
    
    Initializes a basic one-player game of higher/lower for casino.py
    Returns the wager to be sent to the player
    """  
    start = bankroll   
    previous = "0"
    while(bankroll-bet >=0):  
        bankroll = bankroll - bet
        choice,previous = turn(active_terminal,1, bankroll, previous)
        if(str(choice) == 'q'): 
            bankroll = bankroll + bet
            break 
        bankroll = bet*choice + bankroll
        print("\033[H\033[J", end="")
    print("\033[H\033[J", end="") 
    round(bankroll,2)
    if(start < bankroll):
        print(f"\r You won {bankroll - start}!!!!!")
    elif(start  > bankroll):
        print(f"\r You lost {start - bankroll}")
    else:
        print(f"\r You won because you did not lose!!!!!")
    return bankroll
if __name__ == "__main__":
    play(1,1,500) 
    
