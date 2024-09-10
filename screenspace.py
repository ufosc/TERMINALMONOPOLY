# This file contains the logic for the terminal screen

#TODO rewrite into classes: player & banker
# Terminal total width and height: 150x40
# This matches the default Windows terminal size nicely.
# os.get_terminal_size() should be looked into. 
WIDTH = 150
HEIGHT = 40
import os
from colorama import Fore, Style, Back

class Player:
    ### Player Printing below ###

    # Each quadrant is half the width and height of the screen 
    global rows, cols, quadrant1, quadrant2, quadrant3, quadrant4, active_terminal
    rows = HEIGHT//2
    cols = WIDTH//2

    # Create the quadrants as 2D lists
    quadrant1 = ['1' * cols] * rows
    quadrant2 = ['2' * cols] * rows
    quadrant3 = ['3' * cols] * rows
    quadrant4 = ['4' * cols] * rows
    active_terminal = 1

    def print_board(gameboard: list[str]) -> None:
        """
        Used in printing the gameboard for the player. Overwrites the current screen to display the gameboard. 
        
        Parameters: 
        gameboard (list[str]): A representation of the gameboard as a list of strings. 

        Returns: None
        """
        # clear_screen()
        # Resets cursor position to top left
        print("\033[1A" * (HEIGHT + 4), end='\r')
        
        for y in range(len(gameboard)):
            print(gameboard[y])
        

    def update_quadrant(n: int, data: str) -> None:
        """
        Creates a list of lines from the data string, and pads each line with spaces to match the width of the screen. 

        Parameters: 
        n (int): Quadrant number (1-4)
        data (str): String data to update quadrant. Separate lines must be indicated by \\n. 

        Returns: None

        """
        line_list = data.split('\n')
        for i in range(len(line_list)):
                line_list[i] = line_list[i] + ' ' * (cols - len(line_list[i]))
        for i in range(len(line_list), rows):
            line_list.append(' ' * cols)
        match n:
            case 1:
                global quadrant1
                quadrant1 = line_list
            case 2:
                global quadrant2
                quadrant2 = line_list
            case 3:
                global quadrant3
                quadrant3 = line_list
            case 4:
                global quadrant4
                quadrant4 = line_list

    def update_quadrant_strictly(n: int, data: str):
        """ 
        Same as update_quadrant, but does not pad the lines with spaces.
        
        Could be useful for color formatting where update_quadrant fails.

        Parameters:
        n (int): Quadrant number (1-4)
        data (str): Data to update quadrant. String must be exactly the right length. (i.e. 75*20)

        Returns: None
        """
        line_list = data.split('\n')
        match n:
            case 1:
                global quadrant1
                quadrant1 = line_list
            case 2:
                global quadrant2
                quadrant2 = line_list
            case 3:
                global quadrant3
                quadrant3 = line_list
            case 4:
                global quadrant4
                quadrant4 = line_list

    def update_active_terminal(n: int):
        """
        Updates the active terminal to the given number.

        Parameters:
        n (int): The terminal number to set as active.
        
        Returns: None
        """
        global active_terminal
        active_terminal = n 

    def overwrite(text: str = ""):
        """
        Writes text over 2nd to last line of the terminal (input line).
        
        Use this method regularly.
        
        Parameters: 
        text (str): The text to overwrite with. Default is empty string.

        Returns: None
        """
        print(f'\033[1A\r{text}', end='')

    def clear_screen():
        """
        Naively clears the terminal screen.

        Parameters: None
        Returns: None
        """
        print(Style.RESET_ALL,end='')
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_screen() -> None:
        """
        This function overwrites the previous terminal's display. 
        
        Because Terminal Monopoly is not supposed to 
        repeatedly print lines after lines (there should be no scrollbar in the terminal), this function overwrites 
        all needed information. 
        
        The class variables quadrant1, quadrant2, etc. are iterated through to print each character. Because
        splitting the terminal is entirely artificial to this program, it stops at a hardcoded width value and 
        begins printing the next quadrant.  
        
        Parameters: None
        Returns: None
        """

        # Resets cursor position to top left
        print("\033[1A" * (HEIGHT + 4), end='\r')
        # Prints the top border, with ternary conditions if terminal 1 or 2 are active
        print(Back.BLACK + Fore.LIGHTYELLOW_EX+(Fore.GREEN+'╔' if active_terminal == 1 else '╔')+('═' * (cols))+
            (Fore.GREEN if active_terminal == 1 or active_terminal == 2 else Fore.LIGHTYELLOW_EX) +'╦'
            +(Fore.GREEN if active_terminal == 2 else Fore.LIGHTYELLOW_EX)+('═' * (cols))+'╗' + Fore.LIGHTYELLOW_EX + "   ") # Additional spaces to fill remaining 3 columns
        
        # Prints the middle rows
        for y in range(rows):
            print((Fore.GREEN if active_terminal == 1 else Fore.LIGHTYELLOW_EX)+'║', end=Style.RESET_ALL) 
            for x in range(2*cols):
                if x < cols:
                    print(quadrant1[y][x], end='')
                elif x == cols:
                    print((Fore.GREEN if active_terminal == 1 or active_terminal == 2 else Fore.LIGHTYELLOW_EX)+'║'+Style.RESET_ALL + quadrant2[y][x - cols], end='')
                else:
                    print(quadrant2[y][x-cols], end='') 
            print((Fore.GREEN if active_terminal == 2 else Fore.LIGHTYELLOW_EX)+'║'+Style.RESET_ALL + "   ")
        
        # Middle divider
        print((Fore.GREEN if active_terminal == 1 or active_terminal == 3 else Fore.LIGHTYELLOW_EX)+'╠' + '═' * (cols)
            +Fore.GREEN + '╬' + (Fore.GREEN if active_terminal == 2 or active_terminal == 4 else Fore.LIGHTYELLOW_EX)+ '═' * (cols) + '╣' + Style.RESET_ALL + "   ")
        
        # Prints the bottom rows
        for y in range(rows):
            print((Fore.GREEN if active_terminal == 3 else Fore.LIGHTYELLOW_EX)+'║', end=Style.RESET_ALL) 
            for x in range(2 * cols):
                if x < cols:
                    print(quadrant3[y][x], end='')
                elif x == cols:
                    print((Fore.GREEN if active_terminal == 3 or active_terminal == 4 else Fore.LIGHTYELLOW_EX)+'║'+Style.RESET_ALL + quadrant4[y][x - cols], end='')
                else:
                    print(quadrant4[y][x - cols], end='')
            print((Fore.GREEN if active_terminal == 4 else Fore.LIGHTYELLOW_EX)+'║'+Style.RESET_ALL + "   ")
        
        # Print final row
        print((Fore.GREEN if active_terminal == 3 else Fore.LIGHTYELLOW_EX)+'╚' + '═' * (cols) + 
            (Fore.GREEN if active_terminal == 3 or active_terminal == 4 else Fore.LIGHTYELLOW_EX) +'╩'
                + (Fore.GREEN if active_terminal == 4 else Fore.LIGHTYELLOW_EX) + '═' * (cols) + '╝'+ Style.RESET_ALL + "   ")
        # Fills the rest of the terminal
        print(' ' * WIDTH, end='\r')

    def test_1():
        """Test 1 - Update all quadrants with different characters"""
        input("This visual test contains flashing images. Press enter to continue...")
        quads = ['', '', '', '']
        for row in range(rows):
            for col in range(cols):
                for i in range(0,4):
                    quads[i] += str(i)
                    Player.update_quadrant(i+1, quads[i])
                Player.print_screen()
            for i in range(4):
                quads[i] += '\n'

