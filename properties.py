import style as s
from style import COLORS

class Property:
    """
    Property class for Monopoly game\n
    Contains location data.\n
    """
    name = "Go"
    players = list(range(0))
    houses = 0
    owner = -10
    position = (32, 72)
    x = position[0]
    y = position[1]
    color = COLORS.LIGHTGRAY
    purchasePrice = 0
    housePrice = 0
    rent = 0
    rent1H = 0
    rent2H = 0
    rent3H = 0
    rent4H = 0
    rentHotel = 0
    mortgage = 0
    mortgaged = False

    def __init__(self, num_players:int, name:str, owner:int, position:tuple, color:COLORS, purchasePrice:int, housePrice:int, rent:int, rent1H:int, rent2H:int, rent3H:int, rent4H:int, rentHotel:int,mortgage:int) -> None:
        self.players = list(range(num_players))
        self.name = name
        self.owner = owner
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.color = color
        self.purchasePrice = purchasePrice
        self.housePrice = housePrice
        self.rent = rent
        self.rent1H = rent1H
        self.rent2H = rent2H
        self.rent3H = rent3H
        self.rent4H = rent4H
        self.rentHotel = rentHotel
        self.mortgage = mortgage
    
    def getPrice(self) -> int:
        if self.purchasePrice == 0:
            return -1
        return self.purchasePrice

    def getRent(self) -> int:
        if self.purchasePrice != 0:
            match self.houses:
                case 0:
                    return self.rent
                case 1:
                    return self.rent1H
                case 2:
                    return self.rent2H
                case 3:
                    return self.rent3H
                case 4:
                    return self.rent4H
                case 5:
                    return self.rentHotel


