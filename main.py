import pygame
import sys
from controls import SCREEN, MODE, DIRECTIONS
from menus import Main, Info, Mode, Pause, End
from config import CONFIG, COLORS
from snake import Snake, SnakeTail
from food import Food
from score import ReadScore, WriteScore

pygame.init()

class Window:
    def __init__(self):
        self.Display = pygame.display.set_mode([CONFIG["X"], CONFIG["Y"]])
        pygame.display.set_caption(CONFIG["TITLE"])
        self.Font = pygame.font.SysFont("microsoftsansserif", 25)
        self.FontColor = COLORS["GRAY"]
        self.Background = COLORS["MIDNIGHTBLUE"]
        self.Screen = SCREEN.MAIN
        self.Mode = MODE.EASY
        self.Size = CONFIG["SIZE"]
        self.Snake = Snake(MODE.EASY.value, False)
        self.FoodCount = 1
        self.Food = []
        self.BadFoodCount = 0
        self.BadFood = []
        self.Score = 0
        self.HighScore = ReadScore()
    
    def ChangeScreen(self, Screen):
        self.Screen = Screen
    
    def ChangeMode(self, Mode):
        self.Mode = Mode
    
    def DrawScreen(self):
        if self.Screen == SCREEN.GAME:
            self.DrawGame()
        else:
            self.DrawMenu()
    
    def DrawMenu(self):
        self.Display.fill(self.Background)
        Y_POSITION = 30
        Menu = []
        FontColor = self.FontColor
        match self.Screen:
            case SCREEN.MAIN:
                Menu = Main
            case SCREEN.INFO:
                Menu = Info
            case SCREEN.MODE:
                Menu = Mode
            case SCREEN.PAUSE:
                Menu = Pause
            case SCREEN.END:
                Menu = End
                FontColor = COLORS["RED"]
        for Line in Menu:
            Text = self.Font.render(Line, True, FontColor)
            self.Display.blit(Text, [30, Y_POSITION])
            Y_POSITION += 30
        if self.Screen == SCREEN.PAUSE or self.Screen == SCREEN.END:
            self.DrawCurrentScore(FontColor, Y_POSITION)
            Y_POSITION += 30
            self.DrawRecordScore(FontColor, Y_POSITION)
        if self.Screen == SCREEN.MAIN:
            self.DrawRecordScore(FontColor, Y_POSITION)
        pygame.display.update()

    def DrawCurrentScore(self, FontColor, Y_POSITION = 0):
        ScoreString = ""
        BlitLocation = []
        if self.Screen == SCREEN.GAME:
            ScoreString = str(self.Score)
            BlitLocation = [20, 20]
        else:
            ScoreString = "Score: " + str(self.Score)
            BlitLocation = [30, Y_POSITION]
        Score = self.Font.render(ScoreString, True, FontColor)
        self.Display.blit(Score, BlitLocation)
    
    def DrawRecordScore(self, FontColor, Y_POSITION = 0):
        HighScore = self.Font.render("HighScore: " + str(self.HighScore), True, FontColor)
        self.Display.blit(HighScore, [30, Y_POSITION])

    def DrawGame(self):
        self.Display.fill(self.Background)
        self.DrawCurrentScore(self.FontColor)
        self.Snake.Tail.append(SnakeTail(self.Snake.X, self.Snake.Y, self.Snake.Color))
        if len(self.Snake.Tail) > self.Snake.Length:
            del self.Snake.Tail[0]
        pygame.draw.rect(self.Display, self.Snake.Color, [ self.Snake.X, self.Snake.Y, self.Size, self.Size ])
        for block in self.Snake.Tail + self.Food + self.BadFood:
            pygame.draw.rect(self.Display, block.Color, [ block.X, block.Y, self.Size, self.Size ])
        if self.Score > self.HighScore:
            self.HighScore = self.Score
        pygame.display.update()
        self.CheckCollision()
        self.CheckFood()
        self.CheckLevel()
    
    def CheckCollision(self):
        self.Snake.Move()
        if self.Snake.Alive and self.Snake.Direction != DIRECTIONS.NONE:
            if (self.Snake.X < 0
            or self.Snake.X >= CONFIG["X"]
            or self.Snake.Y < 0
            or self.Snake.Y >= CONFIG["Y"]):
                self.SnakeDied()
            for block in self.Snake.Tail + self.BadFood:
                if [self.Snake.X, self.Snake.Y] == [block.X, block.Y]:
                    self.SnakeDied()

    def SnakeDied(self):
        self.Snake.Alive = False
        self.ChangeScreen(SCREEN.END)       

    def CheckFood(self):
        for food in self.Food:
            if (food.X == self.Snake.X
            and food.Y == self.Snake.Y):
                self.Snake.Length += 1
                self.Score += int(self.Mode.value / 2)
                self.Food.remove(food)
                del food
        if len(self.Food) < self.FoodCount:
            self.Food.append(self.GenFood(True))
        if len(self.BadFood) < self.BadFoodCount:
            self.BadFood.append(self.GenFood(False))
    
    def GenFood(self, Good):
        food = Food(Good)
        regen = False
        for block in self.Snake.Tail:
            if [food.X, food.Y] == [block.X, block.Y]:
                regen = True
        if regen:
            return self.GenFood(Good)
        else:
            return food


    def CheckLevel(self):
        if self.Score >= 50:
            self.FoodCount = 2
        if self.Score >= 100:
            self.Snake.Speed = int(self.Mode.value) + 2
        if self.Score >=  250:
            self.FoodCount = 3
        if self.Score >= 400:
            self.BadFoodCount = 1
        if self.Score >= 600:
            self.Snake.Speed = int(self.Mode.value) + 4
        if self.Score >= 800:
            self.BadFoodCount = 2
        if self.Score >= 1000:
            self.Snake.Speed = int(self.Mode.value) + 6

    def Reset(self):
        self.Snake.Alive = False
        self.FoodCount = 1
        self.BadFoodCount = 0
        self.Score = 0
        self.ClearFood(self.Food)
        self.ClearFood(self.BadFood)

    def ClearFood(self, foodlist):
        for food in foodlist:
            foodlist.remove(food)
            del food

    def Quit(self):
        WriteScore(self.HighScore)
        pygame.quit()
        sys.exit()

