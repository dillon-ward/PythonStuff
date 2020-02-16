import pygame
from pygame import *
import os
import random

pygame.init()

# Initialise basic colours
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
WHITE = (255, 255, 255)

# Set the size of the screen
size = (800, 1000)
screen = pygame.display.set_mode(size)

# Set frame count
frameCount = 0

# Show the title of the game
pygame.display.set_caption("Star Wars Invaders")

# Get directory of the currently running program for all images
dirname = os.path.dirname(__file__)

# --- Player assets
# Load imgage of player's sprite and lives
spaceship = pygame.image.load(os.path.join(dirname, "Images/millenium_falcon.png"))
life = transform.scale(spaceship, (64, 64))
lives = 3

# Speed in pixels per frame of spaceship
x_speed = 0
y_speed = 0

# Current position of spaceship
x_coord = 400
y_coord = 850

# Define some audio
player_laser_sound = pygame.mixer.Sound(os.path.join(dirname, "Sound/laser5.ogg"))

# Define class bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 10

pygame.init()

# Define bullet list
bullet_list = pygame.sprite.Group()

# Allow bullet to fire
bulletFire = True

# ---

# --- Invader assets
# Load image of invader
invader = pygame.image.load(os.path.join(dirname, "Images/TIE_fighter.png"))

# Allign invaders across screen
def setUpInvaders():
    invaderList = []

    # y coord for first row of invaders
    y = 50

    # Two constants for number of rows
    # and numbers of invaders per row
    num_rows = 5
    num_invaders_per_row = 6

    # This while loop tells me how many invaders I want
    # by taking the height of the invader
    # and multiplying them by the number of rows
    while y <= 100 * num_rows:

        # x coord for first column of invaders
        x = 50

        # The width of the invader is multiplied by the
        # number of invaders per row to get the length
        # of the row
        while x <= 100 * num_invaders_per_row:
            invaderList.append(Rect(x, y, 76, 50))
            x += 80
        y += 100

    return invaderList

# Draw invaders on screen
def drawInvaders(invaderList, screen):
    for i in invaderList:
        screen.blit(invader, i)

# Set up invaders
invaderList = setUpInvaders()

# Set up enemy detection
enemy_detection = setUpInvaders()
for d in enemy_detection:
    d.move_ip(0, -100)

detect_down = False

# TODO move enemy_detection along with invaderList

# Check if enemy can fire
noFireList = []

# Assign speed to invaders
invaderSpeed = 20

# Set up enemy bullets
enemyBullets = []
probFire = 0.001 # Controls how often an enemy will fire
maxEnemyBullets = 8 # Limits bullets so they don't fill the screen

# ---

# List of explosions
explosions = ["explosion1.png","explosion2.png",
        "explosion3.png","explosion4.png","explosion5.png",
        "explosion6.png","explosion7.png","explosion8.png","explosion9.png"]

# Set explosions to none
explode = False
explode_count = 0

# Loop until user clicks the close button
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Don't show mouse on screen
pygame.mouse.set_visible(False)

