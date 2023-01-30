import os.path

def ReadScore():
    if os.path.isfile("score.txt"):
        file = open("score.txt", "r")
        HighScore = int(file.read())
        file.close()
        return HighScore
    else:
        return 0

def WriteScore(HighScore):
    file = open("score.txt", "w")
    file.write(str(HighScore))
    file.close()