import asyncio
import random
import sys

# Roulette wheel setup
wheel = [
    (0, "green"), (32, "red"), (15, "black"), (19, "red"), (4, "black"),
    (21, "red"), (2, "black"), (25, "red"), (17, "black"), (34, "red"),
    (6, "black"), (27, "red"), (13, "black"), (36, "red"), (11, "black"),
    (30, "red"), (8, "black"), (23, "red"), (10, "black"), (5, "red"),
    (24, "black"), (16, "red"), (33, "black"), (1, "red"), (20, "black"),
    (14, "red"), (31, "black"), (9, "red"), (22, "black"), (18, "red"),
    (29, "black"), (7, "red"), (28, "black"), (12, "red"), (35, "black"),
    (3, "red"), (26, "black")
]

wheel_numbers = [num for num, _ in wheel]
wheel_colors = {num: color for num, color in wheel}


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
    delay = 0.1  # Initial delay
    max_delay = 0.6  # Slowest speed before stopping
    slow_factor = 1.15  # Slowdown rate

    index = random.randint(0, len(wheel_numbers) - 1)  # Start position
    for _ in range(30):  # Control animation duration
        index = (index + 1) % len(wheel_numbers)  # Move forward

        # Display 8 numbers including the current one with the ball symbol
        display_numbers = []
        for i in range(8):
            num = wheel_numbers[(index + i) % len(wheel_numbers)]
            # Place ball symbol on the current number (middle position)
            if i == 4:
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