def main():
    Game = Window()
    clock = pygame.time.Clock()

    while True:
        Game.DrawScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.Quit()
            if event.type == pygame.KEYDOWN:
                if Game.Screen == SCREEN.MAIN:
                    if event.key == pygame.K_q:
                        Game.Quit()
                    if event.key == pygame.K_i:
                        Game.ChangeScreen(SCREEN.INFO)
                    if event.key == pygame.K_n:
                        Game.Reset()
                        Game.ChangeScreen(SCREEN.MODE)
                if Game.Screen == SCREEN.INFO:
                    if event.key == pygame.K_q:
                        Game.Quit()
                    if event.key == pygame.K_b:
                        Game.ChangeScreen(SCREEN.MAIN)
                if Game.Screen == SCREEN.MODE:
                    if event.key == pygame.K_q:
                        Game.Quit()
                    if event.key == pygame.K_b:
                        Game.ChangeScreen(SCREEN.MAIN)
                    if event.key == pygame.K_1:
                        Game.Snake = Snake(MODE.EASY.value, True)
                        Game.ChangeMode(MODE.EASY)
                        Game.ChangeScreen(SCREEN.GAME)
                    if event.key == pygame.K_2:
                        Game.Snake = Snake(MODE.MEDIUM.value, True)
                        Game.ChangeMode(MODE.MEDIUM)
                        Game.ChangeScreen(SCREEN.GAME)
                    if event.key == pygame.K_3:
                        Game.Snake = Snake(MODE.HARD.value, True)
                        Game.ChangeMode(MODE.HARD)
                        Game.ChangeScreen(SCREEN.GAME)
                if Game.Screen == SCREEN.GAME:
                    if event.key == pygame.K_p:
                        Game.ChangeScreen(SCREEN.PAUSE)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if Game.Snake.Direction != DIRECTIONS.DOWN:
                            Game.Snake.Direction = DIRECTIONS.UP
                            break
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if  Game.Snake.Direction != DIRECTIONS.UP:
                            Game.Snake.Direction = DIRECTIONS.DOWN
                            break
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a: 
                        if Game.Snake.Direction != DIRECTIONS.RIGHT:
                            Game.Snake.Direction = DIRECTIONS.LEFT
                            break
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d: 
                        if Game.Snake.Direction != DIRECTIONS.LEFT:
                            Game.Snake.Direction = DIRECTIONS.RIGHT
                            break
                if Game.Screen == SCREEN.PAUSE:
                    if event.key == pygame.K_r:
                        Game.ChangeScreen(SCREEN.GAME)
                    if event.key == pygame.K_m:
                        Game.ChangeScreen(SCREEN.MAIN)
                    if event.key == pygame.K_q:
                        Game.Quit()
                if Game.Screen == SCREEN.END:
                    if event.key == pygame.K_q:
                        Game.Quit()
                    if event.key == pygame.K_n:
                        Game.Reset()
                        Game.ChangeScreen(SCREEN.MODE)
                    if event.key == pygame.K_m:
                        Game.ChangeScreen(SCREEN.MAIN)
        clock.tick(Game.Snake.Speed)

if __name__ == "__main__":
    main()