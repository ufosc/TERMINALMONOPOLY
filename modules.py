from colorama import Fore, Style, Back
import screenspace as ss
import style as s

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
        #To-do
        '''
        History
        Left-Justified - DONE
        Keep calculator open after multiple operations
        A proper wrapping for long equations - DONE
        Add eponents - DONE
        Strip extra spaces and pad operators with spaces - DONE
        Add support for unary operator '-' - DONE
        '''
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
        equation = input(Fore.GREEN)
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

        print(Style.RESET_ALL, end='')
        return wrappedResponse

    def deed(title: str) -> str:
        divider = s.get_graphics()['divider']
        response = "PROPERTY LIST TERMINAL\n".center(ss.cols)
        properties = {"Mediterranean Avenue": (60, 50, 2, 10, 30, 90, 160, 250, 30, "\033[38;5;94m"),
                    "Baltic Avenue":          (60, 50, 4, 20, 60, 180, 320, 450, 30, "\033[38;5;94m"),
                    "Oriental Avenue":        (100, 50, 6, 30, 90, 270, 400, 550, 50, "\033[38;5;117m"),
                    "Vermont Avenue":         (100, 50, 6, 30, 90, 270, 400, 550, 50, "\033[38;5;117m"),
                    "Conneticut Avenue":      (120, 50, 8, 40, 100, 300, 450, 600, 60, "\033[38;5;117m"),
                    "St. Charles Place":      (140, 100, 10, 50, 150, 450, 625, 750, 70, "\033[38;5;162m"),
                    "States Avenue":          (140, 100, 10, 50, 150, 450, 625, 750, 70, "\033[38;5;162m"),
                    "Virginia Avenue":        (160, 100, 12, 60, 180, 500, 700, 900, 80, "\033[38;5;162m"),
                    "St. James Place":        (180, 100, 14, 70, 200, 550, 750, 950, 90, "\033[38;5;202m"),
                    "Tennessee Avenue":       (180, 100, 14, 70, 200, 550, 750, 950, 90, "\033[38;5;202m"),
                    "New York Avenue":        (200, 100, 16, 80, 220, 600, 800, 1000, 100, "\033[38;5;202m"),
                    "Kentucky Avenue":        (220, 150, 18, 90, 250, 700, 875, 1050, 110, Fore.RED),
                    "Indiana Avenue":         (220, 150, 18, 90, 250, 700, 875, 1050, 110, Fore.RED),
                    "Illinois Avenue":        (240, 150, 20, 100, 300, 750, 925, 1100, 120, Fore.RED),
                    "Atlantic Avenue":        (260, 150, 22, 110, 330, 800, 975, 1150, 130, "\033[38;5;226m"),
                    "Ventnor Avenue":         (260, 150, 22, 110, 330, 800, 975, 1150, 130, "\033[38;5;226m"),
                    "Marvin Gardens":         (280, 150, 24, 120, 360, 850, 1025, 1200, 140, "\033[38;5;226m"),
                    "Pacific Avenue":         (300, 200, 26, 130, 390, 900, 1100, 1275, 150, Fore.GREEN),
                    "North Carolina Avenue":  (300, 200, 26, 130, 390, 900, 1100, 1275, 150, Fore.GREEN),
                    "Pennsylvania Avenue":    (320, 200, 28, 150, 450, 1000, 1200, 1400, 160, Fore.GREEN),
                    "Park Place":             (350, 200, 35, 175, 500, 1100, 1300, 1500, 175, Fore.BLUE),
                    "Boardwalk":              (400, 200, 50, 200, 600, 1400, 1700, 2000, 200, Fore.BLUE)
                    }
        """dict[str, tuple]: properties
        Key: title
        Value: tuple with values as follows:
            0 - Purchase Price
            1 - Price Per House
            2 - Rent
            3 - Rent w 1 House
            4 - Rent w 2 House
            5 - Rent w 3 House
            6 - Rent w 4 House
            7 - Rent w Hotel
            8 - Mortgage Value
            9 - Color Code
        """
        """
        @RR_VALUES constants for the purchase, rent, mortgage, and color code values of the railroads
        """
        RR_VALUES = [200, 25, 50, 100, 200, 100, Fore.LIGHTBLACK_EX]
        """
            Key: title
            Value: tuple with values as follows:
                0 - Purchase Price
                1 - Price / multiplier with 1 property 
                2 - Price / multiplier with 2 properties
                3 - Price with 3 railroads (or -1 if utility)
                4 - Price with 4 railroads (or -1 if utility)
                5 - Mortgage Value
                6 - Color Code
        """
        special_properties = {
                "Reading Railroad":       ([value for value in RR_VALUES]),
                "Pennsylvania Railroad":  ([value for value in RR_VALUES]),
                "B&O Railroad":           ([value for value in RR_VALUES]),
                "Short Line":             ([value for value in RR_VALUES]),
                "Electric Company":       (150, 4, 10, -1, -1, 75, Fore.YELLOW),
                "Water Works":            (150, 4, 10, -1, -1, 75, Fore.CYAN)
                }
        for key in properties:
            if key.lower().startswith(title.lower()):
                data = properties.get(key)
                break
            else: 
                data = None  
        
        for sp_key in special_properties:
            if sp_key.lower().startswith(title.lower()):
                special_data = special_properties.get(sp_key)
                break
            else: 
                special_data = None
        
        if data is not None:
            response += f"""{data[9]}
    {divider}
        === {key} ===
        Purchase Price: {data[0]}
        Price Per House: {data[1]}
        Rent: {data[2]}
        Rent w 1 house: {data[3]} 
        Rent w 2 houses: {data[4]}
        Rent w 3 houses: {data[5]}
        Rent w 4 houses: {data[6]}
        Rent w hotel: {data[7]}
        Mortgage Value: {data[8]}
    {divider}
            """
        elif special_data is not None:
            response += f"""{special_data[6]}
    {divider}
        === {sp_key} ===
        Purchase Price: {special_data[0]}
        Rent (or multiplier) with 1 locations owned: {special_data[1]}
        Rent (or multiplier) with 2 locations owned: {special_data[2]}
        Rent (or multiplier) with 3 locations owned: {special_data[3]}
        Rent (or multiplier) with 4 locations owned: {special_data[4]}
        Mortgage Value: {special_data[5]}
    {divider}
            """
        else:
            response += Fore.RED + "Unrecognized property!"
        response += Style.RESET_ALL
        return response
        
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