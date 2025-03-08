import networking as net
from screenspace import Terminal
import screenspace as ss
from style import MYCOLORS as COLORS
from socket import socket
import keyboard
import time

class TicTacToe:
    def __init__(self):
        self.board = [['▒' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.gamestate = 'X move'

    def place(self, x:int,y:int) -> bool:
        if self.board[y][x] == '▒':
            self.board[y][x] = self.current_player
            return True
        return False

    def get_board(self) -> str:
        return '\n'.join([''.join(row) for row in self.board])

    def check_winner(self):
        # Check rows, columns and diagonals
        for row in self.board:
            if all(s == self.current_player for s in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == self.current_player for row in range(3)):
                return True
        if all(self.board[i][i] == self.current_player for i in range(3)) or all(self.board[i][2 - i] == self.current_player for i in range(3)):
            return True
        return False

    def is_full(self):
        return all(all(cell != '▒' for cell in row) for row in self.board)

def construct_board(b: list[list[str]]) -> str:
        # Create new board state. 
        board_proper = ""
        for row in b:
            board_proper += "".join(row) + '\n'
        return board_proper

def destruct_board(board: str) -> list[list[str]]:
        """
        Necessary for player.py (in modules.py handler) to 
        interpret the board string sent by the server.
        This saves a lot of headache so the client doesn't
        have to send back and forth delta positions 
        checking if they'll be valid. It also minimizes
        the amount of data saved on player's end. (Design
        philosophy)

        Takes in a current board string and returns a 
        list of lists representing the board, where x
        and y values can be accessed as board[x][y].
        """
        return [list(row) for row in board.split('\n')]

if __name__ == "__main__": # Driver code for 
    ttt = TicTacToe()
    while True:
        print(ttt.get_board())
        if ttt.check_winner():
            print(f"{ttt.current_player} wins!")
            break
        if ttt.is_full():
            print("It's a tie!")
            break
        x,y = map(int, input("Enter x,y: ").split(','))
        ttt.place(x,y)
        ttt.print_board



name = "TicTacToe Module"
author = "https://github.com/adamgulde"
description = "TicTacToe basis for attack module."
version = "1.1" # Moved to its own file
command = "ttt"
help_text = "Type TTT to play someone in TicTacToe."

def run(server: socket, active_terminal: Terminal, player_id: int) -> None:
    """
    Manages the client-side logic for joining and playing a Tic-Tac-Toe game.

    This function interacts with the game server to check for ongoing Tic-Tac-Toe games,
    allow the player to join or create a new game, and handle player moves using keyboard
    input. The game board updates dynamically based on player actions.

    Args:
        server (socket): The socket connection to the game server.
        active_terminal (Terminal): The terminal where the game is displayed.
        player_id (int): The player's unique identifier.

    Returns:
        None
    """
    net.send_message(server, f'{player_id}ttt,getgamestate')
    time.sleep(0.1)
    active_terminal.update("Waiting for server...", padding=True)
    game_data = net.receive_message(server)
    game_id = None 

    def get_printable_board(upper_text: str, board_data: str, lower_text) -> str:
        return f"{upper_text}\n{board_data}\n{lower_text}\nUse WASD to move, Enter to select, Esc to cancel."

    if 'create a new' in game_data:
        active_terminal.update(game_data, padding=True)
        game_id = ss.get_valid_int(prompt='Enter the game id: ', min_val=-1, max_val=0)
        if game_id == -1: # If creating a new game, ask who else is playing.
            while True:
                active_terminal.update("1: Player 1\n2: Player 2\n3: Player 3\n4: Player 4", padding=True)  # TODO: This is hardcoded for now, but should be dynamic
                opponent = ss.get_valid_int(prompt=f"Enter the opponent's ID (1-4), not including your ID): ",
                                            min_val=1, max_val=4)-1 # -1 for zero-indexing

                net.send_message(server, f'{player_id}ttt,joingame,{game_id},{opponent}')
                active_terminal.update("Attempting to join game...", padding=True)
                game_data = net.receive_message(server)
                if 'select a game' in game_data or (('X' in game_data and 'O' in game_data and (not '▒' in game_data)) or '▒' in game_data):
                    break
                else:
                    active_terminal.update(game_data + "\nEnter to continue...", padding=True)
                    input()
        else: 
            active_terminal.update("Not creating a new game.", padding=True)

    if 'select a game' in game_data:
        active_terminal.update(game_data, padding=True)    
        game_id = ss.get_valid_int(prompt='Enter the game id: ', min_val=-1, max_val=10) # 10 is incorrect! temp for now TODO
        # Send the server the game id to join. Should be validated on server side. 
        net.send_message(server, f'{player_id}ttt,joingame,{game_id}')

        # Wait for server to send back the new board
        game_data = net.receive_message(server)
        active_terminal.update(game_data, padding=True)

    if ('X' in game_data and 'O' in game_data and (not '▒' in game_data)) or '▒' in game_data: # If the game data sent back is a board, then we can play the game
        # TODO check this is going to work with player name's that have 'X' or 'O' in them, or hell, with the '▒' character
        simple_board = destruct_board(game_data)
        original_board = destruct_board(game_data)
        x,y = 0,0
        b = construct_board(simple_board)
        active_terminal.update(get_printable_board("New board:", b, f"Coordinates:\n({x},{y})"))

        # Only hook the keyboard after you are definitely IN a game. 
        ss.indicate_keyboard_hook(active_terminal.index) # update terminal border to show keyboard is hooked

        while True:

            if keyboard.read_event().event_type == keyboard.KEY_DOWN:
                simple_board[y][x] = COLORS.RESET + original_board[y][x]
                b = construct_board(simple_board)
                active_terminal.update(get_printable_board("New board:", b, f"Coordinates:\n({x},{y})"))

            if keyboard.is_pressed('w'):
                y = max(0, min(y-1, 2))
            if keyboard.is_pressed('a'):
                x = max(0, min(x-1, 2))
            if keyboard.is_pressed('s'):
                y = max(0, min(y+1, 2))
            if keyboard.is_pressed('d'):
                x = max(0, min(x+1, 2))

            simple_board[y][x] = COLORS.backYELLOW + original_board[y][x] + COLORS.RESET
            time.sleep(0.05)
            b = construct_board(simple_board)
            active_terminal.update(get_printable_board("New board:", b, f"Coordinates:\n({x},{y})"))
            
            if keyboard.is_pressed('enter'):
                # Send move to server
                if '▒' in simple_board[y][x]:
                    # At this point, the client can be sure that they have the
                    # correct game ID and that the move is valid. Thus, we add
                    # the game ID to the move string.
                    net.send_message(server, f'{player_id}ttt,move,{game_id},{x}.{y}')
                    # receive new board (for display) from server
                    active_terminal.update("Updated board:\n" + net.receive_message(server), padding=True)
                    ss.update_terminal(active_terminal.index, active_terminal.index) # reset terminal to normal
                    keyboard.unhook_all()
                    break
                else:
                    active_terminal.update(get_printable_board("New board:", b, f"Coordinates:\n({x},{y})\nInvalid move. Try again."))

            if keyboard.is_pressed('esc'):
                ss.update_terminal(active_terminal.index, active_terminal.index) # reset terminal to normal
                keyboard.unhook_all()
                break