# BLACKJACK
import random
import screenspace as ss
from style import get_graphics
from style import COLORS

game_title = "🃑 Blackjack"

            # 0         1         2      3      4
card_temp = ["┌───┐", "│   │", "| ", " │", "└───┘"] # This is not in ASCII.txt due to its strange composition.
cards = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "1 0": 10, "A": 11, "J": 10, "K": 10, "Q": 10}

header = "─" * ((75 - len(game_title)) // 2) + game_title + "─" * ((75 - len(game_title)) // 2)

def render_hand(player, active_terminal, hand, dealer_hand):
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
                    dealer_hand_str += card_temp[i] + card[1] + card_temp[i+1] + " "
                else:
                    dealer_hand_str += card_temp[i] + " " + card_temp[i+1] + " "
            elif(i == 3):
                dealer_hand_str += card_temp[i+1] + " "
            else:
                dealer_hand_str += card_temp[i] + " "
        dealer_hand_str += "\n"
    
    ss.update_quadrant(active_terminal, header + f"\n\n{dealer_hand_str} {"\n" * 5}{hand_str}")

def draw(player, dealer, hidden,score):
    card_type, card_value = random.choice(list(cards.items()))
    if(card_value == 11 and not dealer and score[0] + 11 > 21):
        card_value = 1
        card_type = "1"
    return [card_value, card_type, hidden]

def turn(player, active_terminal, turn):
    hand = []
    dealer_hand = []
    score = [0,0,0,0]

    input(COLORS.backYELLOW+COLORS.BLACK+f"\rPlayer {turn}: DRAW CARD")
    ss.overwrite("\r" + " " * 40)

    hand.append(draw(player, False, False, score))
    score[turn - 1] += hand[-1][0]
    hand.append(draw(player, False, False, score))
    score[turn - 1] += hand[-1][0]

    dealer_hand.append(draw(player, True, False, score))
    score[turn] += dealer_hand[-1][0]
    dealer_hand.append(draw(player, True, True, score))
    score[turn] += dealer_hand[-1][0]

    render_hand(player, active_terminal, hand, dealer_hand)

    if(score[turn - 1] == 21):
        dealer_hand[-1][-1] = False
        render_hand(player, active_terminal, hand, dealer_hand)
        if(score[turn] == 21):
            input(COLORS.backYELLOW+COLORS.BLACK+f"\rPlayer {turn}: STAND-OFF!")
            ss.overwrite("\r" + " " * 40)
            return "TIE"
        input(COLORS.backYELLOW+COLORS.BLACK+f"\rPlayer {turn}: YOU GOT A NATURAL!")
        ss.overwrite("\r" + " " * 40)
        return "WIN"
    elif(score[turn] == 21):
        dealer_hand[-1][-1] = False
        render_hand(player, active_terminal, hand, dealer_hand)
        input(COLORS.backYELLOW+COLORS.BLACK+f"\rPlayer {turn}: DEALER GOT A NATURAL!")
        ss.overwrite("\r" + " " * 40)
        return "BUST"

    while score[turn - 1] < 21:
        render_hand(player, active_terminal, hand, dealer_hand)
        choice = input(COLORS.backYELLOW+COLORS.BLACK+f"\rPlayer {turn}: You have {score[turn - 1]}. HIT? (y/N)")
        ss.overwrite("\r" + " " * 40)
        if(choice.lower() == "y"):
            input(COLORS.backYELLOW+COLORS.BLACK+f"\rPlayer {turn}: DRAW CARD")
            ss.overwrite("\r" + " " * 40)
            hand.append(draw(player, False, False, score))
            score[turn - 1] += hand[-1][0]
            render_hand(player, active_terminal, hand, dealer_hand)
        else: break
        if(score[turn - 1] > 21):
            input(COLORS.backYELLOW+COLORS.BLACK+f"\rPlayer {turn}: YOU BUST!")
            ss.overwrite("\r" + " " * 40)
            return "BUST"
        if(score[turn - 1] == 21):
            dealer_hand[-1][-1] = False
            render_hand(player, active_terminal, hand, dealer_hand)
            input(COLORS.backYELLOW+COLORS.BLACK+f"\rPlayer {turn}: YOU GOT A 21!")
            ss.overwrite("\r" + " " * 40)
            return "WIN"
    
    while(score[turn] < 17):
        dealer_hand.append(draw(player, True, True, score))
        score[turn] += dealer_hand[-1][0]
    for card in dealer_hand:
        card[-1] = False
    render_hand(player, active_terminal, hand, dealer_hand)
    if(score[turn] > 21):
        input(COLORS.backYELLOW+COLORS.BLACK+f"\rPlayer {turn}: DEALER BUST!")
        ss.overwrite("\r" + " " * 40)
        return "WIN"
    if(score[turn - 1] < score[turn]):
        input(COLORS.backYELLOW+COLORS.BLACK+f"\rPlayer {turn}: DEALER WINS!")
        ss.overwrite("\r" + " " * 40)
        return "BUST"
    elif(score[turn - 1] > score[turn]):
        input(COLORS.backYELLOW+COLORS.BLACK+f"\rPlayer {turn}: YOU WIN!")
        ss.overwrite("\r" + " " * 40)
        return "WIN"
    else:
        input(COLORS.backYELLOW+COLORS.BLACK+f"\rPlayer {turn}: STAND-OFF!")
        ss.overwrite("\r" + " " * 40)
        return "TIE"

def play(player, active_terminal, bet):
    outcome = turn(player, active_terminal, 1)

    graphics = get_graphics()
    match outcome:
        case "WIN":
            ss.update_quadrant(active_terminal, header + f"\n{graphics['casino_win']}")
            bet *= 2
        case "BUST":
            ss.update_quadrant(active_terminal, header + f"\n{graphics['casino_lose']}")
            bet = 0
        case "TIE":
            ss.update_quadrant(active_terminal, header + f"\n{graphics['casino_tie']}")
    
    input("\r")
    ss.overwrite("\r" + " " * 40)
    return bet
