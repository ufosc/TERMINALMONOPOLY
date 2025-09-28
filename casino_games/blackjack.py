# BLACKJACK
import random
from utils.screenspace import Terminal, g, overwrite
game_title = "🃑 Blackjack"

            # 0         1         2      3      4
card_temp = ["┌───┐", "│   │", "│ ", " │", "└───┘"] # This is not in ASCII.txt due to its strange composition.
cards = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "1 0": 10, "A": 11, "J": 10, "K": 10, "Q": 10}

header = "─" * ((75 - len(game_title)) // 2) + game_title + "─" * ((75 - len(game_title)) // 2)

def render_hand(active_terminal: Terminal, hand, dealer_hand):
    hand_str = "═" * ((75 - 9) // 2) + "Your Hand" + "═" * ((75 - 9) // 2) +"\n"
    for i in range(0,4):
        hand_str += " " * ((75 - (len(hand) * 6)) // 2)
        for card in hand:
            if(i == 2):
                if(card[2] == False):
                    if(card[1] == "1 0"):
                        hand_str += card_temp[i].replace(" ", "") + card[1] + card_temp[i+1].replace(" ", "") + " "
                    else:
                        hand_str += card_temp[i] + card[1] + card_temp[i+1] + " "
                else:
                    hand_str += card_temp[i] + " " + card_temp[i+1] + " "
            elif(i == 3):
                hand_str += card_temp[i+1] + " "
            else:
                hand_str += card_temp[i] + " "
        hand_str += "\n"

    dealer_hand_str = "═" * ((75 - 13) // 2) + "Dealer's Hand" + "═" * ((75 - 13) // 2) +"\n"
    for i in range(0,4):
        dealer_hand_str += " " * ((75 - (len(dealer_hand) * 6)) // 2)
        for card in dealer_hand:
            if(i == 2):
                if(card[2] == False):
                    if(card[1] == "1 0"):
                        dealer_hand_str += card_temp[i].replace(" ", "") + card[1] + card_temp[i+1].replace(" ", "") + " "
                    else:
                        dealer_hand_str += card_temp[i] + card[1] + card_temp[i+1] + " "
                else:
                    dealer_hand_str += card_temp[i] + " " + card_temp[i+1] + " "
            elif(i == 3):
                dealer_hand_str += card_temp[i+1] + " "
            else:
                dealer_hand_str += card_temp[i] + " "
        dealer_hand_str += "\n"
    
    active_terminal.update(header + f"\n\n{dealer_hand_str}" + '\n' * 5 + f"{hand_str}")

def draw(dealer, hidden,score):
    card_type, card_value = random.choice(list(cards.items()))
    if(card_value == 11 and ((not dealer and score[0] + 11 > 21) or (dealer and score[1] + 11 > 21))):
        card_value = 1
        card_type = "1"
    return [card_value, card_type, hidden]

def turn(active_terminal: Terminal, turn):
    hand = []
    dealer_hand = []
    score = [0,0,0,0]

    input(f"\rPlayer {turn}: DRAW CARD")
    overwrite("\r" + " " * 40)

    hand.append(draw(False, False, score))
    score[turn - 1] += hand[-1][0]
    hand.append(draw(False, False, score))
    score[turn - 1] += hand[-1][0]

    dealer_hand.append(draw(True, False, score))
    score[turn] += dealer_hand[-1][0]
    dealer_hand.append(draw(True, True, score))
    score[turn] += dealer_hand[-1][0]

    render_hand(active_terminal, hand, dealer_hand)

    if(score[turn - 1] == 21):
        dealer_hand[-1][-1] = False
        render_hand(active_terminal, hand, dealer_hand)
        if(score[turn] == 21):
            input(f"\rPlayer {turn}: STAND-OFF!")
            overwrite("\r" + " " * 40)
            return "TIE"
        input(f"\rPlayer {turn}: YOU GOT A NATURAL!")
        overwrite("\r" + " " * 40)
        return "WIN"
    elif(score[turn] == 21):
        dealer_hand[-1][-1] = False
        render_hand(active_terminal, hand, dealer_hand)
        input(f"\rPlayer {turn}: DEALER GOT A NATURAL!")
        overwrite("\r" + " " * 40)
        return "BUST"

    while score[turn - 1] < 21:
        render_hand(active_terminal, hand, dealer_hand)
        choice = input(f"\rPlayer {turn}: You have {score[turn - 1]}. HIT? (y/N)")
        overwrite("\r" + " " * 40)
        if(choice.lower() == "y"):
            input(f"\rPlayer {turn}: DRAW CARD")
            overwrite("\r" + " " * 40)
            hand.append(draw(False, False, score))
            score[turn - 1] += hand[-1][0]
            if(score[turn -1] > 21):
                for card in hand:
                    if(card[1] == "A"):
                        card[0] = 1
                        card[1] = "1"
                        score[turn - 1] -= 10
                        if(score[turn - 1] <= 21): break
            render_hand(active_terminal, hand, dealer_hand)
        else: break
        if(score[turn - 1] > 21):
            input(f"\rPlayer {turn}: YOU BUST!")
            overwrite("\r" + " " * 40)
            return "BUST"
        if(score[turn - 1] == 21):
            dealer_hand[-1][-1] = False
            render_hand(active_terminal, hand, dealer_hand)
            input(f"\rPlayer {turn}: YOU GOT A 21!")
            overwrite("\r" + " " * 40)
            return "WIN"
    
    while(score[turn] < 17):
        dealer_hand.append(draw(True, True, score))
        score[turn] += dealer_hand[-1][0]
        if(score[turn] > 21):
            for card in dealer_hand:
                if(card[1] == "A"):
                    card[0] = 1
                    card[1] = "1"
                    score[turn] -= 10
                    if(score[turn] <= 21): break
    for card in dealer_hand:
        card[-1] = False
    render_hand(active_terminal, hand, dealer_hand)
    if(score[turn] > 21):
        input(f"\rPlayer {turn}: DEALER BUST!")
        overwrite("\r" + " " * 40)
        return "WIN"
    if(score[turn - 1] < score[turn]):
        input(f"\rPlayer {turn}: DEALER WINS!")
        overwrite("\r" + " " * 40)
        return "BUST"
    elif(score[turn - 1] > score[turn]):
        input(f"\rPlayer {turn}: YOU WIN!")
        overwrite("\r" + " " * 40)
        return "WIN"
    else:
        input(f"\rPlayer {turn}: STAND-OFF!")
        overwrite("\r" + " " * 40)
        return "TIE"

def play(active_terminal: Terminal, bet) -> int:
    """
    Blackjack
    
    Initializes a basic one-player game of Blackjack for casino.py
    Returns the wager to be sent to the player
    """
    render_hand(active_terminal, [], [])
    outcome = turn(active_terminal, 1)
    if (outcome == "WIN"):
        active_terminal.update(header + f"\n{g.get('casino_win')}")
        bet *= 2
    elif (outcome == "BUST"):
        active_terminal.update(header + f"\n{g.get('casino_lose')}")
        bet = 0
    elif (outcome == "TIE"):
        active_terminal.update(header + f"\n{g.get('casino_tie')}")
    
    input("\r")
    overwrite("\r" + " " * 40)
    return bet
