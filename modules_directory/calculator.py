from utils.utils import Terminal
from utils.utils import MYCOLORS as COLORS
from socket import socket
from utils.utils import set_cursor

name = "Calculator Module"
command = "calc"
author = "https://github.com/adamgulde"
version = "1.3"
help_text = "Type CALC to view your inventory. Use a calculator."
persistent = True # Should be able to run additional commands after switching
# No out of focus function needed, because nothing will happen when the terminal is out of focus

calculator_history_queue = []
calculator_history_current_capacity = 15

def run(server: socket, active_terminal: Terminal, player_id: int):
    #Clears "calc" from command line.
    for i in range (0, 5):
            set_cursor(i,45)
            print(" ")
    
    """
    A command-line calculator module that supports basic arithmetic operations.

    This function provides a terminal-based calculator where users can input mathematical
    expressions, which are evaluated recursively. The results are displayed in the terminal,
    and a history of recent calculations is maintained. Users can exit the calculator by
    typing 'e'.

    Args:
        active_terminal (Terminal): The terminal interface where the calculator operates.

    Returns:
        str: The last computed result or an error message.
    """

    active_terminal.persistent = persistent

    # Helper function that contructs terminal printing.
    def calculator_terminal_response(footer_option: int) -> str:
        calculator_header = "\nCALCULATOR TERMINAL\nHistory: (Enter 'c' to clear)\n"
        footer_options = ["Awaiting an equation...\nPress 'e' to exit the calculator terminal.", 
                      COLORS.BLUE+"Type 'calc' to begin the calculator!", 
                      COLORS.RED+"Equation either malformed or undefined! Try again!\nPress 'e' to exit the calculator terminal"+COLORS.RESET]
        response = calculator_header
        for i in range(len(calculator_history_queue)-1, -1, -1):
            response += calculator_history_queue[i][0]
        response += '\n' + footer_options[footer_option]
        
        return response
    
    #Helper function to update calculator history
    def update_history(equation: str) -> None:
        global calculator_history_current_capacity

        numLines = (len(equation)//75) + 1
        while(numLines > calculator_history_current_capacity):
            calculator_history_current_capacity += calculator_history_queue[0][1]
            calculator_history_queue.pop(0)
        
        calculator_history_current_capacity -= numLines
        calculator_history_queue.append((equation, numLines))

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

    # Initial comment in active terminal
    active_terminal.update(calculator_terminal_response(0), padding=True)
    # All other work is done on the work line (bottom of the screen)
    while True:
            
        response = '\nCALCULATOR TERMINAL\n' 
        digit_result = 0
        print("\r", end='')
        equation = input(COLORS.GREEN)

        for i in range (0, len(equation)+1):
            set_cursor(i,45)
            print(" ")

        print(COLORS.RESET, end="")
        if(equation == "e"):
            active_terminal.update(calculator_terminal_response(1), padding=True)
            break
        elif(equation == "c"):
            calculator_history_queue.clear()
            active_terminal.update(calculator_terminal_response(0))
            continue

        #Trims unnecessary spaces and pads operators with spaces
        equation = equation.replace(" ", "")
        for op in ['+', '-', '*', '/', '%', '^']:
            equation = equation.replace(op, " " + op + " ")
        #Removes spaces from negative number
        if(len(equation) > 1 and equation[1] == '-'):
            equation = "-" + equation[3:]

        try:
            digit_result = calculate(equation)
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

            player_equation = wrappedResponse

            print(COLORS.RESET, end='')
            update_history(player_equation)
            active_terminal.update(calculator_terminal_response(0))
        except:
            active_terminal.update(calculator_terminal_response(2), padding=True)
