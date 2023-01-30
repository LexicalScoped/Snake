import random
from config import CONFIG, COLORS

class Food:
    def __init__(self, Good):
        self.X = round(random.randrange(CONFIG["SIZE"],(CONFIG["X"] - (CONFIG["SIZE"] * 2)), CONFIG["SIZE"]), -1)
        self.Y = round(random.randrange(CONFIG["SIZE"],(CONFIG["Y"] - (CONFIG["SIZE"] * 2)), CONFIG["SIZE"]), -1)
        self.Good = Good
        if Good:
            self.Color = COLORS["FORESTGREEN"]
        else:
            self.Color = COLORS["RED"]