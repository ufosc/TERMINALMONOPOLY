import asyncio
import random
import sys
from utils.utils import Terminal, overwrite, get_valid_int
from utils.utils import set_cursor_str, MYCOLORS as COLORS
from time import sleep

# Roulette wheel setup
# Updated using some python comprehension
wheel = [
    (0, "green", COLORS.GREEN)
] + [(i, "red" if i % 2 == 0 else "black", COLORS.RED if i % 2 == 0 else COLORS.LIGHTBLACK) for i in range(1, 37)]

# Shuffle the wheel to ensure randomness
# Ensure blacks and reds are alternating next to each other
reds = [item for item in wheel if item[1] == "red"]
blacks = [item for item in wheel if item[1] == "black"]
greens = [item for item in wheel if item[1] == "green"]

# Shuffle reds and blacks separately
random.shuffle(reds)
random.shuffle(blacks)

# Interleave reds and blacks
alternating_wheel = []
for red, black in zip(reds, blacks):
    alternating_wheel.append(red)
    alternating_wheel.append(black)

# Add the green slot at the beginning
wheel = greens + alternating_wheel

"""
    Roulette Casino Game
    Author:  https://github.com/useyourshadow
    Version: 1.2 - Integrated with player.py and added colors
    Description: A simple roulette game where players can bet on numbers, colors, or even/odd outcomes to mimic a roulette table.
"""

wheel_numbers = [num for num, _, _ in wheel]
wheel_color_codes = {color: code for _, color, code in wheel}
wheel_colors = {num: color for num, color, _ in wheel}

game_title = "⚂ Roulette"
header = game_title.center(75,"─")

def play(active_terminal: Terminal, bet: int) -> int:
    active_terminal.clear()
    ret_val = header
    ret_val += "\nChoose an option:\n"
    ret_val += "1 - Bet on a single number for a high payout (35x)\n"
    ret_val += "2 - Bet on a color (red/black) for a 2x payout\n"
    ret_val += "3 - Bet on even or odd for a 2x payout\n"

    active_terminal.update(ret_val, padding=False)
    choice = get_valid_int("Enter your choice: ", 1, 3)

    if choice == 1:
        bet_value = get_valid_int("Choose a number (0-36): ", 0, 36)
        if bet_value not in wheel_numbers:
            active_terminal.update(set_cursor_str(0, 5) + "Invalid number! Defaulting to 0.", padding=False)
            bet_value = 0

    elif choice == 2:
        overwrite("Choose a color (red/black): ")
        bet_value = input().lower()
        if bet_value not in ["red", "black"]:
            active_terminal.update(set_cursor_str(0, 5) + "Invalid color! Defaulting to red.", padding=False)
            bet_value = "red"

    elif choice == 3:
        overwrite("Bet on (even/odd): ")
        bet_value = input().lower()
        if bet_value not in ["even", "odd"]:
            active_terminal.update(set_cursor_str(0, 5) + "Invalid choice! Defaulting to even.", padding=False)
            bet_value = "even"
    else:
        active_terminal.update(set_cursor_str(0, 5) + "Invalid choice! Defaulting to betting on red", padding=False)
        choice = 2
        bet_value = "red"

    ret_val = active_terminal.data # update ret_val with the current terminal state, because 

    delay = 0.05  # Initial delay
    max_delay = 0.5  # Slowest speed before stopping
    slow_factor = 1.20  # Slowdown rate

    index = random.randint(0, len(wheel_numbers) - 1)  # Start position
    clear_line = active_terminal.translate_coords(set_cursor_str(1, 10) + " " * 70)
    for _ in range(random.randint(15, 25)):  # Control animation duration
        index = (index + 1) % len(wheel_numbers)  # Move forward

        # Display 12 numbers including the current one with the ball symbol
        display_numbers = []
        for i in range(12):
            num = wheel_numbers[(index + i) % len(wheel_numbers)]
            color = wheel_color_codes[wheel_colors[num]]
            # Place ball symbol on the current number (middle position)
            if i == 6:
                display_numbers.append(f"⊙︎ {color}{num} {COLORS.RESET}" if num < 10 else f"⊙︎{color}{num}{COLORS.RESET}")
            else:
                display_numbers.append(color + (f" {num}" if num < 10 else str(num)))

        # Print the 8 numbers from left to right
        ret_val = set_cursor_str(0, 10) + COLORS.RESET + "Roulette spinning: " + " ".join(display_numbers)
        ret_val = active_terminal.translate_coords(ret_val)
        sys.stdout.write(clear_line)
        sys.stdout.write(ret_val)
        sys.stdout.flush()
        sleep(delay)
        delay = min(delay * slow_factor, max_delay)

    # The winning number is the one with the ball to the right
    winning_number = wheel_numbers[(index + 5) % len(wheel_numbers)]
    winning_color = wheel_colors[winning_number]

    ret_val = set_cursor_str(0, 11) + f"The ball landed on {winning_number} ({winning_color})"
    overwrite("Press enter to continue...")
    input()
    payout = 0
    if choice == 1 and bet_value == winning_number:
        payout = bet * 35
        ret_val += set_cursor_str(0,15) + f"You won! Your payout is ${payout}"
    elif choice == 2 and bet_value == winning_color:
        payout = bet * 2
        ret_val += set_cursor_str(0,15) + f"You won! Your payout is ${payout}"
    elif choice == 3:
        if winning_number == 0:
            ret_val += set_cursor_str(0,15) + "The ball landed on 0, house wins!"
        else:
            is_even = winning_number % 2 == 0
            if (bet_value == "even" and is_even) or (bet_value == "odd" and not is_even):
                payout = bet * 2
                ret_val += set_cursor_str(0,15) + f"You won! Your payout is ${payout}"
            else:
                ret_val += set_cursor_str(0,15) + "You lost!"
    else:
        ret_val += set_cursor_str(0,15) + "You lost!"
    
    ret_val = active_terminal.translate_coords(ret_val)
    sys.stdout.write(ret_val)
    sys.stdout.flush()

    overwrite("Press enter to continue...")
    input()
    return payout

