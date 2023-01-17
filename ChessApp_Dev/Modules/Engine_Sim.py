from importlib.util import find_spec
from re import S
from select import select
from stockfish.models import Stockfish as sf

class EngineSim:
    """Creates an object with args version: int, boardstate: list and 
    depth: int"""
    def __init__(self,version: int,boardstate: list, depth: int) -> None:
        """version, boardstate, depth"""
        if version == 8:
            self.engine = sf(path="../Engines\SF\SF_8\stockfish-8-win\stockfish-8-win\Windows\stockfish_8_x64.exe")
        if version == 15:
            self.engine = sf(path="../Engines\SF\SF_15\stockfish_15_win_x64_avx2\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")
        else: 
            self.engine = sf(path="../Engines\SF\SF_15\stockfish_15_win_x64_avx2\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")
        
        self.depth = depth
        self.engine.set_depth(depth)

        self.boardstate = boardstate
        self.engine.set_position(boardstate)

    def setdepth(self, depth: int):
        self.depth = depth

    def getboardlist(self):
        return self.boardstate.split(" ")

    def setboard(self, boardstate: list):
        self.boardstate = boardstate
        self.engine.set_position(boardstate)
        print(f"Board -> {self.boardstate}")

    def addmoves(self,moves: list):
        if len(moves) < 2:
            print("moved:",moves[0])
            self.boardstate.append(moves[0])
            self.engine.set_position(self.boardstate)
        else:
            for move, i in moves, enumerate:
                print(f"move {i}: {move}")
                self.boardstate.append(move)
                self.engine.set_position(self.boardstate)
                print(f"board: {self.boardstate}")

    def calculate_move(self):
        print(f"calculating for move at depth {self.depth}...")
        return self.engine.get_best_move()

