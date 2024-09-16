import screenspace as ss
import style as s

class PlayerModules():

    # Calculator is fixed on remote

    # Deed is better implemented in monopoly.py
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