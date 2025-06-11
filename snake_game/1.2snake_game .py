import pygame as pg
from random import randrange

Window = 1000  # screen size
tile_size = 50
Range = (tile_size // 2, Window - tile_size // 2, tile_size)  # tile size range
get_random = lambda: [randrange(*Range), randrange(*Range)]  # where the snake starts
snake = pg.rect.Rect(0, 0, tile_size - 2, tile_size - 2)  # snake size, making it smaller than tile size
snake.center = get_random()  # snake position
length = 1  # size of the snake

segment = [snake.copy()]  # different parts of the snake
snake_move = (0, 0)  # movement direction
time, timestep = 0, 110
food = snake.copy()
food.center = get_random()
screen = pg.display.set_mode([Window] * 2)
clock = pg.time.Clock()  # game clock

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
                snake_move = (-tile_size, 0)
            if event.key == pg.K_d:
                snake_move = (tile_size, 0)

    screen.fill('black')  # clear screen

    # Check if the snake eats food
    if food.center == snake.center:
        food.center = get_random()  # generate new food
        length += 1  # increase snake length

    # Draw food
    pg.draw.rect(screen, 'red', food)

    # Move the snake
    timenow = pg.time.get_ticks()
    if timenow - time > timestep:
        time = timenow
        snake.move_ip(snake_move)

        # Add the new head to the snake
        segment.insert(0, snake.copy())  # insert the new head at the front

        # If the snake has eaten food, don't remove the tail
        if len(segment) > length:
            segment.pop()  # remove the last part (tail)

    # Draw the snake (all segments)
    [pg.draw.rect(screen, 'dark green', s) for s in segment]

    pg.display.flip()  # update the screen
    clock.tick(60)  # set FPS