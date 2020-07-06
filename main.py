# The goal of this project is to create a game using pygame Python package
# Game: Space Invaders
# Rules: destroy alien spaceships before they reach you.

# Importing required packages.
import math
import pygame
import random
from pygame import mixer

# Initializing Pygame
pygame.init()

# Creating a game window
screen = pygame.display.set_mode((800, 600))

# Title, logo, background
pygame.display.set_caption("Space Invaders")

icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

background = pygame.image.load("background.png")

mixer.music.load('background.wav')
mixer.music.play(-1)


# VARIABLES
# Player
player_img = pygame.image.load('space_invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemies
enemy_img = pygame.image.load('aliens.png')
enemies_loc = {}
num_of_enemies = 6  # the number of enemies on the screen
for i in range(1, num_of_enemies + 1):
    enemies_loc[i] = {
        'X': random.randint(0, 736),
        'Y': random.randint(0, 3) * 64,
        'X_change': 3
    }
enemyY_change = 64

# Bullet
bullet_img = pygame.image.load('laser.png')
bulletX = 0
bulletY = 480
bulletY_change = 16
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('Player1UpBoldItalic-K9Xp.ttf', 24)
textX = 10
textY = 10

# Game over
game_over_f = pygame.font.Font('Player1Up3DRegular-81Jz.ttf', 48)


# FUNCTIONS
def player(x, y):
    """This function plots a player on the screen."""
    screen.blit(player_img, (x, y))


def enemies(x, y):
    """This function plots enemies on the screen."""
    screen.blit(enemy_img, (x, y))


def bullet(x, y):
    """This function plots a bullet on the screen and changes its state."""
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collided(x0, y0, x1, y1):
    """
    This functions returns True if the Euclidean distance between two objects is less
    than 27 pixels, otherwise it returns False.
    :param int x0: X coordinate of the first object
    :param int y0: Y coordinate of the first object
    :param int x1: X coordinate of the second object
    :param int y1: Y coordinate of the second object
    :return: True if collided, False if not
    """
    distance = math.dist([x0, y0], [x1, y1])
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    """This function makes the score to show on the screen."""
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    """This function makes the Game over text to show when called."""
    end = game_over_f.render('GAME OVER', True, (255, 0, 0))
    screen.blit(end, (200, 250))


# GAME LOOP
running = True
while running:
    # plot background pic
    screen.blit(background, (0, 0))

    # looping through pygame events list
    for event in pygame.event.get():
        # checking if "close" button was pressed
        if event.type == pygame.QUIT:
            running = False

        # checking if the following keys were pressed.
        if event.type == pygame.KEYDOWN:
            # player movement
            if event.key == pygame.K_LEFT:
                playerX_change += -10
            if event.key == pygame.K_RIGHT:
                playerX_change += 10
            # shooting a bullet
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)
        # checking if the key was released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player movement
    playerX += playerX_change

    # creating a border for the player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemies appearance
    for i in range(1, num_of_enemies + 1):

        # Game over condition
        if enemies_loc[i]['Y'] >= 420:
            for j in range(1, num_of_enemies + 1):
                enemies_loc[j].update(Y=2000)
            game_over()
            break

        # enemies movement
        enemies_loc[i]['X'] += enemies_loc[i]['X_change']

        if enemies_loc[i]['X'] >= 736:
            enemies_loc[i].update(X_change=-3)
            enemies_loc[i]['Y'] += enemyY_change
        elif enemies_loc[i]['X'] <= 0:
            enemies_loc[i].update(X_change=3)
            enemies_loc[i]['Y'] += enemyY_change

        # collision condition
        collision = is_collided(enemies_loc[i]['X'], enemies_loc[i]['Y'],
                                bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = 'ready'

            score_value += 1
            enemies_loc[i].update(X=random.randint(0, 736))
            enemies_loc[i].update(Y=random.randint(0, 3) * 64)

        # calling the enemies function
        enemies(enemies_loc[i]['X'], enemies_loc[i]['Y'])

    # movement of a bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # calling the player function
    player(playerX, playerY)
    # score
    show_score(textX, textY)

    pygame.display.update()
