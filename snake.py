from config import CONFIG, COLORS
from controls import DIRECTIONS

class Snake:
    def __init__(self, Speed, Alive):
        self.X = CONFIG["X"] / 2
        self.Y = CONFIG["Y"] / 2
        self.Size = CONFIG["SIZE"]
        self.Color = COLORS["LIGHTBLUE"]
        self.Direction = DIRECTIONS.NONE
        self.Speed = int(Speed)
        self.Alive = Alive
        self.Length = 1
        self.Tail = []
    
    def Move(self):
        match self.Direction:
            case DIRECTIONS.UP:
                self.Y -= self.Size
            case DIRECTIONS.DOWN:
                self.Y += self.Size
            case DIRECTIONS.LEFT:
                self.X -= self.Size
            case DIRECTIONS.RIGHT:
                self.X += self.Size

class SnakeTail:
    def __init__(self, X, Y, COLOR):
        self.X = X
        self.Y = Y
        self.Color = COLOR
    
    def Move(self, X, Y):
        self.X = X
        self.Y = Y