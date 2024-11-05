import pygame
import sys
import random

# Initialize Pygame and its mixer for sounds
pygame.init()
pygame.mixer.init()

# Load sound effects
jump_sound = pygame.mixer.Sound("jump.wav")
collect_sound = pygame.mixer.Sound("collect.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
stomp_sound = pygame.mixer.Sound("stomp.wav")  # New sound for stomping on enemies

# Load images and scale them
ground_img = pygame.image.load("ground.png")
ground_img = pygame.transform.scale(ground_img, (800, 100))  # Scale ground image

platform_img = pygame.image.load("platform.png")
platform_img = pygame.transform.scale(platform_img, (200, 20))  # Scale platform image

marko_img = pygame.image.load("marko.png")
marko_img = pygame.transform.scale(marko_img, (50, 50))  # Scale Marko image

polo_img = pygame.image.load("polo.png")
polo_img = pygame.transform.scale(polo_img, (50, 50))  # Scale Polo image

enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (60, 60))  # Scale enemy image to a bigger size

collectible_img = pygame.image.load("collectible.png")
collectible_img = pygame.transform.scale(collectible_img, (20, 20))  # Scale collectible image

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Marko Brothers")

# Define constants
GRAVITY = 0.8
PLAYER_SPEED = 5
JUMP_STRENGTH_MARKO = 15
JUMP_STRENGTH_POLO = 18
MAX_LIVES = 3
STOMP_BOUNCE = -10  # Bounce upward when stomping on an enemy

# Player attributes
player_size = (50, 50)

# Initialize players' positions
marko_pos = [100, SCREEN_HEIGHT - 150]
marko_vel_y = 0
marko_on_ground = False
marko_lives = MAX_LIVES

polo_pos = [200, SCREEN_HEIGHT - 150]
polo_vel_y = 0
polo_on_ground = False
polo_lives = MAX_LIVES

# Define ground level and platforms
ground_level = SCREEN_HEIGHT - 100
platforms = [
    pygame.Rect(150, 400, 200, 20),
    pygame.Rect(400, 300, 200, 20),
    pygame.Rect(250, 200, 150, 20)
]

# Enemy attributes
enemy_size = (60, 60)  # Increased enemy size
enemies = [pygame.Rect(200, 400 - enemy_size[1], *enemy_size),
           pygame.Rect(450, 300 - enemy_size[1], *enemy_size)]
enemy_speed = 2

# Collectibles
collectible_size = (20, 20)
collectibles = [
    pygame.Rect(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, ground_level - 150), *collectible_size)
    for _ in range(5)
]

# Scoring
score = 0
font = pygame.font.Font(None, 36)

# Initialize camera
camera_x = 0

def reset_level():
    """Reset the level after all collectibles are gathered."""
    global collectibles, score, marko_pos, polo_pos, marko_lives, polo_lives
    collectibles = [
        pygame.Rect(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, ground_level - 150), *collectible_size)
        for _ in range(5)
    ]
    score += 50  # Reward for completing the level

    # Reset player positions and lives
    marko_pos = [100, SCREEN_HEIGHT - 150]
    marko_vel_y = 0
    marko_on_ground = False
    marko_lives = MAX_LIVES

    polo_pos = [200, SCREEN_HEIGHT - 150]
    polo_vel_y = 0
    polo_on_ground = False
    polo_lives = MAX_LIVES

