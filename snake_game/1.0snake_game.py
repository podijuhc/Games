import pygame as pg
from random import randrange

Window = 1000 #the poop scren size
tile_size = 50
Range = (tile_size // 2, Window - tile_size // 2, tile_size) # tile size
get_random = lambda: [randrange(*Range), randrange(*Range)] #were the snake starts
snake = pg.rect.Rect(0, 0, tile_size - 2, tile_size -2) #snake size making it smaler than tile size
snake.center = get_random() #snake posestion
lenth = 1 #size of the snake
segment = [snake.copy()] # difrent parts of the snake
snake_move = (0,0)
screen = pg.display.set_mode([Window]*2)
clock = pg.time.Clock() #how fast things move in the game

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                snake_move = (0, -tile_size)
            if event.key == pg.K_s:
                snake_move = (0, tile_size)
            if event.key == pg.K_a:
                snake_move = ( -tile_size, 0)
            if event.key == pg.K_d:
                snake_move = (tile_size, 0)


    screen.fill('black')#pop up scren colere
    #drwaing  the snake
    [pg.draw.rect(screen, 'dark green', segment) for segment in segment]
    #move the snake
    snake.move_ip(snake_move)
    segment = [snake.copy()]
    pg.display.flip()
    clock.tick(60)