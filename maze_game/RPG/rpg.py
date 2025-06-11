import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple RPG Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FLOOR_COLOR = (200, 200, 200)
WALL_COLOR = (100, 100, 100)
PLAYER_COLOR = (50, 150, 250)
ENEMY_COLOR = (250, 50, 50)
TEXT_COLOR = (255, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 24)

# Map layout: 0 = floor, 1 = wall
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Player attributes
player_pos = [1, 1]
player_hp = 10

# Enemy attributes
enemy_pos = [18, 7]
enemy_hp = 5

# Movement directions for enemy
directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]  # up, down, right, left, stay

clock = pygame.time.Clock()


def draw_map():
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            color = FLOOR_COLOR if tile == 0 else WALL_COLOR
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def draw_player():
    pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def draw_enemy():
    pygame.draw.rect(screen, ENEMY_COLOR, (enemy_pos[0] * TILE_SIZE, enemy_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def can_move(x, y):
    if 0 <= y < len(game_map) and 0 <= x < len(game_map[0]):
        return game_map[y][x] == 0
    return False


def move_enemy():
    global enemy_pos
    dx, dy = random.choice(directions)
    new_x, new_y = enemy_pos[0] + dx, enemy_pos[1] + dy
    if can_move(new_x, new_y) and [new_x, new_y] != player_pos:
        enemy_pos = [new_x, new_y]


def draw_text(text, x, y):
    img = font.render(text, True, TEXT_COLOR)
    screen.blit(img, (x, y))


def battle():
    global player_hp, enemy_hp
    # Simple battle: player and enemy lose 1 hp each turn
    player_hp -= 1
    enemy_hp -= 1


def main():
    global player_pos, player_hp, enemy_hp

    running = True
    battle_mode = False

    while running:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and not battle_mode:
                new_x, new_y = player_pos[0], player_pos[1]
                if event.key == pygame.K_LEFT:
                    new_x -= 1
                elif event.key == pygame.K_RIGHT:
                    new_x += 1
                elif event.key == pygame.K_UP:
                    new_y -= 1
                elif event.key == pygame.K_DOWN:
                    new_y += 1

                if can_move(new_x, new_y):
                    player_pos = [new_x, new_y]

        # Enemy movement
        if not battle_mode:
            move_enemy()

        # Check for battle
        if player_pos == enemy_pos and not battle_mode:
            battle_mode = True

        screen.fill(BLACK)
        draw_map()
        draw_player()
        draw_enemy()

        draw_text(f"Player HP: {player_hp}", 10, HEIGHT - 40)
        draw_text(f"Enemy HP: {enemy_hp}", 150, HEIGHT - 40)

        if battle_mode:
            battle()
            draw_text("Battle ongoing! Both lose 1 HP each turn.", 10, HEIGHT - 70)
            if player_hp <= 0:
                draw_text("You died! Game Over.", 10, HEIGHT - 100)
                pygame.display.flip()
                pygame.time.delay(3000)
                running = False
            elif enemy_hp <= 0:
                draw_text("Enemy defeated! You win!", 10, HEIGHT - 100)
                pygame.display.flip()
                pygame.time.delay(3000)
                running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
