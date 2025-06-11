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
pygame.display.set_caption("Dungeon RPG")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FLOOR_COLOR = (40, 40, 40)  # Darker floor
FLOOR_COLOR2 = (105, 117, 138) #liter floor
WALL_COLOR = (10, 10, 10)  # Dark walls
TEXT_COLOR = (255, 255, 0)
HEALTH_BG = (100, 0, 0)
HEALTH_FG = (0, 255, 0)
TREASURE_COLOR = (255, 215, 0)  # Gold color
locked_treasures = (92, 44, 2)

# Fonts
font = pygame.font.SysFont(None, 24)

# Dungeon map: 30x35 (1=wall, 0=path)
game_map = [
    [1] * 30,
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
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
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Treasure locations (x,y)
treasures = [[3, 1], [15, 12], [8, 10]]
trigger_chests = [[8, 10], [15, 12]]
locked_treasures = [[19, 27]]  # Requires key to open
boss_door_pos = [27, 28]  # Where the locked door is
boss_room_entered = False


# Player attributes
player_pos = [1, 1]
player_hp = 20
player_max_hp = 20
player_attack_power = 4
player_score = 0
player_keys = 0

player_img = pygame.image.load("priest3_v1_1.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))

# Enemy attributes - multiple enemies with activation radius
enemies = [
    {'pos': [18, 1], 'hp': 10, 'cooldown': 0, 'max_hp': 10, 'attack': 2, 'active': False, 'detect_range': 6, 'type': 'scull', 'style': 'melee'},
    {'pos': [10, 7], 'hp': 8, 'cooldown': 6, 'max_hp': 8, 'attack': 3, 'active': False, 'detect_range': 6, 'type': 'vampire', 'style': 'ranged'},
    {'pos': [14, 11], 'hp': 12, 'cooldown': 8 , 'max_hp': 12, 'attack': 4, 'active': False, 'detect_range': 6, 'type': 'skeleton', 'style': 'defensive'},
]

enemy_imgs = {
    "scull": pygame.image.load("skull_v2_1.png").convert_alpha(),
    "vampire": pygame.image.load("vampire_v2_4.png").convert_alpha(),
    "skeleton": pygame.image.load("skeleton2_v2_1.png").convert_alpha(),

}


# Scale them to TILE_SIZE
for key in enemy_imgs:
    enemy_imgs[key] = pygame.transform.scale(enemy_imgs[key], (TILE_SIZE, TILE_SIZE))


clock = pygame.time.Clock()
enemy_move_cooldown = 3  # Counter to slow enemy moves
VISION_RADIUS = 6  # Player vision radius


def draw_map():
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            # Fog of war: only draw tiles within vision radius
            if math.dist((x, y), player_pos) <= VISION_RADIUS:
                color = FLOOR_COLOR if tile == 0 else WALL_COLOR
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                # Draw treasure if present
                if [x, y] in treasures:
                    pygame.draw.rect(screen, TREASURE_COLOR,
                                     (x * TILE_SIZE + 8, y * TILE_SIZE + 8, TILE_SIZE // 2, TILE_SIZE // 2))
            else:
                # Draw black for unexplored tiles (fog)
                pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def draw_player():
    screen.blit(player_img, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))


#def draw_enemies():
#    for enemy in enemies:
#        if enemy['hp'] > 0 and enemy['active']:
#            # Only draw enemies within vision radius
#            if math.dist(enemy['pos'], player_pos) <= VISION_RADIUS:
#                pygame.draw.rect(screen, ENEMY_COLOR,
#                                 (enemy['pos'][0] * TILE_SIZE, enemy['pos'][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_enemies():
    for enemy in enemies:
        if enemy['hp'] > 0 and enemy['active']:
            # Only draw enemies within vision radius
            if math.dist(enemy['pos'], player_pos) <= VISION_RADIUS:
                screen.blit(enemy_imgs[enemy['type']], (enemy['pos'][0] * TILE_SIZE, enemy['pos'][1] * TILE_SIZE))




def draw_health_bar(x, y, current_hp, max_hp):
    bar_width = TILE_SIZE
    bar_height = 5
    fill_width = int((current_hp / max_hp) * bar_width)
    pygame.draw.rect(screen, HEALTH_BG, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, HEALTH_FG, (x, y, fill_width, bar_height))


def draw_hud():
    draw_text(f"HP: {player_hp}/{player_max_hp}  Score: {player_score}", 10, HEIGHT - 30)
    draw_text("Use WASD to move, E to attack adjacent enemy, collect gold!", 10, HEIGHT - 50)


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
    if enemy_move_cooldown < 5:  # Enemies move once every 5 frames (slower)
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
                if enemy['hp'] <= 0:
                    player_score += 10  # Gain points for defeating enemy
                break

def collect_treasure():
    global player_score

    if player_pos in treasures:
        print("Treasure collected at", player_pos)
        treasures.remove(player_pos)
        player_score += 20
        if player_pos in trigger_chests:  # Check if this was a trigger chest
            handle_trigger_chest(player_pos)

def handle_trigger_chest(pos):
    draw_text("A triggered chest was opened! Something happens...", WIDTH // 2 - 110, HEIGHT // 2)
    # Example: spawn a surprise enemy next to the player
    px, py = player_pos
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x, new_y = px + dx, py + dy
        if can_move(new_x, new_y) and not any(e['pos'] == [new_x, new_y] for e in enemies):
            enemies.append({
                'pos': [8, 7],
                'hp': 8,
                'cooldown': 6,
                'max_hp': 8,
                'attack': 3,
                'active': False,
                'detect_range': 5,
                'type': 'vampire',
                'style': 'ranged'
            })
            print(f"An enemy has appeared at ({new_x}, {new_y})!")
            break


def collect_treasure():
    global player_score, player_keys

    if player_pos in treasures:
        if player_pos in locked_treasures:
            if player_keys > 0:
                print("Used a key to open locked treasure.")
                locked_treasures.remove(player_pos)
                player_keys -= 1
                player_score += 50
                treasures.remove(player_pos)
            else:
                print("This treasure is locked. Find a key!")
        else:
            print("Treasure collected.")
            treasures.remove(player_pos)
            player_score += 20

        # Trigger special event
        if player_pos in trigger_chests:
            handle_trigger_chest(player_pos)


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
                    if not any(enemy['pos'] == [new_x, new_y] and enemy['hp'] > 0 for enemy in enemies):
                        player_pos[0], player_pos[1] = new_x, new_y

        collect_treasure()
        enemy_turn()

        screen.fill(BLACK)
        draw_map()
        draw_player()
        draw_enemies()
        draw_hud()

        # Draw health bars above enemies
        for enemy in enemies:
            if enemy['hp'] > 0 and enemy['active']:
                x = enemy['pos'][0] * TILE_SIZE
                y = enemy['pos'][1] * TILE_SIZE - 10
                draw_health_bar(x, y, enemy['hp'], enemy['max_hp'])

        # Draw player health bar top-left corner
        draw_health_bar(10, HEIGHT - 50, player_hp, player_max_hp)

        if player_hp <= 0:
            draw_text("You died! Game Over.", WIDTH // 2 - 80, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False
#        elif all(enemy['hp'] <= 0 for enemy in enemies):
#            draw_text("All enemies defeated! You win!", WIDTH // 2 - 110, HEIGHT // 2)
#            pygame.display.flip()
#            pygame.time.delay(3000)
#            running = False

        pygame.display.flip()




if __name__ == "__main__":
    main()
