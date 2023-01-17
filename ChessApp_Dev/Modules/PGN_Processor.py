import chess
import chess.pgn
import datetime

class Reader: 

    def __init__(self, moves: list,white:str,black:str):
        self.moves = moves
        self.game = chess.pgn.Game()
        
        self.game.headers['Event'] = 'Magachess 2.0'
        self.game.headers['Site'] = 'Gotsonburg Hamlet'
        self.game.headers['Date'] = str(datetime.datetime.today().strftime('%Y.%m.%d'))
        self.game.headers['Round'] = "69"
        self.game.headers['White'] = white
        self.game.headers['Black'] = black

    def get_pgn(self):

        # CONVERT ALGEBRAIC TO UCI
        for move in self.moves:
            if len(move) != 4 and len(move) != 5:
                print(move, len(move))
                i = 0
                while i < len(self.moves):
                    if self.moves[i] == move:
                        self.moves.pop(i)
                        i -= 1
                    i += 1


        node = self.game.add_variation(chess.Move.from_uci(self.moves[0]))
        i = 0
        for move in self.moves:
            if i == 0: 
                i += 1 
                continue
            node = node.add_variation(chess.Move.from_uci(move))
            i += 1
            
        fen = node.board().board_fen()
        fenboard = chess.Board()
        fenboard.set_board_fen(fen)
        self.game.headers['Result'] = str(fenboard.result())
        return str(self.game)

if __name__ == "__main__":
    moves = ['e2e4','e7e6','d2d4','d7d5','e4e5','c7c5','c2c3','b8c6','g1f3','c8d7']
    read = Reader(moves,'15','8')
    print(read.get_pgn())