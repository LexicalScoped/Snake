from enum import Enum

class SCREEN(Enum):
    MAIN = 0
    INFO =1
    MODE = 2
    PAUSE = 3
    END = 4
    GAME = 5
    
class MODE(Enum):
    EASY = 12
    MEDIUM = 20
    HARD = 30

class DIRECTIONS(Enum):
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4