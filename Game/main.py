import pygame as pg
from random import choice

w, h = 700, 450
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 30

image_dict = {
    "bg" : pg.image.load("img/Background.png"),
    "empty_bg" : pg.image.load("img/empty_background.png"),
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
    "parking" : pg.transform.scale(pg.image.load("img/parking.png"), (48, 48)),
    "obstacle" : {
        "small" : pg.image.load("img/small_barrier.png"),
        "tall" : pg.image.load("img/tall_barrier.png"),
        "long" : pg.image.load("img/long_barrier.png")
    }
}


class Obstacle:
    def __init__(self, x: float, y: float, size: str):
        if size not in ("long", "tall", "small"):
            raise ValueError("An obstacle's size can only be 'small', 'tall', or 'long'")
        self.image = image_dict["obstacle"][size]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Player:
    def __init__(self, x, y):
        self.view = "rear"
        self.image = image_dict["player"][self.view]
        self.rect = self.image.get_rect()
        self.starting_position = (x, y)
        self.rect.topleft = self.starting_position
        self.x_direction = 0
        self.y_direction = 0
        self.speed = 5

    def update(self):
        self.image = image_dict["player"][self.view]
        self.rect.x += self.speed * self.x_direction
        self.rect.y += self.speed * self.y_direction

    def is_crashed(self):
        if self.rect.collidelist(obstacles) != -1 or\
                hotel.rect.colliderect(self.rect) or\
                self.rect.left < 0 or self.rect.right > w or self.rect.top < 0 or self.rect.bottom > h:
            return True
        return False


class Hotel:
    def __init__(self, x = None, y = None):
        self.image = image_dict["hotel"]
        self.rect = self.image.get_rect()
        self.positions = (
            (57, -4),
            (563, -4),
            (438, 260),
            (57, 260)
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
    def __init__(self, my_hotel: Hotel, my_player: Player, my_parking: Parking):
        self.image = image_dict["passenger"]
        self.rect = self.image.get_rect()
        self.positions = ((70, 130), (575, 140), (450, 400), (70, 400))
        self.starting_position = choice(self.positions)
        while self.positions.index(self.starting_position) == my_hotel.positions.index(my_hotel.rect.topleft):
            self.starting_position = choice(self.positions)
        self.is_collected = False
        self.is_parked = False
        self.player = my_player
        self.parking = my_parking

    def update(self):
        if self.parking.rect.contains(self.rect):
            self.is_parked = True
        elif self.rect.colliderect(self.player.rect):
            self.is_collected = True
        if self.is_parked:
            self.rect.center = self.parking.rect.center
        elif self.is_collected:
            self.rect.topleft = self.player.rect.topleft
        else:
            self.rect.bottomleft = self.starting_position

player: Player = Player(300, 190)
hotel: Hotel = Hotel()
parking: Parking = Parking(hotel)
passenger: Passenger = Passenger(hotel, player, parking)

obstacles: list[Obstacle] = []
long_obstacle1 = Obstacle(65, 14, "long")
long_obstacle2 = Obstacle(65, 415, "long")
tall_obstacle1 = Obstacle(12, 67, "tall")
tall_obstacle2 = Obstacle(645, 67, "tall")
small_obstacle1 = Obstacle(265, 67, "small")
small_obstacle2 = Obstacle(139, 261, "small")
small_obstacle3 = Obstacle(392, 261, "small")
obstacles.extend((long_obstacle1, long_obstacle2, tall_obstacle1, tall_obstacle2, small_obstacle1, small_obstacle2, small_obstacle3))

def win_message(x: float | None, y: float | None, screen: pg.SurfaceType, my_passenger: Passenger) -> None:
    font: pg.font.FontType = pg.font.Font(None, 150)
    win_message_img: pg.SurfaceType = font.render("YOU WON!", False, (0, 255, 0, 255), (0, 0, 0, 50))
    if x is None:
        x = w / 2 - win_message_img.get_width() / 2
    if y is None:
        y = h / 2 - win_message_img.get_height() / 2
    if my_passenger.is_parked:
        screen.blit(win_message_img, (x, y))


pg.init()

sc = pg.display.set_mode((w, h))
clock = pg.time.Clock()
running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
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
    sc.blit(pg.transform.scale(image_dict["empty_bg"], (w, h)), (0, 0))

    for obstacle in obstacles:
        sc.blit(obstacle.image, obstacle.rect)

    player.update()

    if player.is_crashed():
        player.rect.topleft = player.starting_position
        passenger.is_collected = False

    win_message(None, None, sc, passenger)

    passenger.update()

    sc.blit(parking.image, parking.rect)

    sc.blit(player.image, player.rect)

    sc.blit(hotel.image, hotel.rect)

    sc.blit(passenger.image, passenger.rect)

    pg.display.flip()

pg.quit()