def get_bet():
    bet = int(input("How much do you want to bet? $"))
    print("Choose an option:")
    print("1 - Bet on a single number for a high payout (35x)")
    print("2 - Bet on a color (red/black) for a 2x payout")
    print("3 - Bet on even or odd for a 2x payout")

    choice = int(input("Enter your choice: "))
    bet_value = None

    if choice == 1:
        bet_value = int(input("Choose a number (0-36): "))
        if bet_value not in wheel_numbers:
            print("Invalid number! Defaulting to 0.")
            bet_value = 0

    elif choice == 2:
        bet_value = input("Choose a color (red/black): ").lower()
        if bet_value not in ["red", "black"]:
            print("Invalid color! Defaulting to red.")
            bet_value = "red"

    elif choice == 3:
        bet_value = input("Bet on (even/odd): ").lower()
        if bet_value not in ["even", "odd"]:
            print("Invalid choice! Defaulting to even.")
            bet_value = "even"
    else:
        print("Invalid choice! Defaulting to betting on red")
        choice = 2
        bet_value = "red"

    return bet, choice, bet_value


async def spin_wheel(bet, choice, bet_value):
    num_positions = len(wheel_numbers)  # Ensure ball cycles through all numbers
    delay = 0.05  # Initial delay
    max_delay = 0.5  # Slowest speed before stopping
    slow_factor = 1.20  # Slowdown rate

    index = random.randint(0, len(wheel_numbers) - 1)  # Start position
    for _ in range(30):  # Control animation duration
        index = (index + 1) % len(wheel_numbers)  # Move forward

        # Display 12 numbers including the current one with the ball symbol
        display_numbers = []
        for i in range(12):
            num = wheel_numbers[(index + i) % len(wheel_numbers)]
            # Place ball symbol on the current number (middle position)
            if i == 6:
                display_numbers.append(f"⚪ {num}")
            else:
                display_numbers.append(str(num))

        # Print the 8 numbers from left to right
        sys.stdout.write(f"\rRoulette spinning: {' '.join(display_numbers)}")
        sys.stdout.flush()
        await asyncio.sleep(delay)
        delay = min(delay * slow_factor, max_delay)

    # The winning number is the one with the ball to the right
    winning_number = wheel_numbers[(index + 4) % len(wheel_numbers)]
    winning_color = wheel_colors[winning_number]

    print(f"\nThe ball landed on {winning_number} ({winning_color})")

    payout = 0
    if choice == 1 and bet_value == winning_number:
        payout = bet * 35
        print(f"You won! Your payout is ${payout}")
    elif choice == 2 and bet_value == winning_color:
        payout = bet * 2
        print(f"You won! Your payout is ${payout}")
    elif choice == 3:
        if winning_number == 0:
            print("The ball landed on 0, house wins!")
        else:
            is_even = winning_number % 2 == 0
            if (bet_value == "even" and is_even) or (bet_value == "odd" and not is_even):
                payout = bet * 2
                print(f"You won! Your payout is ${payout}")
            else:
                print("You lost!")
    else:
        print("You lost!")

    return payout



async def main():
    bet, choice, bet_value = get_bet()
    await spin_wheel(bet, choice, bet_value)


if __name__ == "__main__":
    asyncio.run(main())