def game_over():
    """Show Game Over screen and wait for restart."""
    screen.fill((0, 0, 0))
    game_over_text = font.render("Game Over! Press R to Restart", True, (255, 255, 255))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_level()  # Reset the game state
                return  # Restart the game

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((135, 206, 235))

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get player input
    keys = pygame.key.get_pressed()

    # --- Marko's Controls ---
    if keys[pygame.K_a]:
        marko_pos[0] -= PLAYER_SPEED
    if keys[pygame.K_d]:
        marko_pos[0] += PLAYER_SPEED
    if keys[pygame.K_w] and marko_on_ground:
        marko_vel_y = -JUMP_STRENGTH_MARKO
        marko_on_ground = False
        jump_sound.play()

    # --- Polo's Controls ---
    if keys[pygame.K_LEFT]:
        polo_pos[0] -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        polo_pos[0] += PLAYER_SPEED
    if keys[pygame.K_UP] and polo_on_ground:
        polo_vel_y = -JUMP_STRENGTH_POLO
        polo_on_ground = False
        jump_sound.play()

    # --- Gravity and Movement for Marko ---
    marko_vel_y += GRAVITY
    marko_pos[1] += marko_vel_y

    if marko_pos[1] >= ground_level - player_size[1]:
        marko_pos[1] = ground_level - player_size[1]
        marko_vel_y = 0
        marko_on_ground = True

    marko_rect = pygame.Rect(*marko_pos, *player_size)
    for platform in platforms:
        if marko_rect.colliderect(platform) and marko_vel_y >= 0:
            marko_pos[1] = platform.top - player_size[1]
            marko_vel_y = 0
            marko_on_ground = True

    # --- Gravity and Movement for Polo ---
    polo_vel_y += GRAVITY
    polo_pos[1] += polo_vel_y

    if polo_pos[1] >= ground_level - player_size[1]:
        polo_pos[1] = ground_level - player_size[1]
        polo_vel_y = 0
        polo_on_ground = True

    polo_rect = pygame.Rect(*polo_pos, *player_size)
    for platform in platforms:
        if polo_rect.colliderect(platform) and polo_vel_y >= 0:
            polo_pos[1] = platform.top - player_size[1]
            polo_vel_y = 0
            polo_on_ground = True

    # --- Camera Logic ---
    rightmost_player = max(marko_pos[0], polo_pos[0])
    if rightmost_player > SCREEN_WIDTH // 2:
        camera_x = rightmost_player - SCREEN_WIDTH // 2

    # --- Enemy Movement and Collision ---
    for enemy in enemies[:]:  # Use a copy of the list to safely remove enemies
        enemy.x += enemy_speed
        if enemy.left <= 150 or enemy.right >= SCREEN_WIDTH - 150:
            enemy_speed = -enemy_speed

        # Adjust enemy position for camera
        enemy.x -= camera_x

        if marko_rect.colliderect(enemy):
            # Check if Marko is stomping the enemy (approaching from above)
            if marko_vel_y > 0 and marko_rect.bottom - enemy.top <= 10:
                enemies.remove(enemy)
                stomp_sound.play()
                marko_vel_y = STOMP_BOUNCE  # Bounce up after stomping
                score += 20
            else:
                hit_sound.play()
                marko_lives -= 1
                marko_pos = [100, SCREEN_HEIGHT - 150]  # Reset position after hit

        if polo_rect.colliderect(enemy):
            # Check if Polo is stomping the enemy
            if polo_vel_y > 0 and polo_rect.bottom - enemy.top <= 10:
                enemies.remove(enemy)
                stomp_sound.play()
                polo_vel_y = STOMP_BOUNCE
                score += 20
            else:
                hit_sound.play()
                polo_lives -= 1
                polo_pos = [200, SCREEN_HEIGHT - 150]  # Reset position after hit

    if marko_lives <= 0 and polo_lives <= 0:
        game_over()

    # --- Collectibles Collision ---
    for collectible in collectibles[:]:
        if marko_rect.colliderect(collectible) or polo_rect.colliderect(collectible):
            collectibles.remove(collectible)
            score += 10
            collect_sound.play()

    if not collectibles:
        reset_level()

    # --- Drawing ---
    for x in range(0, SCREEN_WIDTH, ground_img.get_width()):
        screen.blit(ground_img, (x - camera_x, ground_level))

    for platform in platforms:
        screen.blit(platform_img, (platform.x - camera_x, platform.y))

    for enemy in enemies:
        screen.blit(enemy_img, (enemy.x, enemy.y))

    for collectible in collectibles:
        screen.blit(collectible_img, (collectible.x - camera_x, collectible.y))  # Corrected collectible drawing position

    screen.blit(marko_img, (marko_pos[0] - camera_x, marko_pos[1]))
    screen.blit(polo_img, (polo_pos[0] - camera_x, polo_pos[1]))

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    lives_text = font.render(f"Marko Lives: {marko_lives} | Polo Lives: {polo_lives}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

    pygame.display.flip()
    clock.tick(30)
