from properties import Property
from style import MYCOLORS as COLORS
from player_class import MonopolyPlayer

class Board:
    """
    Board class for Monopoly game\n
    Contains location data.\n
    """
    def __init__(self, num_players) -> None:
        # owner var indicates who owns, but also is used for special codes below:
        # Special codes: -1 is not owned, -2 is mortaged, -3 is community chest, -4 is chance, -5 is tax
        # -6 is jail, -7 is go to jail, -8 is free parking, -9 is luxury, -10 is go 
        property = Property(num_players, "Go", -10, (32,72), COLORS.LIGHTGRAY, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.locations = {
            0: Property(num_players, "Go", -10, (32,72), COLORS.LIGHTGRAY, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            1: Property(0, "Mediterranean Avenue", -1, (32,65), COLORS.BROWN, 60, 50, 2, 10, 30, 90, 160, 250, 30),
            2: Property(0, "Community Chest", -3, (32,58), COLORS.COMMUNITY, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            3: Property(0, "Baltic Avenue", -1, (32,51), COLORS.BROWN, 60, 50, 4, 20, 60, 180, 320, 450, 30),
            4: Property(0, "Income Tax", -5, (32,44), COLORS.LIGHTGRAY, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            5: Property(0, "Reading Railroad", -1, (32,37), COLORS.LIGHTBLACK, 200, 0, 0, 25, 50, 100, 200, 0, 100),
            6: Property(0, "Oriental Avenue", -1, (32,30), COLORS.LIGHTBLUE, 100, 50, 6, 30, 90, 270, 400, 550, 50),
            7: Property(0, "Chance", -4, (32,23), COLORS.CHANCE, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            8: Property(0, "Vermont Avenue", -1, (32,16), COLORS.LIGHTBLUE, 100, 50, 6, 30, 90, 270, 400, 550, 50),
            9: Property(0, "Connecticut Avenue", -1, (32,9), COLORS.LIGHTBLUE, 120, 50, 8, 40, 100, 300, 450, 600, 60),
            10: Property(0, "Jail", -6, (32,2), COLORS.LIGHTGRAY, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            11: Property(0, "St. Charles Place", -1, (29,2), COLORS.ROUGE, 140, 100, 10, 50, 150, 450, 625, 750, 70),
            12: Property(0, "Electric Company", -1, (26,2), COLORS.YELLOW, 150, 0, 0, 4, 10, 0, 0, 0, 75),
            13: Property(0, "States Avenue", -1, (23, 2), COLORS.ROUGE, 140, 100, 10, 50, 150, 450, 625, 750, 70),
            14: Property(0, "Virginia Avenue", -1, (20, 2), COLORS.ROUGE, 160, 100, 12, 60, 180, 500, 700, 900, 80),
            15: Property(0, "Pennsylvania Railroad", -1, (17,2), COLORS.LIGHTBLACK, 200, 0, 0, 25, 50, 100, 200, 0, 100),
            16: Property(0, "St. James Place", -1, (14,2), COLORS.ORANGE, 180, 100, 14, 70, 200, 550, 750, 950, 90),
            17: Property(0, "Community Chest", -3, (11,2), COLORS.COMMUNITY, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            18: Property(0, "Tennessee Avenue", -1, (8,2), COLORS.ORANGE, 180, 100, 14, 70, 200, 550, 750, 950, 90),
            19: Property(0, "New York Avenue", -1, (5,2), COLORS.ORANGE, 200, 100, 16, 80, 220, 600, 800, 1000, 100),
            20: Property(0, "Free Parking", -8, (2,2), COLORS.LIGHTGRAY, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            21: Property(0, "Kentucky Avenue", -1, (2,9), COLORS.RED, 220, 150, 18, 90, 250, 700, 875, 1050, 110),
            22: Property(0, "Chance", -4, (2,16), COLORS.CHANCE, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            23: Property(0, "Indiana Avenue", -1, (2,23), COLORS.RED, 220, 150, 18, 90, 250, 700, 875, 1050, 110),
            24: Property(0, "Illinois Avenue", -1, (2,30), COLORS.RED, 240, 150, 20, 100, 300, 750, 925, 1100, 120),
            25: Property(0, "B&O Railroad", -1, (2,37), COLORS.LIGHTBLACK, 200, 0, 0, 25, 50, 100, 200, 0, 100),
            26: Property(0, "Atlantic Avenue", -1, (2,44), COLORS.YELLOW, 260, 150, 22, 110, 330, 800, 975, 1150, 130),
            27: Property(0, "Ventnor Avenue", -1, (2,51), COLORS.YELLOW, 260, 150, 22, 110, 330, 800, 975, 1150, 130),
            28: Property(0, "Water Works", -1, (2,58), COLORS.CYAN, 150, 0, 0, 4, 10, 0, 0, 0, 75),
            29: Property(0, "Marvin Gardens", -1, (2,65), COLORS.YELLOW, 280, 150, 24, 120, 360, 850, 1025, 1200, 140),
            30: Property(0, "Go To Jail", -7, (2,72), COLORS.LIGHTGRAY, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            31: Property(0, "Pacific Avenue", -1, (5,72), COLORS.GREEN, 300, 200, 26, 130, 390, 900, 1100, 1275, 150),
            32: Property(0, "North Carolina Avenue", -1, (8,72), COLORS.GREEN, 300, 200, 26, 130, 390, 900, 1100, 1275, 150),
            33: Property(0, "Community Chest", -3, (11,72), COLORS.COMMUNITY, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            34: Property(0, "Pennsylvania Avenue", -1, (14,72), COLORS.GREEN, 320, 200, 28, 150, 450, 1000, 1200, 1400, 160),
            35: Property(0, "Short Line", -1, (17,72), COLORS.LIGHTBLACK, 200, 0, 0, 25, 50, 100, 200, 0, 100),
            36: Property(0, "Chance", -4, (20,72), COLORS.CHANCE, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            37: Property(0, "Park Place", -1, (23,72), COLORS.BLUE, 350, 200, 35, 175, 500, 1100, 1300, 1500, 175),
            38: Property(0, "Luxury Tax", -9, (26,72), COLORS.LIGHTGRAY, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            39: Property(0, "Boardwalk", -1, (29,72), COLORS.BLUE, 400, 200, 50, 200, 600, 1400, 1700, 2000, 200),
        }

    def update_location(self, player:MonopolyPlayer, roll: int, new = None) -> None:
        """
        Update location with player\n
        @location: int\n
        @player: Player object\n
        """
        if(new == None):
            new_location = player.location + roll
            if new_location > 39:
                new_location -= 40
                player.receive(200)
            self.locations[player.location].players.remove(player.order)
            self.locations[new_location].players.append(player.order)
            player.location = new_location

            if(roll == -1):
                self.locations[player.location].players.remove(player.order)
                self.locations[10].players.append(player.order)
                player.location = 10
        else: # Used mostly for chance and community chest cards (roll = old location, new = new location)
            if roll > new and new != 10 and new != player.location-3:
                player.receive(200)
            self.locations[roll].players.remove(player.order)
            self.locations[new].players.append(player.order)
            player.location = new
        
    def current_location(self, player:MonopolyPlayer) -> int:
        """
        Return current location\n
        @player: Player object\n
        """
        return player.location
