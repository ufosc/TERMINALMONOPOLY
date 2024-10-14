import screenspace as ss
import style as s
import random
from player_class import Player

class PlayerModules():
    # Color literals for printing board
    COLORS = {"BROWN": "\033[38;5;94m",
            "LIGHTBLUE": "\033[38;5;117m",
            "ROUGE": "\033[38;5;162m",
            "ORANGE": "\033[38;5;202m",
            "RED": "\033[38;5;9m",
            "YELLOW": "\033[38;5;226m",
            "GREEN": "\033[38;5;2m",
            "BLUE": "\033[38;5;12m",
            "WHITE": "\033[38;5;15m",
            "CYAN": "\033[38;5;14m",
            "LIGHTGRAY": "\033[38;5;7m"}

    def calculator() -> str:
        """A simple calculator module that can perform basic arithmetic operations."""
        #Uses recursion to calculate.
        def calculate(equation: str) -> float:
            for i in range(0, len(equation)-1):
                if(equation[i] == '+'):
                    eqLeft = equation[:i]
                    eqRight = equation[(i+1):]
                    return calculate(eqLeft) + calculate(eqRight)
            
            for i in range(0, len(equation)-1):
                if(equation[i] == '-'):
                    #Checks for unary operator '-'
                    if(i == 0):
                        eqLeft = "0"
                    else:
                        eqLeft = equation[:i]
                    eqRight = equation[(i+1):]
                    return calculate(eqLeft) - calculate(eqRight)
            
            for i in range(0, len(equation)-1):
                if(equation[i] == '*'):
                    eqLeft = equation[:i]
                    eqRight = equation[(i+1):]
                    return calculate(eqLeft) * calculate(eqRight)

            for i in range(0, len(equation)-1):
                if(equation[i] == '/'):
                    eqLeft = equation[:i]
                    eqRight = equation[(i+1):]
                    return calculate(eqLeft)/calculate(eqRight)
            
            for i in range(0, len(equation)-1):
                if(equation[i] == '%'):
                    eqLeft = equation[:i]
                    eqRight = equation[(i+1):]
                    return calculate(eqLeft)%calculate(eqRight) 
                
            for i in range(0, len(equation)-1):
                if(equation[i] == '^'):
                    eqLeft = equation[:i]
                    eqRight = equation[(i+1):]
                    return calculate(eqLeft) ** calculate(eqRight)
            
            return float(equation)

        response = '\nCALCULATOR TERMINAL\n' 
        digit_result = 0
        print("\r", end='')
        equation = input(s.COLORS.GREEN)
        if(equation == "e"):
            return equation
        
        #Trims unnecessary spaces and pads operators with spaces
        equation = equation.replace(" ", "")
        for op in ['+', '-', '*', '/', '%', '^']:
            equation = equation.replace(op, " " + op + " ")
        
        #Removes spaces from negative number
        if(len(equation) > 1 and equation[1] == '-'):
            equation = "-" + equation[3:]

        try:
            digit_result = calculate(equation)
        except:
            return "error"
            
        responseEQ = f'{equation} = {digit_result}'

        #There are 75 columns for each terminal, making any string longer than 75 characters overflow.
        numOverflowingChar = len(responseEQ) - 75
        lineNumber = 0
        wrappedResponse = ""
        while(numOverflowingChar > 0):
            wrappedResponse += responseEQ[(75*lineNumber):(75*(lineNumber + 1))] + '\n'
            lineNumber = lineNumber + 1
            numOverflowingChar = numOverflowingChar - 75
        
        wrappedResponse += responseEQ[(75*lineNumber):(75*(lineNumber + 1)) + numOverflowingChar] + '\n'
        #response += wrappedResponse

        print(s.COLORS.RESET, end='')
        return wrappedResponse

    def trade():
        pass

    def mortgage():
        pass

    def roll():
        pass

    def gamble():
        pass

    def attack():
        pass

    def stocks():
        pass

    def kill() -> str:
        return s.get_graphics()['skull']

    def disable() -> str:
        result = ('X ' * round(ss.cols/2+0.5) + '\n' + 
                    (' X' * round(ss.cols/2+0.5)) + '\n'
                    ) * (ss.rows//2)
        return result
    
    def make_board(board_pieces) -> list[str]:
        board = [''] * 35
        # Hard coded for board printing specifically
        for i in range(35):
            for j in range(80):
                if board_pieces[i*80+j] != '\n':
                    board[i] += (board_pieces[i*80+j])
        return board
    
class BankerModules():
    pass

class CasinoModule():
    """ Casino Module with various gambling games"""
    def game_select():
        pass
    def black_jack():
        pass
    def coin_flip(player: Player):
        """
        Parameters : player (Player class)
        returns : null

        Description: Allows a player to make a 50/50 wager, if it hits they double their wager
        """
        def get_wager():
            try:
                wagerT = int(input("\033Enter Wager amount"))
                return wagerT
            except:
                print("\033Must enter an integer.")
                return get_wager()
        def get_choice():
            try:
                choiceT = input("\033Heads or Tails? (H/T)")
                if(choiceT == "H"):
                    return 1
                elif(choiceT == "T"):
                    return 0
                else:
                    raise ValueError("\033Invalid choice. Please enter 'H' for Heads or 'T' for Tails.")
            except ValueError as e:
                return get_choice()

        wager = get_wager()
        choice = get_choice()
        flip = random.choice([0, 1])
        if(flip == choice):
            player.cash += wager
        else:
            player -= wager

    def texas_holdem():
        pass