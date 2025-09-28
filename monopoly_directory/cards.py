import random
from monopoly_directory.board import Board
from monopoly_directory.player_class import MonopolyPlayer
from utils.screenspace import g

class Cards:
    """
    Cards class for Monopoly game\n
    Contains card data.\n
    """
    def __init__(self) -> None:
        self.chance = g.get('chance cards text').split("\n")
        self.community_chest = g.get('community chest text').split("\n")
        random.shuffle(self.chance)
        random.shuffle(self.community_chest)
    def draw_chance(self, p: MonopolyPlayer, board: Board, players) -> str:
        """
        Draw chance card\n
        """
        self.chance.append(self.chance.pop(0))

        card_number = int(self.chance[-1].split(".")[0])
        if (card_number == 1): 
            board.update_location(p, p.location, 39)
        elif(card_number == 2): 
            board.update_location(p, p.location, 0)
        elif(card_number == 3):
            board.update_location(p, p.location, 24)
        elif(card_number == 4): 
            board.update_location(p, p.location, 11)
        elif(card_number == 5):
            if p.location < 5 or p.location > 35:
                board.update_location(p, p.location, 5)
            elif p.location < 15:
                board.update_location(p, p.location, 15)
            elif p.location < 25:
                board.update_location(p, p.location, 25)
            else:
                board.update_location(p, p.location, 35)
        elif(card_number == 6): 
            if p.location < 5 or p.location > 35:
                board.update_location(p, p.location, 5)
            elif p.location < 15:
                board.update_location(p, p.location, 15)
            elif p.location < 25:
                board.update_location(p, p.location, 25)
            else:
                board.update_location(p, p.location, 35)
        elif(card_number == 7): 
            if p.location < 12 or p.location > 28:
                board.update_location(p, p.location, 12)
            else:
                board.update_location(p, p.location, 28)
        elif(card_number == 8): 
            p.receive(50)
        elif(card_number == 9): 
            p.jail_cards += 1
        elif(card_number == 10): 
            board.update_location(p, p.location, p.location - 3)
        elif(card_number == 11): 
            p.jail = True
            board.update_location(p, p.location, 10)
        elif(card_number == 12): 
            for property in p.properties:
                if(board.locations[property].houses == 5):
                    p.pay(150) #price for 4 houses x1.5
                elif(board.locations[property].houses > 0):
                    p.pay(25*board.locations[property].houses)
        elif(card_number == 13):
            p.pay(15)
        elif(card_number == 14):
            board.update_location(p, p.location, 5)
        elif(card_number == 15):
            for receiver in players:
                p.pay(50)
                receiver.receive(50)
        elif(card_number == 16): 
            p.receive(150)
        return self.chance[-1]
    def draw_community_chest(self, p: MonopolyPlayer, board: Board, players) -> str:
        """
        Draw community chest card\n
        """
        self.community_chest.append(self.community_chest.pop(0))

        card_number = int(self.community_chest[-1].split(".")[0])
        if (card_number == 1):
            board.update_location(p, p.location, 0)
        elif (card_number == 2):
            p.receive(200)
        elif (card_number == 3):
            p.pay(50)
        elif (card_number == 4): 
            p.receive(50)
        elif (card_number == 5):
            p.jail_cards += 1
        elif (card_number == 6):
            p.go_to_jail()
        elif (card_number == 7):
            p.receive(100)
        elif (card_number == 8):
            p.receive(20)
        elif (card_number == 9):
            for payer in players:
                payer.pay(10)
                p.receive(10)
        elif (card_number == 10):
            p.receive(100)
        elif (card_number == 11):
            p.pay(100)
        elif (card_number == 12):
            p.pay(50)
        elif (card_number == 13):
            p.receive(25)
        elif (card_number == 14): 
            for property in p.properties:
                if(board.locations[property].houses == 5):
                    p.pay(240) #price for 4 houses x1.5
                elif(board.locations[property].houses > 0):
                    p.pay(40*board.locations[property].houses)
        elif (card_number == 15):
            p.receive(10)
        elif (card_number == 16):
            p.receive(100)
        return self.community_chest[-1]
