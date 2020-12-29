import pygame as pg

def length2(vec2):
    return (vec2[0] * vec2[0] + vec2[1] * vec2[1])

def length(vec2):
    return length2(vec2) ** 0.5

def normalize(vec2):
    if length(vec2) == 0:
        return (0, 0)
    return (vec2[0] / length(vec2), vec2[1] / length(vec2))

class World:
    def __init__(self, map, players):
        self.map = map
        self.players = players
    
    def getPlayers(self):
        return self.players

    
    def tick(self):
        for player in self.players:
            player.tick()

class Player:
    def __init__(self, position, movementForce, actionForce):
        self.position = position
        self.speed = (0, 0)
        self.movementForce = movementForce
        self.actionForce = actionForce

    def applyForce(self, force):
        self.speed = (self.speed[0] + force[0], self.speed[1] + force[1])
    
    def moveUp(self):
        self.move((0, self.movementForce))
    def moveDown(self):
        self.move((0, -self.movementForce))
    def moveRight(self):
        self.move((self.movementForce, 0))
    def moveLeft(self):
        self.move((-self.movementForce, 0))

    def move(self, f):
        self.applyForce(f)

    def attractPlayers(self, world):
        p0 = self.position
        for player in world.getPlayers():
            p1 = player.getPosition()
            p = (p0[0] - p1[0], p0[1] - p1[1])
            l = length2(p)
            p = normalize(p)
            if l != 0:
                player.applyForce((self.actionForce * p[0] / l,
                                   self.actionForce * p[1] / l))

    def repelPlayers(self, world):
        p0 = self.position
        for player in world.getPlayers():
            p1 = player.getPosition()
            p = (p1[0] - p0[0], p1[1] - p0[1])
            l = length2(p)
            p = normalize(p)
            if l != 0:
                player.applyForce((self.actionForce * p[0] / l,
                                   self.actionForce * p[1] / l))

    def getPosition(self):
        return self.position

    def tick(self):
        p = self.position
        s = self.speed
        self.position = (p[0] + s[0], p[1] + s[1])

class Renderer:
    def __init__(self, size, world, textures):
        self.size = size
        self.world = world
        self.image = pg.Surface(size)
        self.textures = textures

    def render(self):
        self.image.fill((0, 0, 0))
        for player in self.world.getPlayers():
            pos = player.getPosition()
            pg.draw.rect(self.image, (200, 200, 100),
                         (pos[0], size[1] - pos[1], 10, 10))
        
    def getImage(self):
        return self.image

if __name__ == '__main__':
    pg.init()
    pg.display.set_caption("")
    size = width, height = 1920, 1080
    screen = pg.display.set_mode(size)

    running = True
    clock = pg.time.Clock()
    players = [
            Player((150, 150), 0.5, 1000.0),
            Player((300, 300), 0.5, 1000.0),
    ]
    world = World(1, players)
    renderer = Renderer(size, world, [])
    

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        if pg.key.get_pressed() != 0:
            if pg.key.get_pressed()[pg.K_w]:
                players[0].moveUp()
            if pg.key.get_pressed()[pg.K_s]:
                players[0].moveDown()
            if pg.key.get_pressed()[pg.K_a]:
                players[0].moveLeft()
            if pg.key.get_pressed()[pg.K_d]:
                players[0].moveRight()
            if pg.key.get_pressed()[pg.K_q]:
                players[0].attractPlayers(world)
            if pg.key.get_pressed()[pg.K_e]:
                players[0].repelPlayers(world)

            if pg.key.get_pressed()[pg.K_o]:
                players[1].moveUp()
            if pg.key.get_pressed()[pg.K_l]:
                players[1].moveDown()
            if pg.key.get_pressed()[pg.K_k]:
                players[1].moveLeft()
            if pg.key.get_pressed()[pg.K_SEMICOLON]:
                players[1].moveRight()
            if pg.key.get_pressed()[pg.K_i]:
                players[1].attractPlayers(world)
            if pg.key.get_pressed()[pg.K_p]:
                players[1].repelPlayers(world)


        screen.fill((0, 0, 0))
        renderer.render()
        screen.blit(renderer.getImage(), (0, 0))

        world.tick()
        pg.display.flip()
        clock.tick(30)
    pg.quit()
