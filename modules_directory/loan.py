import keyboard
import os
from utils import screenspace
import time
import re
import networking as net
from socket import socket

g = screenspace.get_graphics()


class LoanScreen:
    def __init__(self, player_id=None, server=None):
        self.__pictures = []
        self.loanScreen = True
        self.gettingLoan = False
        self.low_or_high = None
        self.player_id = player_id
        self.server = server
    
    def process_input(self):
        """
        Checks for key events, includes delay so that multiple keys don't register at once. Returns false if no key is pressed.
        
        """
        if keyboard.is_pressed('y') and not self.gettingLoan:
            self.gettingLoan = True
            time.sleep(0.2)
            return True
        
        elif keyboard.is_pressed('n') and not self.gettingLoan:
            self.loanScreen = False
            time.sleep(0.2)
            return True
        
        elif self.gettingLoan:
            if keyboard.is_pressed('h'):
                self.low_or_high = True
                time.sleep(0.2)
                return True
            
            elif keyboard.is_pressed('l'):
                self.low_or_high = False
                time.sleep(0.2)
                return True
            
            elif keyboard.is_pressed('q'):
                self.gettingLoan = False
                time.sleep(0.2)
                return True
        
        return False
    
    def loanLogic(self):
        """
        Logic for loan options. Returns a bool and int
        """
        if self.low_or_high is None:
            return False, 0
        
        try:
            print("\n\t\t\t\tHow much would you like to take out? ", end="")
            time.sleep(1)
            amntbuffer = input()
            amnt = int(re.sub(r"\D", "", amntbuffer))
            
            
            if self.low_or_high:  # High interest loan
                if amnt > 2000 or amnt <= 0:
                    raise ValueError("High interest loan must be between $0 and $2000.")
                else:
                    return True, amnt
            else:  # Low interest loan
                if amnt > 500 or amnt <= 0:
                    raise ValueError("Low interest loan must be between $0 and $500.")
                else:
                    return True, amnt
        except ValueError as e:
            print(f"\n\t\t\t\t Please enter a valid amount. ")
            time.sleep(1)
            return False, 0
    
    def buildDisplay(self):
        """
        Builds dipslay... that's about it
        
        """
        retval = screenspace.set_cursor_str(0, 0) + g.get('loan')
        
        if self.loanScreen and not self.gettingLoan:
            retval += screenspace.set_cursor_str(3,
                                                 3) + "== Welcome to the office of J.G. Hopworth, esteemed financial lender =="
            retval += screenspace.set_cursor_str(30, 5) + "Would you like to take out a loan? (y/n)"
            
            
        
        elif self.loanScreen and self.gettingLoan:
            retval += screenspace.set_cursor_str(32, 3) + "You may choose a high or low interest loan."
            retval += screenspace.set_cursor_str(33, 5) + "High interest (h) - Up to $2000"
            retval += screenspace.set_cursor_str(33, 6) + "Low interest (l) - Up to $500"
            retval += screenspace.set_cursor_str(33, 8) + "Press (q) to cancel"
            
            if self.low_or_high is not None:
                loan_type = "high" if self.low_or_high else "low"
                retval += screenspace.set_cursor_str(33, 10) + f"Selected: {loan_type} interest loan"
        
        return retval
    
    def displayLoanScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.buildDisplay())


def main(player_id=None, server=None):
    """
        Initializes keyboard hook, displays current state, processes input and handles loan amount.
        
        Args:
            player_id (int): The ID of the player (for networking)
            server (socket): The server socket to communicate with (for networking)
    """
    loan = LoanScreen(player_id, server)
    
    
    keyboard.hook(lambda e: None)
    
    while loan.loanScreen:
       
        loan.displayLoanScreen()
        
       
        update_needed = loan.process_input()
        
        if loan.low_or_high is not None:
            valid_loan, amount = loan.loanLogic()
            if valid_loan:
                loan_type = "high" if loan.low_or_high else "low"
        
                net.send_message(loan.server, f'{loan.player_id}loan {loan_type} {amount}')
                response = net.receive_message(loan.server)
                
                print(f"\nCongratulations! You have taken out a {loan_type} interest loan of ${amount}.")
                print(f"\n{response}")
                
                print("Press any key to continue...")
                keyboard.read_event()
                loan.loanScreen = False
            else:
                loan.low_or_high = None
        
        time.sleep(0.1)


if __name__ == '__main__':
    main()



