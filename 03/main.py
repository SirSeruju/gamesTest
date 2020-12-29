import random
import pygame as pg
from math import pi, cos, sin, floor, atan2

class Player:
    def __init__(self, pos, m, visibleBlocks, spaceBlocks, speed, fov):
        self.pos = pos
        self.map = m
        self.visibleBlocks = visibleBlocks
        self.spaceBlocks = spaceBlocks
        self.speed = speed
        self.direction = 0
        self.fov = fov
        self.shifted = False

    def moveRight(self):
        self.move((self.speed, 0))

    def moveLeft(self):
        self.move((-self.speed, 0))

    def moveDown(self):
        self.move((0, self.speed))

    def moveUp(self):
        self.move((0, -self.speed))

    def shift(self):
        self.shifted = True

    def move(self, d):
        for _ in range(2 if self.shifted else 1):
            pos = self.pos
            self.pos = (self.pos[0] + d[0], self.pos[1] + d[1])
            if self.isCollide():
                self.pos = pos
        self.shifted = False

    def getPosition(self):
        return self.pos

    def changeDirection(self, direction):
        self.direction = direction % (2 * pi)

    def getDirection(self):
        return self.direction
    
    def getVisibleMap(self):
        m = self.map
        rays = 300
        visibleMap = [[False for i in range(len(m[0]))] for i in range(len(m))]
        for i in range(rays):
            angle = self.direction - self.fov / 2 + self.fov / rays * i
            dx = cos(angle)
            dy = sin(angle)
            x, y = self.pos[0] + 0.5, self.pos[1] + 0.5
            for k in range(40):
                if 0 < floor(x) < len(m[0]) and 0 < floor(y) < len(m):
                    visibleMap[floor(y)][floor(x)] = True
                    if m[floor(y)][floor(x)] not in self.visibleBlocks:
                        break
                    x += dx
                    y += dy
                else:
                    break
        return visibleMap

    def isCollide(self):
        m = self.map
        radius = len(m) / 2
        if 0 < floor(self.pos[0]) < radius * 2 and 0 < floor(self.pos[1]) < radius * 2 and\
           m[floor(self.pos[1])][floor(self.pos[0])] not in self.spaceBlocks:
            return True
        elif 0 < floor(self.pos[0] + 1) < radius * 2 and 0 < floor(self.pos[1]) < radius * 2 and\
           m[floor(self.pos[1])][floor(self.pos[0] + 1)] not in self.spaceBlocks:
            return True
        elif 0 < floor(self.pos[0]) < radius * 2 and 0 < floor(self.pos[1] + 1) < radius * 2 and\
           m[floor(self.pos[1] + 1)][floor(self.pos[0])] not in self.spaceBlocks:
            return True
        elif 0 < floor(self.pos[0] + 1) < radius * 2 and 0 < floor(self.pos[1] + 1) < radius * 2 and\
           m[floor(self.pos[1] + 1)][floor(self.pos[0] + 1)] not in self.spaceBlocks:
            return True
        else:
            return False

class Bullet:
    def __init__(self, m, pos, direction, spaceBlocks):
        self.pos = pos
        self.direction = direction
        self.map = m
        self.sc = (sin(self.direction), cos(self.direction))
    
    def tick(self):
        s, c = self.sc
        if self.isCollide():
            self.map[floor(self.pos[0])][floor(self.pos[1])] = choice(spaceBlock)
        self.pos = (self.pos[0] + c, self.pos[1] + s)

    def isCollide(self):
        m = self.map
        radius = len(m) / 2
        if 0 < floor(self.pos[0]) < radius * 2 and 0 < floor(self.pos[1]) < radius * 2 and\
           m[floor(self.pos[1])][floor(self.pos[0])] not in self.spaceBlocks:
            return True
        else:
            return False


