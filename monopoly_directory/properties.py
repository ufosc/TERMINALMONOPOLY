from style import MYCOLORS as COLORS

class Property:
    """
    Property class for Monopoly game\n
    Contains location data.\n
    """
    name = "Go"
    players = list(range(0))
    houses = 0
    owner = -10
    owner_name = "Unowned"
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
    modifier = 1 # Multiplier for rent based on shop upgrades

    def __init__(self, num_players:int, name:str, owner:int, position:tuple, color:str, purchasePrice:int, housePrice:int, rent:int, rent1H:int, rent2H:int, rent3H:int, rent4H:int, rentHotel:int,mortgage:int) -> None:
        self.players = list(range(num_players))
        self.name = name
        self.owner = owner
        self.owner_name = "Unowned"
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
            rent_values = [self.rent, self.rent1H, self.rent2H, self.rent3H, self.rent4H, self.rentHotel]
            return rent_values[self.houses] * self.modifier

    def get_deed_str(self, is_terminal: bool) -> str:
        """
        Description: 
            Returns a string representation of the deed for the property.

        Parameters:
            is_terminal (bool): Whether the game is in a terminal state. If so, return string formatted for Terminals screen. 
        Returns:

            str: A string representation of the deed for the property.
        """
        deed_str = ""  
        if is_terminal:
            deed_str += self.color + "▓▒▓" * 8 + "█" + "▀" * 25 + "█" + self.color + "▓▒▓" * 8 + "\n" + COLORS.RESET
            deed_str += "=== Property Deed ===".center(75) + "\n"
            deed_str += self.color + "▓▒▓" * 8 + "█" + "▄" * 25 + "█" + self.color + "▓▒▓" * 8 + "\n" + COLORS.RESET
            deed_str += f"Property: {self.color}{self.name}{COLORS.RESET}\n"
            deed_str += f"Owner: {self.owner_name} (Player ID: {self.owner})\n" if self.owner != -1 else "Owner: Unowned\n"
            deed_str += f"Houses: {self.houses}\n"
            deed_str += f"Purchase Price: {self.purchasePrice}\n"
            deed_str += f"House Price: {self.housePrice}\n"
            deed_str += f"Rent: {self.rent}\n"
            deed_str += f"Rent w 1 House: {self.rent1H}\n"
            deed_str += f"Rent w 2 Houses: {self.rent2H}\n"
            deed_str += f"Rent w 3 Houses: {self.rent3H}\n"
            deed_str += f"Rent w 4 Houses: {self.rent4H}\n"
            deed_str += f"Rent w Hotel: {self.rentHotel}\n"
        return deed_str