class Player: 
    """
    Player class for Monopoly game\n
    Contains player data.\n
    """
    def __init__(self, cash:int, order:int) -> None:
        self.cash = cash
        self.properties = []
        self.order = order
        self.location = 0
        self.jail = False
        self.jailcards = 0
        self.name = "Player " + str(order + 1)
    """
    Player cash\n
    @cash: int\n
    Player properties\n
    @properties: list\n
    Player location\n
    @location: int\n
    Player jail status\n
    @jail: bool\n
    """
    def buy(self, location:int, board) -> None:
        """
        Buy property\n
        @location: int\n
        """
        self.properties.append(location)
        self.cash -= board.locations[location].getPrice()
        if (board.locations[location].owner == -1):
            board.locations[location].owner = self.order
            if location == 5 or location == 15 or location == 25 or location == 35: # railroad
                owned_rails = [k for k in [5, 15, 25, 35] if board.locations[k].owner == self.order]
                for k in owned_rails:
                    board.locations[k].houses = len(owned_rails)   
            elif location == 12: # electric company, check if water works is owned
                if board.locations[28].owner == self.order:
                    board.locations[12].houses = 2
                    board.locations[28].houses = 2
                else: board.locations[12].houses = 1
            elif location == 28: # water works, check if electric company is owned
                if board.locations[12].owner == self.order:
                    board.locations[28].houses = 2
                    board.locations[12].houses = 2
                else: board.locations[28].houses = 1
    def pay(self, amount:int) -> None:
        """
        Pay amount\n
        @amount: int\n
        """
        self.cash -= amount
    def receive(self, amount:int) -> None:
        """
        Receive amount\n
        @amount: int\n
        """
        self.cash += amount
    def jail(self) -> None:
        """
        Go to jail\n
        """
        self.location = 10
        self.jail = True
    def leave_jail(self) -> None:
        """
        Leave jail\n
        """
        self.jail = False

    def __str__(self) -> str:
        return f"Player {self.order}"