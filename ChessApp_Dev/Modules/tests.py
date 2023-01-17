import chess
import chess.pgn

moves = ['e2e4','e7e6','d2d4','d7d5','e4e5','c7c5','c2c3','b8c6','g1f3','c8d7']

game = chess.pgn.Game()
game.headers['Event'] = 'example'

node = game.add_variation(chess.Move.from_uci(moves[0]))
i = 0
for move in moves:
    if i == 0: 
        i += 1 
        continue
    node = node.add_variation(chess.Move.from_uci(move))
    i += 1

print(game)