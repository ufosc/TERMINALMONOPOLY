import random
import monopoly as m
import style as s
import board

class Cards:
    """
    Cards class for Monopoly game\n
    Contains card data.\n
    """
    def __init__(self) -> None:
        self.chance = s.get_graphics().get('chance cards text').split("\n")
        self.community_chest = s.get_graphics().get('community chest text').split("\n")
        random.shuffle(self.chance)
        random.shuffle(self.community_chest)
    def draw_chance(self, p: m.Player) -> str:
        """
        Draw chance card\n
        """
        self.chance.append(self.chance.pop(0))

        card_number = int(self.chance[-1].split(".")[0])
        match card_number:
            case 1: 
                board.update_location(p, p.location, 39)
            case 2: 
                board.update_location(p, p.location, 0)
            case 3:
                board.update_location(p, p.location, 24)
            case 4: 
                board.update_location(p, p.location, 11)
            case 5:
                if p.location < 5 or p.location > 35:
                    board.update_location(p, p.location, 5)
                elif p.location < 15:
                    board.update_location(p, p.location, 15)
                elif p.location < 25:
                    board.update_location(p, p.location, 25)
                else:
                    board.update_location(p, p.location, 35)
            case 6: 
                if p.location < 5 or p.location > 35:
                    board.update_location(p, p.location, 5)
                elif p.location < 15:
                    board.update_location(p, p.location, 15)
                elif p.location < 25:
                    board.update_location(p, p.location, 25)
                else:
                    board.update_location(p, p.location, 35)
            case 7: 
                if p.location < 12 or p.location > 28:
                    board.update_location(p, p.location, 12)
                else:
                    board.update_location(p, p.location, 28)
            case 8: 
                p.receive(50)
            case 9: 
                p.jailcards += 1
            case 10: 
                board.update_location(p, p.location, p.location - 3)
            case 11: 
                p.jail = True
                board.update_location(p, p.location, 10)
            case 12: 
                for property in p.properties:
                    if(board.locations[property][2] == 5):
                        p.pay(150) #price for 4 houses x1.5
                    elif(board.locations[property][2] > 0):
                        p.pay(25*board.locations[property][2])
            case 13:
                p.pay(15)
            case 14:
                board.update_location(p, p.location, 5)
            case 15:
                for receiver in m.players:
                    p.pay(50)
                    receiver.receive(50)
            case 16: 
                p.receive(150)
        return self.chance[-1]
    def draw_community_chest(self, p: m.Player) -> str:
        """
        Draw community chest card\n
        """
        self.community_chest.append(self.community_chest.pop(0))

        card_number = int(self.community_chest[-1].split(".")[0])
        match card_number:
            case 1:
                board.update_location(p, p.location, 0)
            case 2:
                p.receive(200)
            case 3:
                p.pay(50)
            case 4: 
                p.receive(50)
            case 5:
                p.jailcards += 1
            case 6:
                board.update_location(p, p.location, 10)
                p.jail = True
            case 7:
                p.receive(100)
            case 8:
                p.receive(20)
            case 9:
                for payer in m.players:
                    payer.pay(10)
                    p.receive(10)
            case 10:
                p.receive(100)
            case 11:
                p.pay(100)
            case 12:
                p.pay(50)
            case 13:
                p.receive(25)
            case 14: 
                for property in p.properties:
                    if(board.locations[property][2] == 5):
                        p.pay(240) #price for 4 houses x1.5
                    elif(board.locations[property][2] > 0):
                        p.pay(40*board.locations[property][2])
            case 15:
                p.receive(10)
            case 16:
                p.receive(100)
        return self.community_chest[-1]