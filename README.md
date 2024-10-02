<p align="center">
  <img src="https://github.com/user-attachments/assets/ea1839ed-fdfc-487e-935e-6876131d00fa" alt="TM logo", class="center">!
</p>

## The last game your computer will play...

# Table of Contents
- [What is TERMINALMONOPOLY?](#what-is-terminalmonopoly)
- [Installation](#installation)
- [Instructions](#instructions)
- [Game Commands](#game-commands)
- [How the Game Works](#how-the-game-works)
- [Customization](#customization)
- [Contributing](#contributing)

# What is TERMINALMONOPOLY? 
Terminal Monopoly is a rapid-pace, eclectic game which merges a classic board game with retro graphics, while satisfying the modern need of constant stimulation. Played entirely over a computer's command line, Terminal Monopoly brings nostalgic feelings of ancient terminal games on the first computers, while ensuring anyone can play due to the minimal graphical and computing requirements.

Terminal Monopoly is only 25% board game. Inspired by inane but hilarious Yakuza-type side quests, overcomplicated mechanics like in Cookie Clicker, and minigames such as those in Mario Party, Terminal Monopoly has so much more to offer than just rolling dice.

Terminal Monopoly is written entirely in Python. The source code is available on GitHub

An initial release of Terminal Monopoly is expected to be completed by the end of Fall 2024 (roughly December).

# Installation
Ensure you have the following installed: 
- Python 3.10+
- install necessary python packages using pip
- run using python monopoly.py

# Instructions
- Banker runs the entire game and manages whose turn it is
- Player will take turns rolling dice, moving across the board, and choosing whether or not to buy a property.
- Each play can see the gameboard in real time, and the banker will oversee the purchasing of property and rent payments

# Game Commands
Inputting these commands in the terminal will cause an action: 
- roll: rolls two dice so the player can move
- buy: purchases an unowned property when landing on it. 
- deed <prop info>: will show you detailed property info such as rent and mortgage
- properties: will list the properties that a player owns
- mortgage: mortgages a property to raise money
- pay: Pays an amount to another player or to the bank 
- housing: Builds hotels or houses on properties where the player has a monopoly
- Jail: Manages jail-related actions when a player is sent to jail

# How the Game Works
- Player Class: represents each player in the game and tracks player's cash, balance, owned properties, location, jail status. 
- Board Class: Handles the game board, managing properties, whether a property is owned or mortgaged, and player locations. This class uses an internal dictionary to store information regarding price, rents, and whethere someone owns a property.
- Card Class: Manages the chance and community chest cards, applies effects to the player
- Update_location(player, roll) Updates the player's location after a dice has been rolled, if the pass go they recieve 200 dollars, also manages actions like landing on Jail or Free Parking
- refresh_board(): This function redraws the ASCII game board and displays the current state of properties, players, and special locations like card draws 
- buy_logic(): Handles the logic for purchasing a property, if a player lands on an unowned property they can buy it

# Customization
For the purposes of testing the program, the number of players and starting cash can be edited using the script: 
- Starting Money: Modify 'CASH = 2000' to adjust the initial cash. 
- Number of Players: Change 'num_players = 4' to set how many people are in the game

# Contributing
Interested in adding to Terminal Monopoly? This is a beginner-friendly project that anyone should feel welcome to work on. Check out CONTRIBUTING.md for how to get started.


With regards to troubleshooting, this program logs errors to an `errorlog.txt` file using the `log_error()` function.
This records error messages along with the current date and time, making it easier to identify and debug issues.
If for any reason you encounter an error while testing, the error will automatically be logged here.

The base Terminal Monopoly game will have a large collection of modules which should promote a large number of playstyles, but if you have ideas for modules, code them up and create a pull request! This game is always looking for creative additions. 

In the future, Terminal Monopoly may support "direct modding," that is, an interface will be available which will make module creation very simple. 
