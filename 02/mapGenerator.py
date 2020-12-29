from math import sin, floor, pi, cos
import pygame as pg
import sys
import os
from random import uniform


def loadImage(name, colorkey=None):
    fullname = name
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    return image

def rotateCenter(image, angle, x, y):
    rotated_image = pg.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)
    return rotated_image, new_rect

class Ship:
    def __init__(self, position, momentAcceleration, momentRotation):
        self.position = position
        self.velocity = (0, 0)
        self.direction = 0
        self.mAcceleration = momentAcceleration
        self.mRotation = momentRotation

    def accelerateForward(self):
        self.velocity = (self.velocity[0] + cos(self.direction) * self.mAcceleration,
                         self.velocity[1] + sin(self.direction) * self.mAcceleration)

    def accelerateBackward(self):
        self.velocity = (self.velocity[0] - cos(self.direction) * self.mAcceleration,
                         self.velocity[1] - sin(self.direction) * self.mAcceleration)

    def getPosition(self):
        return self.position

    def getDirection(self):
        return self.direction

    def rotateRight(self):
        self.direction += self.mRotation
        self.direction = self.direction % (2 * pi)

    def rotateLeft(self):
        self.direction -= self.mRotation
        self.direction = self.direction % (2 * pi)

    def brake(self):
        brakeSpeed = (1 - 0.05)
        self.velocity = (self.velocity[0] * brakeSpeed, self.velocity[1] * brakeSpeed)
        if abs(self.velocity[0]) + abs(self.velocity[1]) < 0.1:
            self.velocity = (0, 0)

    def tick(self):
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])


def generateMap(size, birth, survive, chance, steps):
    m = [[uniform(0, 1) < chance for _ in range(size[0])] for _ in range(size[1])]
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
    radius = 32
    for row in range(size[1]):
        for col in range(size[0]):
            if not ((size[1] / 2 - row) ** 2 + (size[0] / 2 - col) ** 2 <= radius ** 2):
                m[row][col] = False
    return m



if __name__ == '__main__':
    pg.init()
    pg.display.set_caption("")
    size = width, height = 1000, 1000
    screen = pg.display.set_mode(size)

    running = True
    clock = pg.time.Clock()


    player = Ship((150, 150), 0.1, pi / 40)

    sprites = pg.sprite.Group()
    ship = pg.sprite.Sprite(sprites)
    image = loadImage("ship.png")
    image = pg.transform.scale(image, (32, 32))
    ship.image = image
    ship.rect = ship.image.get_rect()
    ship.rect.x = player.position[0] - ship.rect.w / 2
    ship.rect.y = player.position[1] - ship.rect.h / 2


    tileSize = 5
    size = 200
    m = generateMap((size, size), 4, 3, 0.3, 10)
    while running:
        preScreen = screen.copy()
        preScreen.set_alpha(254.99)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        if pg.key.get_pressed() != 0:
            if pg.key.get_pressed()[pg.K_w]:
                player.accelerateForward()
            if pg.key.get_pressed()[pg.K_s]:
                player.accelerateBackward()
            if pg.key.get_pressed()[pg.K_a]:
                player.rotateLeft()
            if pg.key.get_pressed()[pg.K_d]:
                player.rotateRight()
            if pg.key.get_pressed()[pg.K_SPACE]:
                player.brake()
            if pg.key.get_pressed()[pg.K_q]:
                player = Ship((150, 150), 0.1, pi / 30)

        screen.fill((0, 0, 0))
        screen.blit(preScreen, (0, 0))
        rays = 256
        maxDepth = 2
        for i in range(rays):
            angle = 2 * pi / rays * i
            dx = cos(angle) * tileSize
            dy = sin(angle) * tileSize
            x, y = player.position
            depth = 0
            for k in range(50):
                if m[floor(x / tileSize) % size][floor(y / tileSize) % size]:
                    pg.draw.rect(screen, (120, 60, 60), (floor(x / tileSize) * tileSize, floor(y / tileSize) * tileSize, tileSize, tileSize))
                    depth += 1
                    if depth >= maxDepth:
                        break
                else:
                    pg.draw.rect(screen, (10, 20, 10), (floor(x / tileSize) * tileSize, floor(y / tileSize) * tileSize, tileSize, tileSize))
                x += dx
                y += dy

        sprites.update()
        sprites.draw(screen)
        ship.image, ship.rect = rotateCenter(image, -player.getDirection() / pi * 180 - 90, 16, 16)
        ship.rect.x = player.position[0] - ship.rect.w / 2
        ship.rect.y = player.position[1] - ship.rect.h / 2

        player.tick()
        pg.display.flip()
        clock.tick(30)
    pg.quit()