# -------- Main Program Loop -----------
while not done:
    
    starList = []
    
    for i in range (50):
        x = random.randint(0, 800)
        y = random.randint(0, 1000)
        starList.append([x, y])
        
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        # User presses a key
        if event.type == pygame.KEYDOWN:
            # If key pressed is an arrow key, the speed is adjusted
            if event.key == pygame.K_LEFT:
                x_speed = -5
            if event.key == pygame.K_RIGHT:
                x_speed = 5
            # If user pessed spacebar, a laser is fired
            if event.key == pygame.K_SPACE and bulletFire:
                bullet = Bullet()
                player_laser_sound.play()
                bullet_position = (x_coord + 38, y_coord)
                x = bullet_position[0]
                y = bullet_position[1]
                bullet.rect.x = x + 50
                bullet.rect.y = y + 3
                bullet_list.add(bullet)
                bulletFire = False
        # User lets go of key
        if event.type == pygame.KEYUP:
            # If key is an arrow key, vector is set to zero
            # If the key that went up was going in its direction
            if event.key == pygame.K_LEFT and x_speed < 0 or event.key == pygame.K_RIGHT and x_speed > 0:
                x_speed = 0

    # --- Game logic
    # Moving the spaceship and setting boundaries
    x_coord += x_speed

    if x_coord < 0:
        x_coord = 0
    if x_coord > 625:
        x_coord = 625

    player_hitbox = (x_coord + 53, y_coord + 70, 75, 65)

    # Move player bullets and detect collision

    bullet_list.update()
    for b in bullet_list:
        if b.rect.y < -10:
            bullet_list.remove(b)
            bulletFire = True
        for i in invaderList:
            if i.colliderect(b):
                invaderList.remove(i)
                bullet_list.remove(b)
                for d in enemy_detection:
                    if d.colliderect(i):
                        enemy_detection.remove(d)
                    d.move_ip(0, 100)
                    if d.colliderect(i):
                        enemy_detection.remove(d)
                    d.move_ip(0, -100)
                explode_position = (b.rect.x -30, b.rect.y -50)
                explode = True
                bulletFire = True


    # Control enemy bullet fire
    for i in invaderList:
        for d in enemy_detection:
            if i.colliderect(d):
                noFireList.append(i)

    for i in invaderList:
        if i not in noFireList:
            fireChance = random.random() # Pick a number from 0 to 1
            if fireChance <= probFire and len(enemyBullets) <= maxEnemyBullets:
                enemyBullets.append(Rect(i.x + 38, i.y + 20, 5, 20))
                noFireList = []

    # Move invader bullets and detect collision
    for b in enemyBullets:
        b.move_ip(0, 3)
        if b.colliderect(player_hitbox):
            lives -= 1
            enemyBullets.remove(b)
            if lives == 0: done = True
        if b.y > 1000:
            enemyBullets.remove(b)

    # Move invaders and detect collsion

    if frameCount >= 50:
        for i in invaderList:
            if i.right > 800 or i.left < 0:
                invaderSpeed *= -1
                detect_down = True
                for ship in invaderList:
                    ship.move_ip(0, 50)
                break

        if detect_down:
            for d in enemy_detection:
                d.move_ip(0, 50)
            detect_down = False

        for i in invaderList:
            i.move_ip(invaderSpeed, 0)
            if i.colliderect(player_hitbox): done = True

        for d in enemy_detection:
            d.move_ip(invaderSpeed,0)
    
        frameCount = 0

    frameCount += 1

    # --- Drawing code should go here

    # First, clear the screen to blck. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)

    for i in range(len(starList)):
        pygame.draw.circle(screen, WHITE, starList[i], 2)
        starList[i][1] += 1
        if starList[i][1] < 1000:
            y = random.randint(-50, -10)
            starList[i][1] = y
            x = random.randint(0, 700)
            starList[i][1] = x

    # Draw bullets
    bullet_list.draw(screen)
    for b in enemyBullets:
        draw.rect(screen, (RED), b)

    # Blit image of user sprite on screen
    screen.blit(spaceship, (x_coord, y_coord))

    # See player hitbox here:
    # pygame.draw.rect(screen, RED, (player_hitbox))

    # Blit player's lives
    count = 0
    while count < lives:
        screen.blit(life, (count * life.get_width(), 0))
        count += 1

    # Blit image of invaders on screen
    drawInvaders(invaderList, screen)

    # See invaders' hitboxs here:
    # for i in invaderList:
        # pygame.draw.rect(screen, RED, (i))

    # and enemydetection here:
    # for d in enemy_detection:
        # pygame.draw.rect(screen, GREEN, (d))

    # Load and blit images of explosions
    if explode:
        explosion = pygame.image.load(os.path.join(dirname,"Images/", explosions[explode_count]))
        screen.blit(explosion, (explode_position))
        explode_count += 1
        if explode_count == 9:
            explode_count = 0
            explode = False

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Delay to slow down invaders' animation
    time.delay(5)

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
