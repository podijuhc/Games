import pygame
import sys
import random
from collections import deque

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced RPG Maze Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FLOOR_COLOR = (220, 220, 220)
WALL_COLOR = (50, 50, 50)
PLAYER_COLOR = (50, 150, 250)
ENEMY_COLOR = (250, 50, 50)
TEXT_COLOR = (255, 255, 0)
HEALTH_BG = (100, 0, 0)
HEALTH_FG = (0, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 24)

# Bigger maze: 20x15 (1=wall, 0=path)
game_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,1,0,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,1],
    [1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# Player attributes
player_pos = [1, 1]
player_hp = 20
player_max_hp = 20
player_attack_power = 4

# Enemy attributes - multiple enemies
enemies = [
    {'pos': [18, 1], 'hp': 10, 'max_hp': 10, 'attack': 2},
    {'pos': [10, 7], 'hp': 8, 'max_hp': 8, 'attack': 3},
    {'pos': [14, 11], 'hp': 12, 'max_hp': 12, 'attack': 4}
]

clock = pygame.time.Clock()
enemy_move_cooldown = 3  # Counter to slow enemy moves

def draw_map():
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            color = FLOOR_COLOR if tile == 0 else WALL_COLOR
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_player():
    pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[0]*TILE_SIZE, player_pos[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_enemies():
    for enemy in enemies:
        if enemy['hp'] > 0:
            pygame.draw.rect(screen, ENEMY_COLOR, (enemy['pos'][0]*TILE_SIZE, enemy['pos'][1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_health_bar(x, y, current_hp, max_hp):
    bar_width = TILE_SIZE
    bar_height = 5
    fill_width = int((current_hp / max_hp) * bar_width)
    pygame.draw.rect(screen, HEALTH_BG, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, HEALTH_FG, (x, y, fill_width, bar_height))

def draw_hud():
    draw_text(f"HP: {player_hp}/{player_max_hp}", 10, HEIGHT - 30)
    draw_text("Press E to attack adjacent enemy", 200, HEIGHT - 30)

def draw_text(text, x, y):
    img = font.render(text, True, TEXT_COLOR)
    screen.blit(img, (x, y))

def can_move(x, y):
    if 0 <= y < len(game_map) and 0 <= x < len(game_map[0]):
        return game_map[y][x] == 0
    return False

def neighbors(pos):
    x, y = pos
    result = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x+dx, y+dy
        if can_move(nx, ny):
            result.append((nx, ny))
    return result

def bfs(start, goal):
    """Breadth-first search to find shortest path from start to goal."""
    queue = deque([start])
    came_from = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for nxt in neighbors(current):
            if nxt not in came_from:
                queue.append(nxt)
                came_from[nxt] = current
    # Reconstruct path
    path = []
    curr = goal
    while curr != start:
        if curr not in came_from:
            return []  # No path
        path.append(curr)
        curr = came_from[curr]
    path.reverse()
    return path

def enemy_turn():
    global enemy_move_cooldown
    enemy_move_cooldown += 1
    if enemy_move_cooldown < 5:  # Enemies move once every 5 frames (slower)
        return
    enemy_move_cooldown = 0

    for enemy in enemies:
        if enemy['hp'] <= 0:
            continue
        # If next to player, attack
        ex, ey = enemy['pos']
        px, py = player_pos
        dist = abs(ex - px) + abs(ey - py)
        if dist == 1:
            attack(enemy)
        else:
            # Move towards player if path exists
            path = bfs(tuple(enemy['pos']), tuple(player_pos))
            if path and len(path) > 0:
                next_step = path[0]
                # Check no enemy occupies next step
                if not any(e['pos'] == list(next_step) and e != enemy and e['hp'] > 0 for e in enemies):
                    enemy['pos'] = list(next_step)

def attack(attacker):
    global player_hp
    # If attacker is enemy attacking player
    if isinstance(attacker, dict) and 'pos' in attacker:  # enemy dict
        player_hp -= attacker['attack']
    else:
        # Player attack (attacker is player)
        for enemy in enemies:
            ex, ey = enemy['pos']
            px, py = player_pos
            dist = abs(ex - px) + abs(ey - py)
            if dist == 1 and enemy['hp'] > 0:
                enemy['hp'] -= player_attack_power
                break

def main():
    global player_hp

    running = True

    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                new_x, new_y = player_pos[0], player_pos[1]
                if event.key == pygame.K_a:
                    new_x -= 1
                elif event.key == pygame.K_d:
                    new_x += 1
                elif event.key == pygame.K_w:
                    new_y -= 1
                elif event.key == pygame.K_s:
                    new_y += 1
                elif event.key == pygame.K_e:
                    attack('player')

                if can_move(new_x, new_y):
                    # Check no enemy in that tile
                    if not any(enemy['pos'] == [new_x,new_y] and enemy['hp']>0 for enemy in enemies):
                        player_pos[0], player_pos[1] = new_x, new_y

        enemy_turn()

        screen.fill(BLACK)
        draw_map()
        draw_player()
        draw_enemies()
        draw_hud()

        # Draw health bars above enemies
        for enemy in enemies:
            if enemy['hp'] > 0:
                x = enemy['pos'][0] * TILE_SIZE
                y = enemy['pos'][1] * TILE_SIZE - 10
                draw_health_bar(x, y, enemy['hp'], enemy['max_hp'])

        # Draw player health bar top-left corner
        draw_health_bar(10, HEIGHT - 50, player_hp, player_max_hp)

        if player_hp <= 0:
            draw_text("You died! Game Over.", WIDTH//2 - 80, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False
        elif all(enemy['hp'] <= 0 for enemy in enemies):
            draw_text("All enemies defeated! You win!", WIDTH//2 - 110, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
