from screenspace import Terminal
from style import MYCOLORS as COLORS
from socket import socket

name = "Calculator Module"
command = "calc"
author = "https://github.com/adamgulde"
description = "Use a calculator."
version = "1.3"
help_text = "Type CALC to view your inventory."

calculator_history_queue = []
calculator_history_current_capacity = 15

def run(server: socket, active_terminal: Terminal, player_id: int):
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
    # Helper function that contructs terminal printing.
    def calculator_terminal_response(footer_option: int) -> str:
        calculator_header = "\nCALCULATOR TERMINAL\nHistory:\n"
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
        print(COLORS.RESET, end="")
        if(equation == "e"):
            active_terminal.update(calculator_terminal_response(1), padding=True)
            break

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
