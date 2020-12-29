from math import sin, floor, pi, cos
import pygame as pg
import sys
import os


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



if __name__ == '__main__':
    pg.init()
    pg.display.set_caption("")
    size = width, height = 300, 300
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

    while running:
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


        screen.fill((0, 0, 0))
        sprites.update()
        sprites.draw(screen)
        ship.image, ship.rect = rotateCenter(image, -player.getDirection() / pi * 180 - 90, 16, 16)
        ship.rect.x = player.position[0] - ship.rect.w / 2
        ship.rect.y = player.position[1] - ship.rect.h / 2

        player.tick()
        # pg.draw.rect(screen, (200, 200, 200), (*player.getPosition(), 10, 10), 1)
        pg.display.flip()
        clock.tick(30)
    pg.quit()






class World:
    def __init__(self):
        pass
    def getChunk(self, position):
        def noise1D(x):
            return (sin(x + 178283.58912) * 53758.5453123) % 1
        def noise2D(x, y):
            return (noise1D(x) + noise1D(y)) % 1
        planets = []
        for i in range(floor(noise2D(position[0], position[1]) * 6)):
            d = {
                "x": noise1D(i * 2007.0 * position[0]),
                "y": noise1D(i * 1994.9 * position[1]),
                "r": noise1D(i * 92.1 * (position[0] - position[1]))
            }
            planets.append(d)



