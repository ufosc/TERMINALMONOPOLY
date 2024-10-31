import player
import random
import screenspace as ss
import time
from style import get_graphics

suits = ["♥", "♦", "♣", "♠"]
numbers = ["J", "Q", "K", "A"]
cards = []
for i in range(4):
    for j in range(2, 15):
        cards.append((str(j) if j<11 else numbers[j-11]) + suits[i])

def card_value(card) -> int:
    value = int(card[0:-1]) if (card[0:-1] not in numbers) else (11 + numbers.index(card[0:-1]))
    return value

def card_to_str(card):
    if card is None:
        suit = "?"
        number = "?"
    else:
        suit = card[-1]
        number = card[0:-1]
    card_str = " " * 33 + f"┌──────┐" + " " * 34 + "\n"
    card_str += " " * 33 + f"│{number}" + ("     │" if len(number)==1 else "    │") + " " * 34 + "\n"
    card_str += " " * 33 + f"│  {suit}   │" + " " * 34 + "\n"
    card_str += " " * 33 + ("│     " if len(number)==1 else "│    ") + f"{number}│" + " " * 34 + "\n"
    card_str += " " * 33 + f"└──────┘" + " " * 34 + "\n"

    return card_str

def render(card1, card2, wins, losses, total_rounds, active_terminal):
    str_to_render = "─" * 36 + "War" + "─" * 36 + "\n"
    str_to_render += f"You: {wins}" + " " * 23 + f"Best of {total_rounds} battles" + " " * 17 + f"Opponent: {losses}" + "\n" * 2
    str_to_render += card_to_str(card1)
    str_to_render += " " * 30 + "Opponent's card" + " " * 30 + "\n" * 5
    str_to_render += card_to_str(card2)
    str_to_render += " " * 33 + "Your card" + " " * 33 + "\n"

    ss.update_quadrant(active_terminal, str_to_render)

def draw_cards(wins, losses, total_rounds, active_terminal):
    banker_card = None
    card = None
    render(banker_card, card, wins, losses, total_rounds, active_terminal)

    input("Draw a card (press any key)")
    ss.overwrite("\r" + " " * 40)

    card = cards[random.randint(0, 51)]
    render(banker_card, card, wins, losses, total_rounds, active_terminal)
    time.sleep(1)
    banker_card = cards[random.randint(0, 51)]
    render(banker_card, card, wins, losses, total_rounds, active_terminal)
    time.sleep(1)

    if card_value(banker_card) > card_value(card):
        ss.overwrite("You lose")
        time.sleep(1)
        return "LOSE"
    elif card_value(banker_card) < card_value(card):
        ss.overwrite("You win!")
        time.sleep(1)
        return "WIN"
    else:
        ss.overwrite("War!")
        time.sleep(1)
        return draw_cards(wins, losses, total_rounds, active_terminal)

def end(wins, losses, total_rounds, active_terminal):
    banker_card = None
    card = None
    render(banker_card, card, wins, losses, total_rounds, active_terminal)

    graphics = get_graphics()
    win_gfx = graphics["casino_win"]
    lose_gfx = graphics["casino_lose"]

    if wins > total_rounds//2:
        ss.update_quadrant(active_terminal, win_gfx)
        ss.overwrite("\r" + " " * 40)
    else:
        ss.update_quadrant(active_terminal, lose_gfx)
        ss.overwrite("\r" + " " * 40)

def play(active_terminal):
    n = 3  # number of rounds (must be odd)

    wins = 0
    losses = 0

    for _ in range(n):
        match = draw_cards(wins, losses, n, active_terminal)
        if match == "WIN":
            wins += 1
        elif match == "LOSE":
            losses += 1

    end(wins, losses, n, active_terminal)
    time.sleep(1.5)
    ss.update_quadrant(active_terminal, data=None)
    ss.overwrite("\r")


if __name__ == "__main__":
    play(1)
