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
        # ss.indicate_keyboard_hook(active_terminal.index) # update terminal border to show keyboard is hooked

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


def handle_ttt(cmds: str, current_client) -> None:
    """
    Handles all TicTacToe requests from the player.
    
    Parameters:
        cmds (str): The command string from the player.
        current_client (Client): The client object associated with the player.
    
    Returns:
        None
    """
    ttt_game = None
    add_to_output_area("TicTacToe", "TicTacToe data requested!")
    if cmds.split(',')[1] == 'getgamestate':
        # Joining a game logic
        # Game does not exist
        if gm.player_in_game('TicTacToe', current_client.name) == True:
            if len(gm.get_game_by_name('TicTacToe')) >= 1:
                add_to_output_area("TicTacToe", "Player is already playing at least one game, need to select a specific game to rejoin.")
                net.send_message(current_client.socket, "\nPlease select a game to join.\n" + gm.display_games(name='TicTacToe', player_name=current_client.name))
        # Player is not in any games
        else: 
            add_to_output_area("TicTacToe", f"Player is not in any games. Can create a game.")
            # Ask player first, then create a game if they want to play.
            sleep(1)
            net.send_message(current_client.socket, "\nYou are not part of any games.\nWould you like to create a new TicTacToe game?\nEnter -1 to create, or 0 to ignore.")
            net.send_notif(current_client.socket, "You are not part of any games. Would you like to create a new TicTacToe game? Enter -1 to create, or 0 to ignore.")
        return

    if cmds.split(',')[1] == 'joingame':
    # Player knows game exists, and is trying to (re)join a game
        game_id = int(cmds.split(',')[2])

        if game_id == -1: # Create a new game.
            # Don't let a player create a new game if they're already in one.. This might be adjusted later TODO debug
            if gm.player_in_game('TicTacToe', current_client.name) == True:
                if len(gm.get_game_by_name('TicTacToe')) >= 1:
                    add_to_output_area("TicTacToe", "Player input -1 when already playing another game, need to select a specific game to rejoin.")
                    net.send_message(current_client.socket, "\nYou're playing a game already! Rejoin from the game list.\n" + gm.display_games(name='TicTacToe', player_name=current_client.name))
                    return
            else: 
                opponent = int(cmds.split(',')[3])
                # Check if valid opponent inputted
                if len(clients) <= opponent or clients[opponent] == None or clients[opponent] == current_client:
                    net.send_message(current_client.socket, "\nInvalid opponent. Please select another player.")
                    return

                add_to_output_area("TicTacToe", "Creating new TicTacToe game.")
                ttt_game = tictactoe.TicTacToe()
                gm.add_game(gm.Game('TicTacToe', [None] * 2, ttt_game.board, ttt_game))
                game_id = len(gm.games)-1
                gm.get_game_by_id(len(gm.games)-1).players[0] = current_client # Should be able to safely assume that the last game in the list is the one we just created.
                gm.get_game_by_id(len(gm.games)-1).players[1] = clients[opponent] # Second player
                net.send_notif(clients[opponent].socket, f'{current_client.name} is attacking you in TicTacToe!')
                add_to_output_area("TicTacToe", "Game created.")
                add_to_output_area("TicTacToe", f'{current_client.name} joined game with id {len(gm.games)-1}.')
        
        queried_game = gm.get_game_by_id(game_id)
        if queried_game: # Game requested by ID exists
            if queried_game.name == 'TicTacToe' and len(queried_game.players) < queried_game.MAXPLAYERS:
                # Game is a TicTacToe game and has space for another player
                # Note that this means a player can accidentally join a game they're not supposed to
                # if they know the game ID. This is a security flaw. TODO fix this
                gm.add_player_to_game(game_id, current_client.name)
                add_to_output_area("TicTacToe", f'Player {current_client.name} joined game.')
                
                ttt_game = gm.get_game_by_id(game_id)

            elif queried_game.name == 'TicTacToe' and current_client.name in [player.name for player in queried_game.players]:
                # Player is already in the game. Let them rejoin and continue playing with the same game object.
                add_to_output_area("TicTacToe", f'Player rejoined game with ID {game_id}.')
                ttt_game = queried_game

            elif queried_game.name != 'TicTacToe':
                # Player tried to join a game that isn't TicTacToe
                add_to_output_area("TicTacToe", f"[{current_client.name}] Incorrect game name.")
                net.send_message(current_client.socket, "\nIncorrect game name. Please select another game.")
            elif len(queried_game.players) >= queried_game.MAXPLAYERS:
                # Game is full
                add_to_output_area("TicTacToe", f"[{current_client.name}] Game full.")
                net.send_message(current_client.socket, "\nGame is full. Please select another game.")
            else: # Edge case handling. Not strictly necessary or helpful, so remove in the future if it's not needed.
                add_to_output_area("TicTacToe", f"[{current_client.name}] Something else went wrong. Game not found.")
        else: 
            add_to_output_area("TicTacToe", f"[{current_client.name}] Game not found.")
    else: 
        pass
    
    # We should have a game object by now. If we don't, something went wrong.
    if cmds.split(',')[1] == 'move':
        if ttt_game == None: # We know the player is validly in a game, so we can get the game object
            ttt_game = gm.get_game_by_id(int(cmds.split(',')[2]))

        if type(ttt_game) == gm.Game:
            ttt_game_object = ttt_game.other_data # Get the actual *specific* game object from the Game object (in this case, the TicTacToe object)
        # Now check for moves
        if cmds.split(',')[1] == 'move':
            if (ttt_game_object.current_player == 'O' and current_client.name == ttt_game.players[0].name) \
            or (ttt_game_object.current_player == 'X' and current_client.name == ttt_game.players[1].name):
                net.send_message(current_client.socket, "It's not your turn!")
                return "It's not your turn!"
            ttt_game_object.place(int(cmds.split(',')[3].split('.')[0]), int(cmds.split(',')[3].split('.')[1]))
            if ttt_game_object.check_winner():
                net.send_message(current_client.socket, "You win!")
                gm.remove_game(ttt_game.id)
                return "You win!"
            elif ttt_game_object.is_full():
                net.send_message(current_client.socket, "It's a tie!")
                gm.remove_game(ttt_game.id)
                return "It's a tie!"
            else:
                ttt_game_object.current_player = 'O' if ttt_game_object.current_player == 'X' else 'X'
                if current_client.name == ttt_game.players[0].name:
                    net.send_notif(ttt_game.players[1].socket, f'TTT: {current_client.name} has made a move!')
                elif current_client.name == ttt_game.players[1].name:
                    net.send_notif(ttt_game.players[0].socket, f'TTT: {current_client.name} has made a move!')
        
        # Send the board to the player
    if ttt_game != None:
        net.send_message(current_client.socket, tictactoe.construct_board(ttt_game.board))