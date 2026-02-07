import pygame as pg
from random import choice

w, h = 700, 450
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 30

image_dict = {
    "bg" : pg.image.load("img/Background.png"),
    "player" : {
        "front" : pg.image.load("img/cab_front.png"),
        "left" : pg.image.load("img/cab_left.png"),
        "rear" : pg.image.load("img/cab_rear.png"),
        "right" : pg.image.load("img/cab_right.png"),
    },
    "hole" : pg.image.load("img/hole.png"),
    "hotel" : pg.image.load("img/hotel.png"),
    "passenger" : pg.image.load("img/passenger.png"),
    "taxi_bg" : pg.image.load("img/taxi_background.png")
}


class Player:
    def __init__(self, x, y):
        self.view = "rear"
        self.image = image_dict["player"][self.view]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.x_direction = 0
        self.y_direction = 0
        self.speed = 1

    def update(self):
        self.image = image_dict["player"][self.view]
        self.rect.x += self.speed * self.x_direction
        self.rect.y += self.speed * self.y_direction


class Hotel:
    def __init__(self, x = None, y = None):
        self.image = image_dict["hotel"]
        self.rect = self.image.get_rect()
        self.positions = (
            (75, 40),
            (75, 300)
        )
        print(choice(self.positions))
        if x is None and y is None:
            self.rect.topleft = choice(self.positions)
        elif x is not None and y is not None:
            self.rect.topleft = (x, y)
        else:
            raise ValueError("One coordinate is known but the other one is not!")

player = Player(0, 0)
hotel = Hotel()

pg.init()

sc = pg.display.set_mode((w, h))
clock = pg.time.Clock()
running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            ...
            # if event.key == pg.K_RIGHT:
            #     player.x_direction += 1
            #     player.view = "right"
            # elif event.key == pg.K_LEFT:
            #     player.x_direction += -1
            #     player.view = "left"
            # if event.key == pg.K_UP:
            #     player.y_direction += -1
            #     player.view = "rear"
            # elif event.key == pg.K_DOWN:
            #     player.y_direction += 1
            #     player.view = "front"

    keys_pressed = pg.key.get_pressed()

    if keys_pressed[pg.K_RIGHT]:
        player.x_direction = 1
        player.view = "right"
    elif keys_pressed[pg.K_LEFT]:
        player.x_direction = -1
        player.view = "left"
    else:
        player.x_direction = 0
    if keys_pressed[pg.K_UP]:
        player.y_direction = -1
        player.view = "rear"
    elif keys_pressed[pg.K_DOWN]:
        player.y_direction = 1
        player.view = "front"
    else:
        player.y_direction = 0

    # sc.fill(WHITE)
    sc.blit(pg.transform.scale(image_dict["bg"], (w, h)), (0, 0))

    player.update()
    sc.blit(player.image, player.rect)

    sc.blit(hotel.image, hotel.rect)

    pg.display.flip()

pg.quit()
