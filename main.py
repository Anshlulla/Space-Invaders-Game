import pygame
import math
import random

# Initialize pygame
pygame.init()

# Create the screen - game window
screen = pygame.display.set_mode((800,600))
running = True

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon_path = r"C:\Users\Ansh Lulla\PycharmProjects\pygame_tutorial\venv\assets\ufo.png"
iconImg = pygame.image.load(icon_path)
pygame.display.set_icon(iconImg)

# Player
player_path = r"C:\Users\Ansh Lulla\PycharmProjects\pygame_tutorial\venv\assets\player.png"
playerImg = pygame.image.load(player_path)
playerX, playerY = 370, 480
playerX_change, playerY_change = 0, 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6
enemy_path = r"C:\Users\Ansh Lulla\PycharmProjects\pygame_tutorial\venv\assets\enemy.png"

for i in range(num_enemies):
    enemyImg.append(pygame.image.load(enemy_path))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(10)
    enemyY_change.append(14)

# Background
bg_path = r"C:\Users\Ansh Lulla\PycharmProjects\pygame_tutorial\venv\assets\background.png"
bgImg = pygame.image.load(bg_path)

# Bullet
bullet_path = r"C:\Users\Ansh Lulla\PycharmProjects\pygame_tutorial\venv\assets\bullet.png"
bulletImg = pygame.image.load(bullet_path)
bulletX, bulletY = 0, 480
bulletY_change = 12
bulletState = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX, textY = 10, 10

# Timer
total_time = 30  # in seconds
start_ticks = pygame.time.get_ticks()  # Get the current ticks when the game starts

# Player function
def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy Function
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Bullet Fire
def fire_bullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x+16,y+10))

# Collision Detection
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY-bulletY, 2))
    if distance < 27:
        return True
    return False

def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255,255,255))
    screen.blit(score, (x,y))

# Timer display function
def show_timer(x, y):
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000  # Convert milliseconds to seconds
    remaining_time = max(total_time - elapsed_time, 0)
    timer = font.render(f"Time: {remaining_time}s", True, (255, 255, 255))
    screen.blit(timer, (x, y))

# Game Over screen
def game_over_screen():
    game_over_font = pygame.font.Font("freesansbold.ttf", 64)
    score_font = pygame.font.Font("freesansbold.ttf", 32)

    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    final_score_text = score_font.render(f"Your Score: {score_value}", True, (255, 255, 255))

    screen.blit(game_over_text, (200, 250))
    screen.blit(final_score_text, (250, 350))
    pygame.display.update()
    pygame.time.delay(3000)  # Wait for 3 seconds before closing
    pygame.quit()
    exit()

# Game Loop
# If you want something to persist in the window infinitely, put that in this while loop
while running:
    #screen.fill((12, 55, 49))  # RGB
    screen.blit(bgImg, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Boundaries for player
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Bullet fire
    if bulletY <= 0:
        #bulletY = 480
        bulletState = "ready"

    if bulletState == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Enemy movement
    for i in range(num_enemies):
        enemyX[i] += enemyX_change[i]
        #enemyY[i] += enemyY_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        if enemyY[i] <= 0:
            enemyY[i] = 0
        elif enemyY[i] >= 420:
            enemyY[i] = 420

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = playerY
            bulletState = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(textX, textY)
    show_timer(10, 50)

    # Check for game end
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
    if elapsed_time >= total_time:
        game_over_screen()

    pygame.display.update() # update game state for events to occur