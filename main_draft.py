# SpaceInvader Pygame tutorial
# Link to the original video: https://www.youtube.com/watch?v=FfWpgLFMI7w

"""import math
import pygame
import random
from pygame import mixer

# 1. Initialize pygame, otherwise will not work
pygame.init()"""

# 2. Create a game window
"""screen = pygame.display.set_mode((800, 600))"""

"""# 11. Change background
background = pygame.image.load("background.png")

# 17. Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# 4. Change title & logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)"""

# 6. Player
"""player_img = pygame.image.load('space_invaders.png')
playerX = 370
playerY = 480
playerX_change = 0"""


def player(x, y):
    screen.blit(player_img, (x, y))


# 9. Enemy
# 16. Creating multiple enemies.
"""enemies_loc = {}
# enemies_loc = [[734, 60], [720, 70], [710, 80]]
num_of_enemies = 6  # the number of enemies on the screen
for i in range(1, num_of_enemies + 1):
    enemies_loc[i] = {
        'X': random.randint(0, 736),
        'Y': random.randint(0, 3) * 64,
        'X_change': 3
    }
#    X = random.randint(0, 735)
#    Y = random.randint(50, 150)
#    enemies_loc.append([X, Y])
enemy_img = pygame.image.load('aliens.png')
enemyY_change = 64"""


def enemies(x, y):
    screen.blit(enemy_img, (x, y))


# 12. bullet
"""bullet_img = pygame.image.load('laser.png')
bulletX = 0
bulletY = 480
bulletY_change = 16
bullet_state = 'ready'"""

"""# 17. Score
score_value = 0
font = pygame.font.Font('Player1UpBoldItalic-K9Xp.ttf', 24)
textX = 10
textY = 10

# 20. Game over function
game_over_f = pygame.font.Font('Player1Up3DRegular-81Jz.ttf', 48)"""


"""def game_over():
    end = game_over_f.render('GAME OVER', True, (255, 0, 0))
    screen.blit(end, (200, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))


# 14. Function to check if the bullet and the enemy are collided.
def is_collided(x0, y0, x1, y1):
    distance = math.dist([x0, y0], [x1, y1])
    if distance < 27:
        return True
    else:
        return False"""


# 3. Game loop
running = True
while running:
    # 5. Change Background colour (RGB)
    #screen.fill((0, 0, 100))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 8. Check if any key is pressed.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change += -10
            if event.key == pygame.K_RIGHT:
                playerX_change += 10
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change  # player movement
    # 8. Creating a border
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(1, num_of_enemies + 1):
        # 19. Game over text
        if enemies_loc[i]['Y'] >= 420:
            for j in range(1, num_of_enemies + 1):
                enemies_loc[j].update(Y = 2000)
            game_over()
            break

        enemies_loc[i]['X'] += enemies_loc[i]['X_change']

        if enemies_loc[i]['X'] >= 736:
            enemies_loc[i].update(X_change = -3)
            enemies_loc[i]['Y'] += enemyY_change
        elif enemies_loc[i]['X'] <= 0:
            enemies_loc[i].update(X_change = 3)
            enemies_loc[i]['Y'] += enemyY_change

        # 15. Collision condition
        collision = is_collided(enemies_loc[i]['X'], enemies_loc[i]['Y'],
                                bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = 'ready'

            score_value += 1
            enemies_loc[i].update(X = random.randint(0, 736))
            enemies_loc[i].update(Y = random.randint(0, 3) * 64)

        # 10. Layer an enemy image
        enemies(enemies_loc[i]['X'], enemies_loc[i]['Y'])

    # 13. Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # 7. Layer a player image on a background
    player(playerX, playerY)
    # 18. Calling score function
    show_score(textX, textY)
    pygame.display.update()