class Banker:
    ### Banker Printing below ### 
    # Columns are used when printing gameboard with player information.
    global col_len, col1, col2, col3, left_data, right_data
    col_len = (150 - 80)//4
    col1 = ["1" * col_len] * HEIGHT
    col2 = ["2" * col_len] * HEIGHT
    col3 = ["3" * col_len] * HEIGHT
    col3 = ["4" * col_len] * HEIGHT

    left_data = list[str]
    right_data = list[str]

    def append_print_data(data: str, side: str):
        if(side == 'left'):
            left_data.append(data)
        else:
            right_data.append(data)

    def left_print_data() -> list[str]:
        pass

    def right_print_data() -> list[str]:
        pass

    def print_terminal(left_data: list[str], right_data: list[str]):

        # Resets cursor position to top left
        print("\033[1A" * (HEIGHT + 4), end='\r')
        # Prints the top border, with ternary conditions if terminal 1 or 2 are active
        print(Back.BLACK + Fore.LIGHTYELLOW_EX+(Fore.GREEN+'╔' if active_terminal == 1 else '╔')+('═' * (cols))+
            (Fore.GREEN if active_terminal == 1 or active_terminal == 2 else Fore.LIGHTYELLOW_EX) +'╦'
            +(Fore.GREEN if active_terminal == 2 else Fore.LIGHTYELLOW_EX)+('═' * (cols))+'╗' + Fore.LIGHTYELLOW_EX + "   ") # Additional spaces to fill remaining 3 columns
        
        # Prints the middle rows
        for y in range(rows):
            print((Fore.GREEN if active_terminal == 1 else Fore.LIGHTYELLOW_EX)+'║', end=Style.RESET_ALL) 
            for x in range(2*cols):
                if x < cols:
                    print(quadrant1[y][x], end='')
                elif x == cols:
                    print((Fore.GREEN if active_terminal == 1 or active_terminal == 2 else Fore.LIGHTYELLOW_EX)+'║'+Style.RESET_ALL + quadrant2[y][x - cols], end='')
                else:
                    print(quadrant2[y][x-cols], end='') 
            print((Fore.GREEN if active_terminal == 2 else Fore.LIGHTYELLOW_EX)+'║'+Style.RESET_ALL + "   ")
        
        # Middle divider
        print((Fore.GREEN if active_terminal == 1 or active_terminal == 3 else Fore.LIGHTYELLOW_EX)+'╠' + '═' * (cols)
            +Fore.GREEN + '╬' + (Fore.GREEN if active_terminal == 2 or active_terminal == 4 else Fore.LIGHTYELLOW_EX)+ '═' * (cols) + '╣' + Style.RESET_ALL + "   ")
        
        # Prints the bottom rows
        for y in range(rows):
            print((Fore.GREEN if active_terminal == 3 else Fore.LIGHTYELLOW_EX)+'║', end=Style.RESET_ALL) 
            for x in range(2 * cols):
                if x < cols:
                    print(quadrant3[y][x], end='')
                elif x == cols:
                    print((Fore.GREEN if active_terminal == 3 or active_terminal == 4 else Fore.LIGHTYELLOW_EX)+'║'+Style.RESET_ALL + quadrant4[y][x - cols], end='')
                else:
                    print(quadrant4[y][x - cols], end='')
            print((Fore.GREEN if active_terminal == 4 else Fore.LIGHTYELLOW_EX)+'║'+Style.RESET_ALL + "   ")
        
        # Print final row
        print((Fore.GREEN if active_terminal == 3 else Fore.LIGHTYELLOW_EX)+'╚' + '═' * (cols) + 
            (Fore.GREEN if active_terminal == 3 or active_terminal == 4 else Fore.LIGHTYELLOW_EX) +'╩'
                + (Fore.GREEN if active_terminal == 4 else Fore.LIGHTYELLOW_EX) + '═' * (cols) + '╝'+ Style.RESET_ALL + "   ")
        # Fills the rest of the terminal
        print(' ' * WIDTH, end='\r')