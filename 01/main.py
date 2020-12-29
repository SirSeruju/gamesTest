import pygame as pg
import os

class TorusField1D:
    def __init__(self, field):
        self.field = field

    def __len__(self):
        return len(self.field)

    def __getitem__(self, key):
        return self.field[key % len(self.field)]

    def __setitem__(self, key, value):
        self.field[key % len(self.field)] = value

    def getField(self):
        return self.field
    
class TorusField2D:
    def __init__(self, field):
        self.field = list(map(lambda x: TorusField1D(x), field))

    def __len__(self):
        return len(self.field)

    def __getitem__(self, key):
        return self.field[key % len(self.field)]

    def __setitem__(self, key, value):
        self.field[key % len(self.field)] = value

    def getField(self):
        return list(map(lambda x: x.getField(), self.field))
    

class Game:
    def __init__(self, size):
        self.size = size
        self.field = TorusField2D([[0 for i in range(size[0])] for i in range(size[1])])
        self.newField = TorusField2D([[0 for i in range(size[0])] for i in range(size[1])])
        self.cell = 0

        for row in range(size[1] - 1):
            #self.field[row][10] = 1
            self.field[row][0] = 2
            self.field[row][-1] = 2

        for col in range(size[0]):
            self.field[1][col] = 2
        #self.field[5][10] = 1
        self.field[8][10] = 1

    def Rule(self, pos):
        x, y = pos
        if self.field[y][x] == 1:
            if self.field[y - 1][x] == 0:
                return 0
            elif self.field[y + 1][x] == 3 or self.field[y + 2][x] == 3:
                return 0
            else:
                return 1
        elif self.field[y][x] == 0:
            if self.cell != 0 and abs(self.mousePos[1] - y) + abs(self.mousePos[0] - x) <= 3:
                return self.cell
            elif self.field[y + 1][x] == 1:
                return 1
            else:
                return 0
        elif self.field[y][x] == 2:
            return 2
        elif self.field[y][x] == 3:
            return 0

    def nextStep(self):
        for row in range(len(self.field)):
            for col in range(len(self.field[0])):
                self.newField[row][col] = self.Rule((col, row))
        self.cell = 0
        temp = self.field
        self.field = self.newField
        self.newField = temp

    def getField(self):
        return self.field.getField()

    def getSize(self):
        return self.size
    
    def addCells(self, pos, cell):
        self.mousePos = pos
        self.cell = cell
        


class PygameGame:
    def __init__(self, screenSize, fieldSize, cellSize, title, fps):
        pg.init()
        self.screenSize = screenSize
        self.fieldSize = fieldSize
        pg.display.set_caption(title)
        self.screen = pg.display.set_mode(screenSize)
        self.clock = pg.time.Clock()
        self.game = Game(fieldSize)
        self.cellSize = cellSize
        self.fps = fps
        self.colors = {
            0: (0, 0, 0),
            1: (200, 200, 100),
            2: (100, 100, 100),
            3: (200, 100, 100)
        }
        self.mainLoop()
    
    def mainLoop(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = self.getCell(event.pos)
                        if pos is not None:
                            self.game.addCells(pos, 1)
                    if event.button == 3:
                        pos = self.getCell(event.pos)
                        if pos is not None:
                            self.game.addCells(pos, 3)
            self.screen.fill((0, 0, 0))
            self.render()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.game.nextStep()
            self.clock.tick(self.fps)

    def render(self):
        for row in range(self.game.getSize()[1]):
            for col in range(self.game.getSize()[0]):
                pg.draw.rect(self.screen, self.colors[self.game.getField()[row][col]],
                             ((col * self.cellSize,
                              (self.game.getSize()[1] - row) * self.cellSize,
                              self.cellSize, self.cellSize)))

    def getCell(self, mousePos):
        for row in range(self.fieldSize[1]):
            for col in range(self.fieldSize[0]):
                if 0 < mousePos[0] - col * self.cellSize < self.cellSize and\
                   0 < mousePos[1] - row * self.cellSize < self.cellSize:
                    return (col, self.game.getSize()[1] - row)
        return None


    def exit(self):
        pg.quit()
        exit()


if __name__ == '__main__':
    screenSize = (600, 600)
    fieldSize = (100, 100)
    title = "Game"
    fps = 60
    cellSize = 6
    PygameGame(screenSize, fieldSize, cellSize, title, fps)
