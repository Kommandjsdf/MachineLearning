from collections import defaultdict
import numpy as np

import pygame as pg
from random import choice, randint, random

w, h = 700, 450
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 30

pg.init()

sc = pg.display.set_mode((w, h))
clock = pg.time.Clock()
running = True

image_dict = {
    "bg": pg.image.load("img/Background.png"),
    "empty_bg": pg.image.load("img/empty_background.png"),
    "player": {
        "front": pg.image.load("img/cab_front.png"),
        "left": pg.image.load("img/cab_left.png"),
        "rear": pg.image.load("img/cab_rear.png"),
        "right": pg.image.load("img/cab_right.png"),
    },
    "hole": pg.image.load("img/hole.png"),
    "hotel": pg.transform.scale(pg.image.load("img/hotel.png"), (80, 80)),
    "passenger": pg.image.load("img/passenger.png"),
    "taxi_bg": pg.transform.scale(pg.image.load("img/taxi_background.png"), (32, 32)),
    "parking": pg.transform.scale(pg.image.load("img/parking.png"), (48, 48)),
    "obstacle": {
        "small": pg.image.load("img/small_barrier.png"),
        "tall": pg.image.load("img/tall_barrier.png"),
        "long": pg.image.load("img/long_barrier.png")
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
        if self.rect.collidelist(obstacles) != -1 or \
                hotel.rect.colliderect(self.rect) or \
                self.rect.left < 0 or self.rect.right > w or self.rect.top < 0 or self.rect.bottom > h:
            return True
        return False


class Hotel:
    def __init__(self, x=None, y=None):
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


player: Player = Player(300, 210)
hotel: Hotel = Hotel()
parking: Parking = Parking(hotel)

obstacles: list[Obstacle] = []
long_obstacle1 = Obstacle(65, 14, "long")
long_obstacle2 = Obstacle(65, 415, "long")
tall_obstacle1 = Obstacle(12, 67, "tall")
tall_obstacle2 = Obstacle(645, 67, "tall")
small_obstacle1 = Obstacle(265, 67, "small")
small_obstacle2 = Obstacle(139, 261, "small")
small_obstacle3 = Obstacle(392, 261, "small")
obstacles.extend(
    (long_obstacle1, long_obstacle2, tall_obstacle1, tall_obstacle2, small_obstacle1, small_obstacle2, small_obstacle3))

## Q-LEARNING

def apply_action(action):
    # global player
    x_direction = player.x_direction
    y_direction = player.y_direction
    match action:
        case None:
            return
        case 0:
            x_direction = 1
            player.view = "right"
        case 1:
            x_direction = -1
            player.view = "left"
        case 2:
            y_direction = -1
            player.view = "rear"
        case 3:
            y_direction = 1
            player.view = "front"

    new_x = player.rect.x + player.rect.width * x_direction
    new_y = player.rect.y + player.rect.height * y_direction

    if 0 < new_x < w - player.rect.width:
        player.rect.x = new_x
    if 0 < new_y < h - player.rect.height:
        player.rect.y = new_y

actions = [0, 1, 2, 3] # 0 - right, 1 - left, 2 - up, 3 - down
# (x, y) : [0, 0, 0, 0]
Q_table = defaultdict(lambda: [0, 0, 0, 0])

learning_rate = 0.9
discount_factor = 0.9
epsilon = -1

def choose_action(state):
    if random() < epsilon:
        return choice(actions)
    else:
        return np.argmax(Q_table[state])

def update_Q(state, action, reward, new_state):
    base_next = max(Q_table[new_state])
    Q_table[state][action] += learning_rate * (discount_factor * base_next + reward - Q_table[state][action])

def make_step():
    current_state = (player.rect.x, player.rect.y)
    action = choose_action(current_state)

    apply_action(action)

    reward = -1
    episode_end = False
    success = False
    if player.is_crashed():
        reward = -100
        episode_end = True
    elif parking.rect.contains(player.rect):
        reward = 100
        episode_end = True
        success = True

    next_state = (player.rect.x, player.rect.y)
    update_Q(current_state, action, reward, next_state)

    return episode_end, success


num_episodes = 300
max_step = 50
for episode in range(num_episodes):
    player.rect.x, player.rect.y = 300, 300
    for step in range(max_step):
        ep_end, suc = make_step()
        if ep_end:
            print(suc)
            break

print(Q_table)

## Q-LEARNING

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

    # if player.is_crashed():
    #     player.rect.topleft = player.starting_position

    sc.blit(parking.image, parking.rect)

    sc.blit(player.image, player.rect)

    sc.blit(hotel.image, hotel.rect)

    pg.display.flip()

pg.quit()
