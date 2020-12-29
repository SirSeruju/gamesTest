import random
import pygame as pg
from math import pi, cos, sin, floor, atan2

class Player:
    def __init__(self, pos, m, visibleBlocks, spaceBlocks, speed, fov, rays, viewSteps):
        self.pos = pos
        self.map = m
        self.visibleBlocks = visibleBlocks
        self.spaceBlocks = spaceBlocks
        self.speed = speed
        self.direction = 0
        self.fov = fov
        self.rays = rays
        self.viewSteps = viewSteps
        self.shifted = False
        self.sc = (0, 1)

    def moveRight(self):
        s, c = sin(self.direction + pi / 2), cos(self.direction + pi / 2)
        self.move((c * self.speed, s * self.speed))

    def moveLeft(self):
        s, c = sin(self.direction - pi / 2), cos(self.direction - pi / 2)
        self.move((c * self.speed, s * self.speed))

    def moveDown(self):
        s, c = self.sc
        self.move((-c * self.speed, -s * self.speed))

    def moveUp(self):
        s, c = self.sc
        self.move((c * self.speed, s * self.speed))

    def shift(self):
        self.shifted = True
    
    def getRays(self):
        return self.rays

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
        self.direction = (self.direction + direction) % (2 * pi)
        self.sc = (sin(self.direction), cos(self.direction))

    def getDirection(self):
        return self.direction
    
    def getVisibleMap(self):
        m = self.map
        rays = self.rays
        visibleMap = [[False for i in range(len(m[0]))] for i in range(len(m))]
        for i in range(rays):
            angle = self.direction - self.fov / 2 + self.fov / rays * i
            dx = cos(angle)
            dy = sin(angle)
            x, y = self.pos[0] + 0.5, self.pos[1] + 0.5
            for k in range(self.viewSteps):
                if 0 < floor(x) < len(m[0]) and 0 < floor(y) < len(m):
                    visibleMap[floor(y)][floor(x)] = True
                    if m[floor(y)][floor(x)] not in self.visibleBlocks:
                        break
                    x += dx
                    y += dy
                else:
                    break
        return visibleMap

    def getVisibleSpace(self):
        m = self.map
        rays = self.rays
        visibleSpace = [self.viewSteps for i in range(rays)]
        for i in range(rays):
            angle = self.direction - self.fov / 2 + self.fov / rays * i
            dx = cos(angle)
            dy = sin(angle)
            x, y = self.pos[0] + 0.5, self.pos[1] + 0.5
            for k in range(self.viewSteps):
                if 0 < floor(x) < len(m[0]) and 0 < floor(y) < len(m):
                    if m[floor(y)][floor(x)] not in self.visibleBlocks:
                        visibleSpace[i] = k
                        break
                    x += dx
                    y += dy
                else:
                    break
        return visibleSpace

    def isCollide(self):
        m = self.map
        radius = len(m) / 2
        if 0 < floor(self.pos[0] + 0.5) < radius * 2 and 0 < floor(self.pos[1] + 0.5) < radius * 2 and\
           m[floor(self.pos[1] + 0.5)][floor(self.pos[0] + 0.5)] not in self.spaceBlocks:
            return True
        else:
            return False
    def getViewSteps(self):
        return self.viewSteps

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

class Map:
    def __init__(self, seed):
        random.seed(seed)
        self.radius = random.randint(100, 200)
        self.rule = random.choice(
            #[{"B": 4, "S": 3, "C": random.uniform(0, 1) / 2.3},
             [{"B": 5, "S": 4, "C": random.uniform(0, 1) / 1.4}]
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
        self.map = TorusField2D(m)
    
    def getMap(self):
        return self.map

class Planet:
    def __init__(self, pos):
        self.map = Map(pos[0] + pos[1])

    def getRadius(self):
        return self.map.radius

    def getMap(self):
        return self.map.getMap()

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


    def getImage(self):
        return self.image

    def renderMapImage(self):
        mImage = pg.Surface(size)
        mImage.fill((0, 0, 0))
        m = self.world.planet.getMap()
        r = self.world.planet.getRadius()
        visibleSpace = self.world.player.getVisibleSpace()
        playerPos = self.world.player.getPosition()
        colSize = self.size[0] / len(visibleSpace)
        viewSteps = self.world.player.getViewSteps()
        amplitude = self.size[1] / (2 * viewSteps)
        for col in range(len(visibleSpace)):
            pg.draw.rect(mImage, (100 / viewSteps * (viewSteps - visibleSpace[col]), 30 / viewSteps * (viewSteps - visibleSpace[col]), 0),
                         (colSize * col, amplitude * visibleSpace[col],
                             colSize, height - 2 * amplitude * visibleSpace[col]))

        self.mapImage = mImage


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption("")
    pg.mouse.set_visible(False)
    size = width, height = 1920, 1080
    screen = pg.display.set_mode(size)
    padding = 0
    planet = Planet((0, 0))
    player = Player((10, 10), planet.getMap(), [False], [False], 0.2, pi / 2, 64, 50)
    world = World(planet, player)
    running = True
    fps = 60
    clock = pg.time.Clock()
    renderer = Renderer(size, world, 30)
    #tileSize = (min(size) - 2 * padding) / (2 * world.planet.getRadius())
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEMOTION:
                pos = pg.mouse.get_pos()
                pos = (width / 2 - pos[0], height / 2 - pos[1])
                world.player.changeDirection(0.002 * -pos[0])
        pg.mouse.set_pos(width / 2, height / 2)


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
