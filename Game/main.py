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
    "hotel" : pg.transform.scale(pg.image.load("img/hotel.png"), (80, 80)),
    "passenger" : pg.image.load("img/passenger.png"),
    "taxi_bg" : pg.transform.scale(pg.image.load("img/taxi_background.png"), (32, 32)),
    "parking" : pg.transform.scale(pg.image.load("img/parking.png"), (32, 32))
}


class Player:
    def __init__(self, x, y):
        self.view = "rear"
        self.image = image_dict["player"][self.view]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_direction = 0
        self.y_direction = 0
        self.speed = 2

    def update(self):
        self.image = image_dict["player"][self.view]
        self.rect.x += self.speed * self.x_direction
        self.rect.y += self.speed * self.y_direction

    def is_crashed(self):
        for x in range(self.rect.left, self.rect.right, 1):
            for y in range(self.rect.top, self.rect.bottom, 1):
                try:
                    if sc.get_at((x, y)) in ((220, 215, 177, 255),
                                             (202, 206, 157, 255),
                                             (212, 207, 174, 255),
                                             (216, 211, 175, 255),
                                             (150, 140, 119, 255),
                                             (188, 184, 157, 255)):
                        return True
                except IndexError:
                    return True

        if hotel.rect.colliderect(self.rect):
            return True

        return False


class Hotel:
    def __init__(self, x = None, y = None):
        self.image = image_dict["hotel"]
        self.rect = self.image.get_rect()
        self.positions = (
            (57, -4),
            (563, -4),
            (57, 260),
            (438, 260)
        )
        if x is None and y is None:
            self.rect.topleft = choice(self.positions)
        elif x is not None and y is not None:
            self.rect.topleft = (x, y)
        else:
            raise ValueError("One coordinate is known but the other one is not!")


class Parking:
    def __init__(self, my_hotel: Hotel):
        self.image = image_dict["parking"]
        self.rect = self.image.get_rect()
        self.rect.centerx = my_hotel.rect.centerx
        self.rect.y = my_hotel.rect.y + my_hotel.image.get_height()


class Passenger:
    def __init__(self, my_hotel: Hotel, my_player: Player):
        self.image = image_dict["passenger"]
        self.rect = self.image.get_rect()
        self.starting_position = (my_hotel.rect.x, my_hotel.rect.y + my_hotel.image.get_height())
        self.is_collected = False
        self.player = my_player

    def update(self):
        if self.rect.colliderect(self.player.rect):
            self.is_collected = False
        if self.is_collected:
            self.rect.topleft = self.player.rect.topleft
        else:
            self.rect.topleft = self.starting_position

player = Player(300, 300)
hotel = Hotel()
parking = Parking(hotel)
passenger = Passenger(hotel, player)

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
            # if event.key == pg.K_s:
            #     print(pg.mouse.get_pos())
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
        if event.type == pg.MOUSEBUTTONDOWN:
            print(f"{pg.mouse.get_pos()}: {sc.get_at(pg.mouse.get_pos())}")

    keys_pressed = pg.key.get_pressed()

    if keys_pressed[pg.K_UP]:
        player.y_direction = -1
        player.view = "rear"
    elif keys_pressed[pg.K_DOWN]:
        player.y_direction = 1
        player.view = "front"
    else:
        player.y_direction = 0
    if keys_pressed[pg.K_RIGHT]:
        player.x_direction = 1
        player.view = "right"
    elif keys_pressed[pg.K_LEFT]:
        player.x_direction = -1
        player.view = "left"
    else:
        player.x_direction = 0

    # sc.fill(WHITE)
    sc.blit(pg.transform.scale(image_dict["bg"], (w, h)), (0, 0))

    player.update()

    if player.is_crashed():
        player.rect.topleft = (300, 300)
        passenger.is_collected = False

    sc.blit(parking.image, parking.rect)

    sc.blit(player.image, player.rect)

    sc.blit(hotel.image, hotel.rect)

    sc.blit(passenger.image, passenger.rect)

    pg.display.flip()

pg.quit()