# Old Code: (In case there was a mistake in transferring the data values)
        '''self.locations = {
            # locations[x][3] indicates who owns, but also is used for special codes below:
                # Special codes: -1 is not owned, -2 is mortaged, -3 is community chest, -4 is chance, -5 is tax
                # -6 is jail, -7 is go to jail, -8 is free parking, -9 is luxury, -10 is go 
        0: ["Go", list(range(num_players)), 0, -10, (32,72), COLORS.LIGHTGRAY],
        1: ["Mediterranean Avenue", [], 0, -1, (32,65), COLORS.BROWN],
        2: ["Community Chest", [], 0, -3, (32, 58), COLORS.COMMUNITY],
        3: ["Baltic Avenue", [], 0, -1, (32, 51), COLORS.BROWN],
        4: ["Income Tax", [], 0, -5, (32, 44), COLORS.LIGHTGRAY],
        5: ["Reading Railroad", [], 0, -1, (32, 37), COLORS.LIGHTBLACK],
        6: ["Oriental Avenue", [], 0, -1, (32, 30), COLORS.LIGHTBLUE],
        7: ["Chance", [], 0, -4, (32, 23), COLORS.CHANCE],
        8: ["Vermont Avenue", [], 0, -1, (32, 16), COLORS.LIGHTBLUE],
        9: ["Connecticut Avenue", [], 0, -1, (32, 9), COLORS.LIGHTBLUE],
        10: ["Jail", [], 0, -7, (32, 2), COLORS.LIGHTGRAY],
        11: ["St. Charles Place", [], 0, -1, (29, 2), COLORS.ROUGE],
        12: ["Electric Company", [], 0, -1, (26, 2), COLORS.YELLOW],
        13: ["States Avenue", [], 0, -1, (23, 2), COLORS.ROUGE],
        14: ["Virginia Avenue", [], 0, -1, (20, 2), COLORS.ROUGE],
        15: ["Pennsylvania Railroad", [], 0, -1, (17, 2), COLORS.LIGHTBLACK],
        16: ["St. James Place", [], 0, -1, (14, 2), COLORS.ORANGE],
        17: ["Community Chest", [], 0, -3, (11, 2), COLORS.COMMUNITY],
        18: ["Tennessee Avenue", [], 0, -1, (8, 2), COLORS.ORANGE],
        19: ["New York Avenue", [], 0, -1, (5, 2), COLORS.ORANGE],
        20: ["Free Parking", [], 0, -8, (2, 2), COLORS.LIGHTGRAY],
        21: ["Kentucky Avenue", [], 0, -1, (2, 9), COLORS.RED],
        22: ["Chance", [], 0, -4, (2, 16), COLORS.CHANCE],
        23: ["Indiana Avenue", [], 0, -1, (2, 23), COLORS.RED],
        24: ["Illinois Avenue", [], 0, -1, (2, 30), COLORS.RED],
        25: ["B&O Railroad", [], 0, -1, (2, 37), COLORS.LIGHTBLACK],
        26: ["Atlantic Avenue", [], 0, -1, (2, 44), COLORS.YELLOW],
        27: ["Ventnor Avenue", [], 0, -1, (2, 51), COLORS.YELLOW],
        28: ["Water Works", [], 0, -1, (2, 58), COLORS.CYAN],
        29: ["Marvin Gardens", [], 0, -1, (2, 65), COLORS.YELLOW],
        30: ["Go To Jail", [], 0, -7, (2, 72), COLORS.LIGHTGRAY],
        31: ["Pacific Avenue", [], 0, -1, (5, 72), COLORS.GREEN],
        32: ["North Carolina Avenue", [], 0, -1, (8, 72), COLORS.GREEN],
        33: ["Community Chest", [], 0, -3, (11, 72), COLORS.COMMUNITY],
        34: ["Pennsylvania Avenue", [], 0, -1, (14, 72), COLORS.GREEN],
        35: ["Short Line", [], 0, -1, (17, 72), COLORS.LIGHTBLACK],
        36: ["Chance", [], 0, -4, (20, 72), COLORS.CHANCE],
        37: ["Park Place", [], 0, -1, (23, 72), COLORS.BLUE],
        38: ["Luxury Tax", [], 0, -9, (26, 72), COLORS.LIGHTGRAY],
        39: ["Boardwalk", [], 0, -1, (29, 72), COLORS.BLUE]
    }'''
        """Dictionary of Monopoly locations\n
        @locations: {int: [str, list, int, bool]}\n
        key: number
        value: [name, players, number of houses [0-4], owned, (x,y) coordinates on gameboard, color code]"""
        '''self.deeds = {"Mediterranean Avenue": (60, 50, 2, 10, 30, 90, 160, 250, 30),
                    "Baltic Avenue":          (60, 50, 4, 20, 60, 180, 320, 450, 30),
                    "Oriental Avenue":        (100, 50, 6, 30, 90, 270, 400, 550, 50),
                    "Vermont Avenue":         (100, 50, 6, 30, 90, 270, 400, 550, 50),
                    "Connecticut Avenue":     (120, 50, 8, 40, 100, 300, 450, 600, 60),
                    "St. Charles Place":      (140, 100, 10, 50, 150, 450, 625, 750, 70),
                    "States Avenue":          (140, 100, 10, 50, 150, 450, 625, 750, 70),
                    "Virginia Avenue":        (160, 100, 12, 60, 180, 500, 700, 900, 80),
                    "St. James Place":        (180, 100, 14, 70, 200, 550, 750, 950, 90),
                    "Tennessee Avenue":       (180, 100, 14, 70, 200, 550, 750, 950, 90),
                    "New York Avenue":        (200, 100, 16, 80, 220, 600, 800, 1000, 100),
                    "Kentucky Avenue":        (220, 150, 18, 90, 250, 700, 875, 1050, 110),
                    "Indiana Avenue":         (220, 150, 18, 90, 250, 700, 875, 1050, 110),
                    "Illinois Avenue":        (240, 150, 20, 100, 300, 750, 925, 1100, 120),
                    "Atlantic Avenue":        (260, 150, 22, 110, 330, 800, 975, 1150, 130),
                    "Ventnor Avenue":         (260, 150, 22, 110, 330, 800, 975, 1150, 130),
                    "Marvin Gardens":         (280, 150, 24, 120, 360, 850, 1025, 1200, 140),
                    "Pacific Avenue":         (300, 200, 26, 130, 390, 900, 1100, 1275, 150),
                    "North Carolina Avenue":  (300, 200, 26, 130, 390, 900, 1100, 1275, 150),
                    "Pennsylvania Avenue":    (320, 200, 28, 150, 450, 1000, 1200, 1400, 160),
                    "Park Place":             (350, 200, 35, 175, 500, 1100, 1300, 1500, 175),
                    "Boardwalk":              (400, 200, 50, 200, 600, 1400, 1700, 2000, 200)
                    }'''
        """dict[str, tuple]: properties
        Key: title
        Value: tuple with values as follows:\n
            0 - Purchase Price\n
            1 - Price Per House\n
            2 - Rent\n
            3 - Rent w 1 House\n
            4 - Rent w 2 House\n
            5 - Rent w 3 House\n
            6 - Rent w 4 House\n
            7 - Rent w Hotel\n
            8 - Mortgage Value\n
        """
        """
        @RR_VALUES constants for the purchase, rent, mortgage, and color code values of the railroads
    
        RR_VALUES = [200, 25, 50, 100, 200, 100]
        
            Key: title
            Value: tuple with values as follows:
                0 - Purchase Price
                1 - Price / multiplier with 1 property 
                2 - Price / multiplier with 2 properties
                3 - Price with 3 railroads (or -1 if utility)
                4 - Price with 4 railroads (or -1 if utility)
                5 - Mortgage Value
        
        self.special_deeds = {
                "Reading Railroad":       ([value for value in RR_VALUES]),
                "Pennsylvania Railroad":  ([value for value in RR_VALUES]),
                "B&O Railroad":           ([value for value in RR_VALUES]),
                "Short Line":             ([value for value in RR_VALUES]),
                "Electric Company":       (150, 4, 10, -1, -1, 75),
                "Water Works":            (150, 4, 10, -1, -1, 75)
                }
        """