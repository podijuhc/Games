import pygame
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Maze layout (1 = wall, 0 = path)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Player settings
player_pos = [1, 1]  # Starting tile (x, y)
player_color = (255, 0, 0)
player_size = TILE_SIZE - 10  # slightly smaller than tile

# Colors
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (255, 255, 255)
BG_COLOR = (50, 50, 50)

clock = pygame.time.Clock()


def draw_maze():
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            color = PATH_COLOR if tile == 0 else WALL_COLOR
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def draw_player():
    px = player_pos[0] * TILE_SIZE + (TILE_SIZE - player_size) // 2
    py = player_pos[1] * TILE_SIZE + (TILE_SIZE - player_size) // 2
    pygame.draw.rect(screen, player_color, (px, py, player_size, player_size))


def is_valid_move(x, y):
    if 0 <= y < len(maze) and 0 <= x < len(maze[0]):
        return maze[y][x] == 0
    return False


def main():
    running = True
    while running:
        clock.tick(60)  # 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                new_x, new_y = player_pos[0], player_pos[1]
                if event.key == pygame.K_LEFT:
                    new_x -= 1
                elif event.key == pygame.K_RIGHT:
                    new_x += 1
                elif event.key == pygame.K_UP:
                    new_y -= 1
                elif event.key == pygame.K_DOWN:
                    new_y += 1

                if is_valid_move(new_x, new_y):
                    player_pos[0], player_pos[1] = new_x, new_y

        screen.fill(BG_COLOR)
        draw_maze()
        draw_player()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
