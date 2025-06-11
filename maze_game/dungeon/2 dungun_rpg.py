import pygame
import sys
from collections import deque
import math

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 1000
TILE_SIZE = 32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Dungeon of Veshchi")
clock = pygame.time.Clock()


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FLOOR_COLOR = (40, 40, 40)  # Darker floor
FLOOR_COLOR2 = (105, 117, 138) #liter floor
WALL_COLOR = (10, 10, 10)  # Dark walls
TEXT_COLOR = (255, 255, 0)
HEALTH_BG = (100, 0, 0)
HEALTH_FG = (0, 255, 0)


# Fonts
font = pygame.font.SysFont(None, 24)

# Dungeon map: 30x35 (1=wall, 0=path)
game_map = [
    [1] * 30,
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1] * 30,
]

# Treasure locations (x,y)
treasures = [[3, 1], [15, 12], [8, 10], [15, 15], [8, 12]]
trigger_chests = [[8, 12], [15, 15]]

# Treasure sound
trigger_chest_sound = pygame.mixer.Sound("332629__treasuresounds__item-pickup.ogg")
trigger_chest_sound.set_volume(0.5)

# Treasure opening
Open_TREASURE_frames = [
    pygame.image.load("chest_open_1.png").convert_alpha(),
    pygame.image.load("chest_open_2.png").convert_alpha(),
    pygame.image.load("chest_open_3.png").convert_alpha(),
    pygame.image.load("chest_open_4.png").convert_alpha(),
]
Open_TREASURE_frames = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in Open_TREASURE_frames]

TREASURE_image = [
    pygame.image.load("chest_1.png").convert_alpha(),

]

TREASURE_image = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in TREASURE_image]

# Player
player_pos = [1, 1]
player_hp = 30
player_max_hp = 30
player_attack_power = 4
player_attack_range = 2
player_score = 0
player_keys = 0
VISION_RADIUS = 6
player_frame_index = 0

player_frames = [
    pygame.image.load("priest3_v1_1.png").convert_alpha(),
    pygame.image.load("priest3_v1_2.png").convert_alpha(),
    pygame.image.load("priest3_v1_3.png").convert_alpha(),
    pygame.image.load("priest3_v1_4.png").convert_alpha(),

]

player_frames = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in player_frames]

# Enemy attributes - multiple enemies with activation radiusd
enemies = [
    {'pos': [28, 1], 'hp': 10, 'cooldown': 0, 'max_hp': 10, 'attack': 2, 'active': False, 'detect_range': 6,
     'type': 'scull', 'style': 'ranged', 'frame_index': 0, 'frame_timer': 0.0},
    {'pos': [10, 7], 'hp': 8, 'cooldown': 6, 'max_hp': 8, 'attack': 3, 'active': False, 'detect_range': 6,
     'type': 'vampire', 'style': 'melee', 'frame_index': 0, 'frame_timer': 0.0},
    {'pos': [14, 11], 'hp': 12, 'cooldown': 8 , 'max_hp': 12, 'attack': 4, 'active': False, 'detect_range': 6,
     'type': 'skeleton', 'style': 'defensive', 'frame_index': 0, 'frame_timer': 0.0},
]


enemy_move_cooldown = 3  # Counter to slow enemy moves

enemy_imgs = {
    "scull": pygame.image.load("skull_v2_1.png").convert_alpha(),
    "vampire": pygame.image.load("vampire_v2_4.png").convert_alpha(),
    "skeleton": pygame.image.load("skeleton2_v2_1.png").convert_alpha(),

}

enemy_frames = {
    "scull": [
        pygame.image.load("skull_v2_1.png").convert_alpha(),
        pygame.image.load("skull_v2_2.png").convert_alpha(),
        pygame.image.load("skull_v2_3.png").convert_alpha(),
        pygame.image.load("skull_v2_4.png").convert_alpha(),
    ],
    "vampire": [
        pygame.image.load("vampire_v2_3.png").convert_alpha(),
        pygame.image.load("vampire_v2_4.png").convert_alpha(),
        pygame.image.load("vampire_v2_2.png").convert_alpha(),

    ],
    "skeleton": [
        pygame.image.load("skeleton2_v2_1.png").convert_alpha(),
        pygame.image.load("skeleton2_v2_2.png").convert_alpha(),
        pygame.image.load("skeleton2_v2_3.png").convert_alpha(),
        pygame.image.load("skeleton2_v2_4.png").convert_alpha(),

    ],
}
# Scale
for key in enemy_frames:
    enemy_frames[key] = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in enemy_frames[key]]


def draw_map():
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if math.dist((x, y), player_pos) <= VISION_RADIUS:
                color = FLOOR_COLOR if tile == 0 else WALL_COLOR
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                # Draw treasure
                if [x, y] in treasures:
                    screen.blit(TREASURE_image[0], (x * TILE_SIZE, y * TILE_SIZE))
            else:
                pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if math.dist((x, y), player_pos) <= VISION_RADIUS:
                if abs(player_pos[0] - x) + abs(player_pos[1] - y) <= player_attack_range:
                    pygame.draw.rect(screen, (0, 50, 50), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)


