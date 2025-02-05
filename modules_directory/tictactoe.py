

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