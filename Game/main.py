import pygame as pg

w, h = 400, 400
BLACK = (0, 0, 0)
FPS = 30

pg.init()

sc = pg.display.setmode((w, h))
clock = pg.time.Clock()
running = True
while running:
    clock.tick(FPS)

    for event in pg.event.get():
        if event == pg.QUIT:
            running = False
            pg.quit()

    pg.display.flip()