def draw_player():
    screen.blit(player_frames[player_frame_index], (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

def draw_enemies():
    for enemy in enemies:
        if enemy['hp'] > 0 and enemy['active']:
            if math.dist(enemy['pos'], player_pos) <= VISION_RADIUS:
                if enemy.get('spawned_from_chest', False):
                    # Just draw first frame (static)
                    frame = enemy_frames[enemy['type']][0]
                else:
                    # Animate
                    enemy.setdefault('frame_timer', 0.0)
                    enemy.setdefault('frame_index', 0)
                    enemy['frame_timer'] += 0.1
                    if enemy['frame_timer'] >= 1:
                        enemy['frame_timer'] = 0
                        enemy['frame_index'] = (enemy['frame_index'] + 1) % len(enemy_frames[enemy['type']])
                    frame = enemy_frames[enemy['type']][enemy['frame_index']]

                screen.blit(frame, (enemy['pos'][0] * TILE_SIZE, enemy['pos'][1] * TILE_SIZE))




def draw_health_bar(x, y, current_hp, max_hp):
    bar_width = TILE_SIZE
    bar_height = 5
    fill_width = int((current_hp / max_hp) * bar_width)
    pygame.draw.rect(screen, HEALTH_BG, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, HEALTH_FG, (x, y, fill_width, bar_height))


def draw_hud():
    draw_text(f"HP: {player_hp}/{player_max_hp}  Score: {player_score}", 10, HEIGHT - 30)
    draw_text("Use WASD or arrow keys to move, E to attack adjacent enemy, collect gold!", 10, HEIGHT - 50)


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
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
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
    if enemy_move_cooldown < 5:  # Enemies move once every 5 frames
        return
    enemy_move_cooldown = 0

    for enemy in enemies:
        if enemy['hp'] <= 0:
            continue

        # Activate enemy if player is within detect range
        dist_to_player = abs(enemy['pos'][0] - player_pos[0]) + abs(enemy['pos'][1] - player_pos[1])
        if dist_to_player <= enemy['detect_range']:
            enemy['active'] = True
        else:
            enemy['active'] = False

        if not enemy['active']:
            continue

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
    global player_hp, player_score
    if isinstance(attacker, dict) and 'pos' in attacker:
        # Enemy attacking player
        player_hp -= attacker['attack']
    else:
        for enemy in enemies:
            if enemy['hp'] <= 0:
                continue
            ex, ey = enemy['pos']
            px, py = player_pos
            dist = abs(ex - px) + abs(ey - py)
            if dist <= player_attack_range and has_line_of_sight((px, py), (ex, ey)):
                enemy['hp'] -= player_attack_power
                if enemy['hp'] <= 0:
                    player_score += 10
                break


def has_line_of_sight(start, end):
    path = bfs(start, end)
    if not path:
        return False
    return len(path) <= player_attack_range

def handle_trigger_chest(pos):
    # Draw message centered
    draw_text("A triggered chest was opened! Something happens...", WIDTH // 2 - 110, HEIGHT // 2)
    pygame.display.flip()

    # Example: spawn a surprise enemy next to the player
    px, py = player_pos
    for dx, dy in [(-2, 2), (2, 2), (2, -2), (-2, -2)]:
        new_x, new_y = px + dx, py + dy
        if can_move(new_x, new_y) and not any(e['pos'] == [new_x, new_y] for e in enemies):
            enemies.append({
                'pos': [new_x, new_y],
                'hp': 8,
                'cooldown': 6,
                'max_hp': 8,
                'attack': 3,
                'active': False,
                'detect_range': 5,
                'type': 'vampire',
                'style': 'ranged',
                'frame_index': 0,
                'frame_timer': 0.0,
                'spawned_from_chest': True
            })
            print(f"An enemy has appeared at ({new_x}, {new_y})!")
            break


def collect_treasure():
    global player_score
    if player_pos in treasures:
        trigger_chest_sound.play()
        # Animate opening chest frames
        for frame in Open_TREASURE_frames:
            screen.fill(BLACK)  # Or redraw the map, player etc.
            draw_map()
            draw_player()
            draw_enemies()
            screen.blit(frame, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))
            pygame.display.flip()
            pygame.time.delay(150)  # delay between frames

        treasures.remove(player_pos)
        player_score += 20

        if player_pos in trigger_chests:
            handle_trigger_chest(player_pos)


def main():
    global player_hp, player_frame_index

    running = True
    frame_timer = 0
    animation_speed = 0.2

    while running:
        clock.tick(30)

        # Animate player sprite
        frame_timer += animation_speed
        if frame_timer >= 1:
            frame_timer = 0
            player_frame_index = (player_frame_index + 1) % len(player_frames)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                new_x, new_y = player_pos[0], player_pos[1]
                if event.key in [pygame.K_a, pygame.K_LEFT]:
                    new_x -= 1
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    new_x += 1
                elif event.key in [pygame.K_w, pygame.K_UP]:
                    new_y -= 1
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    new_y += 1

                if can_move(new_x, new_y):
                    player_pos[0], player_pos[1] = new_x, new_y

                # Attack on pressing 'E'
                if event.key == pygame.K_e:
                    attack('player')


        # Enemy turn
        enemy_turn()

        # Collect treasure if on same tile
        collect_treasure()

        # Draw everything
        screen.fill(BLACK)
        draw_map()
        draw_player()
        draw_enemies()
        draw_hud()

        # Draw player health bar above player
        draw_health_bar(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE - 7, player_hp, player_max_hp)

        pygame.display.flip()

        # Check for game over
        if player_hp <= 0:
            print("Game Over!")
            running = False
        elif all(enemy['hp'] <= 0 for enemy in enemies):
            draw_text("All enemies defeated! You win!", WIDTH // 2 - 110, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()