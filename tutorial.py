# monopoly notes
"""
turn based game, goal is to make money from other players while not going bankrupt
each turn player rolls 2 die, move around board clockwise
start on go (BR), 200 collected for passing
land on property, able to buy it if you can afford it
land on others' property, pay defined rent amount
rent can be increased by buying houses
utility/railroad: fixed rent, increases depending on other owned utility/railroad (seperate)
roll doubles, roll again, if 3 in a row go to jail tile, done collect money
jail: cant leave until you roll doubles or 3 turns
community chest/chance: given a card that may or may not benefit/move player
"""

# board info
"""
notes:
blue is comm chest
orange is chance
dark grey are railroads
SOMETHING are utilities
BR is go
BL is jail
TL is free parking
TR is go to jail
the color of the bottom right of a tile corresponds to player color
the  number of green voxels following that correspond to number of other util/railroads owned or number of houses
players represented by a colored tile with circle   '
"""

#notes for implementation
"""
- must be skipable
- possibly add additional argument for starting game without getting tutorial screen/question
- info section on different screens, enter to continue to next section screen
"""