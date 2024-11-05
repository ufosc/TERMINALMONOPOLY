# How To Play
## Table of Contents
- [Core Monopoly Game](#core-monopoly-game)
  - [Movement](#movement)
  - [Buying properties](#buying-properties)
  - ...
- [The Terminals](#the-terminals)
  - [Modules](#modules)
    - [Help](#help)
    - [Calculator](#calculator)
    - [Deed Viewing](#deed-viewing)
    - ...
    - [Casino](#casino)
      - [Blackjack](#blackjack)
      - ...
  - [Attacking](#attacking)
    - [Types of attacks](#types-of-attacks)
      - [Fraud](#fraud)
      - ...
## Core Monopoly Game
Bankrupt everyone else and be the last player standing. Only the strongest will survive. 
### Movement
TODO
### Buying properties
TODO
### Improving properties
TODO
### Selling properties
TODO
### Paying rent
TODO
### Trading
TODO
### Jail
TODO

## The Terminals
When not playing the core game, you should switch back to your terminal screen. This is where the real game begins... 

### How To Navigate
TODO 
### Modules

#### Help

#### Calculator

#### Deed Viewing
Shows basic view of deed from core monopoly game, with additional information including current owner, any board-state modifiers, and other information.
#### Shop
- Bonus gameboard items
  - Purchase extra rent on a location for a set number of turns.
  - Move your token to another location.
  - Shuffle chance / community chest
  - Purchase an extra hotel on a location for a set number of turns. 
- Module modifiers
  - Buy fishing equipment
  - Manipulate the stock market
- Terminal repairing
  - Fix a disabled terminal
  - Revive a dead terminal
- Defense items
  - Shield a terminal from successful attacks
  - 

#### Casino
All your gambling dreams, or nightmares, come true here! Gotta spend money to make money!
Note that none of the Casino modules can be used as attack modules, because any player must always wager to play. 
##### Coin Flip
You choose a side, either heads or tails. Once you choose, the coin flips. 
- If it lands on the side you picked, you earn double your wager!
- If it does not land on your side, you lose your wager.

##### Blackjack
The goal of this game is to beat the dealer in getting the highest score without going over 21. The game starts with both of you drawing 2 cards. If you or the dealer draw a natural (total of 21), the game immediately goes to the final stage. If not, you are prompted to either hit and get another card or to stay and keep what you have. If you draw an Ace, it will either be an 11 or 1 based on your current score. If you go over 21, you will bust and lose the game! Once you stay, the dealer will draw until they are at 17 or above. The dealer can also bust and lead to you winning!

If both players are safe, then the game will be decided to 3 outcomes: 
- If you have a higher score than the dealer, you will win double your wager!
- If the dealer has a higher score than you, you will lose your wager.
- If you happen to have the same score as the dealer, the game ends in a stand-off, where you only get your wager back without any extra.

##### Texas Hold 'Em

#### Stock Market

#### Fishing

#### Battleship*
TODO... 
If opposing player takes too long to strike, it will move to the next player's turn. 
#### Tic Tac Toe*
TODO...
If opposing player takes too long to respond, attacking player wins. 
#### Maze*
TODO... 
If opposing player takes too long to respond, this module will become disabled. 
### Attacking
Attacking other players is a crucial part of Terminal Monopoly. Successfully attacking other players will cripple their mobility on their terminals, and put them in precarious situations on the gameboard.
#### Types of Attacks
All attacks are played out by winning against another player in some **active** module. In the [Modules](#modules) section, anything starred (*) can be ran as an attack module. 
##### Fraud
Stealing other player's capital is a quick-and-dirty way to increase your net worth while decreasing theirs.   
- Liquid Capital
  Directly transfer part of their held cash into your account.
- Properties
  Force a player to sell a property to you for free. They immediately sell all houses on that property as per normal Monopoly rules (1/2 price), then transfer the ownership to you.
- Houses
  "Renovate" a player's houses onto your property. They do not lose the property, just a set number of houses / hotels from that location. 

##### DoS
The impact of killing another player's terminal can be severe depending on the current state of the game. Removing effectively 1/4 (or more!) of a player's terminal mobility will decrease their productivity, defenses, and accumulation of capital.
- Disabling a terminal will prevent a player from running any commands on it, and it will automatically be restored after a certain amount of time.
- Killing a terminal will permanently prevent a player from running any commands on it. 
#####