class Planet:
    def __init__(self, pos):
        random.seed(pos[0] * 3 + pos[1] * pos[1] - 12)
        self.radius = random.randint(100, 200)
        self.rule = random.choice(
            [{"B": 4, "S": 3, "C": random.uniform(0, 1) / 3.3},
             {"B": 5, "S": 4, "C": random.uniform(0, 1) / 1.1}]
        )
        self.steps = random.randint(5, 20)
        self.generateMap()
    
    def generateMap(self):
        birth = self.rule["B"]
        survive = self.rule["S"]
        chance = self.rule["C"]
        steps = self.steps
        radius = self.radius
        size = (radius * 2, radius * 2)
        m = [[random.uniform(0, 1) < chance for _ in range(size[0])] for _ in range(size[1])]
        def step(m, size, birth, survive):
            m1 = [[False for _ in range(size[0])] for _ in range(size[1])]
            for row in range(size[1]):
                for col in range(size[0]):
                    c = 0
                    for i in range(-1, 2):
                        for k in range(-1, 2):
                            if i == 0 and k == 0:
                                continue
                            if m[(row + i) % size[1]][(col + k) % size[0]]:
                                c += 1
                    if m[row % size[1]][col % size[0]]:
                        if c < survive:
                            m1[row % size[1]][col % size[0]] = False
                        else:
                            m1[row % size[1]][col % size[0]] = True
                    else:
                        if c < birth:
                            m1[row % size[1]][col % size[0]] = False
                        else:
                            m1[row % size[1]][col % size[0]] = True
            return m1
        for i in range(steps):
            m = step(m, size, birth, survive)
        for row in range(size[1]):
            for col in range(size[0]):
                if not ((size[1] / 2 - row) ** 2 + (size[0] / 2 - col) ** 2 <= radius ** 2):
                    m[row][col] = False
        self.map = m

    def getRadius(self):
        return self.radius

    def getMap(self):
        return self.map

class World:
    def __init__(self, planet, player):
        self.planet = planet
        self.player = player
    def tick(self):
        centre = self.planet.getRadius() / 2

    def getPlayer(self):
        return self.player

    def getPlanet(self):
        return self.planet

    def getVisibleMap(self):
        return self.player.getVisibleMap()


class Renderer:
    def __init__(self, size, world, tileSize):
        self.image = pg.Surface(size)
        self.size = size
        self.world = world
        self.tileSize = tileSize

    def renderImage(self):
        self.image.fill((0, 0, 0))
        self.renderMapImage()
        playerPos = self.world.player.getPosition()

        self.image.blit(self.mapImage, (0, 0))

        pg.draw.rect(self.image, (200, 200, 100), (self.size[0] / 2, self.size[1] / 2, tileSize, tileSize))


    def getImage(self):
        return self.image

    def renderMapImage(self):
        mImage = pg.Surface(size)
        mImage.fill((0, 0, 0))
        tileSize = self.tileSize
        m = self.world.planet.getMap()
        r = self.world.planet.getRadius()
        visibleMap = self.world.getVisibleMap()
        playerPos = self.world.player.getPosition()
        for row in range(r * 2):
            for col in range(r * 2):
                if visibleMap[row][col]:
                    if m[row][col]:
                        pg.draw.rect(mImage, (120, 60, 60),
                                     (self.size[0] / 2 + (col - playerPos[0]) * tileSize,
                                      self.size[1] / 2 + (row - playerPos[1]) * tileSize, tileSize, tileSize))
                    else:
                        pg.draw.rect(mImage, (10, 20, 10),
                                     (self.size[0] / 2 + (col - playerPos[0]) * tileSize,
                                      self.size[1] / 2 + (row - playerPos[1]) * tileSize, tileSize, tileSize))
        self.mapImage = mImage


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption("")
    size = width, height = 1920, 1080
    screen = pg.display.set_mode(size)
    padding = 0
    planet = Planet((0, 0))
    player = Player((10, 10), planet.getMap(), [False], [False], 0.2, 2)
    world = World(planet, player)
    running = True
    fps = 60
    clock = pg.time.Clock()
    renderer = Renderer(size, world, 30)
    #tileSize = (min(size) - 2 * padding) / (2 * world.planet.getRadius())
    tileSize = 30
    fov = 20
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEMOTION:
                a = atan2((event.pos[1] - height / 2), (event.pos[0] - width / 2))
                world.player.changeDirection(a)

        if pg.key.get_pressed() != 0:
            if pg.key.get_pressed()[pg.K_LSHIFT]:
                world.player.shift()
            if pg.key.get_pressed()[pg.K_a]:
                world.player.moveLeft()
            if pg.key.get_pressed()[pg.K_d]:
                world.player.moveRight()
            if pg.key.get_pressed()[pg.K_s]:
                world.player.moveDown()
            if pg.key.get_pressed()[pg.K_w]:
                world.player.moveUp()

        renderer.renderImage()

        screen.fill((0, 0, 0))
        screen.blit(renderer.getImage(), (0, 0))

        world.tick()
        pg.display.flip()
        clock.tick(fps)
    pg.quit()
