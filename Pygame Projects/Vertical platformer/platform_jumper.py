#Demonstrates basic Platforms

import pygame
from platformer_classes import *

# Assign font for text
pygame.font.init()
level_font = pygame.font.SysFont('Comic Sans MS', 30)

# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_name = 'Level 1'

        # Array with width, height, x, and y of platforms
        level = [[210, 20, 500, 500],
                 [210, 20, 200, 400],
                 [210, 20, 600, 300],
                 [210, 20,  75, 180],
                 [210, 20, 350, 250],
                 [210, 20,   0, 300],
                 [210, 20, 400, 100],
                 [800, 20,   0, 600],
                 [210, 20, -10, 520]
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 2. """

    # Call the parent constructor
        Level.__init__(self, player)

        self.level_name = 'Level 2'
    
    # Create and add platforms just like in level 1
        level = [[210, 20, 50, 700],
                 [800, 20,  0, 800]
                ]   

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

""" Main Program """
pygame.init()

# Set the height and width of the screen
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Platformer Jumper")

# Create the player
player = Player()

# Create all the levels
level_list = []
level_list.append(Level_01(player))
level_list.append(Level_02(player))

# Set the current level
current_level_no = 0
current_level = level_list[current_level_no]
    
active_sprite_list = pygame.sprite.Group()
player.level = current_level

player.rect.x = 340
player.rect.y = SCREEN_HEIGHT - player.rect.height
active_sprite_list.add(player)

done = False

clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            if event.key == pygame.K_RIGHT:
                player.go_right()
            if event.key == pygame.K_UP:
                player.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.change_x < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.change_x > 0:
                player.stop()

    # Update the player.
    active_sprite_list.update()

    # Update items in the level
    current_level.update()

    # If the player gets near the top, shift the world down (+y)
    if player.rect.y <= 200:
        diff = player.rect.y - 200
        player.rect.y = 200
        current_level.shift_world(-diff)

    # If the player gets near the bottom, shift the world up (-y)
    if player.rect.y >= 400:
        diff = 400 - player.rect.y
        player.rect.y = 400
        current_level.shift_world(diff)

    # If player goes to the top, start at the bottom of the next level
    current_position = player.rect.y - current_level.world_shift
    if current_position < -50:
        player.rect.y = SCREEN_HEIGHT
        if current_level_no < len(level_list) -1:
            current_level_no += 1

    current_level = level_list[current_level_no]
    player.level = current_level

    if player.rect.x < 0:
        player.rect.x = 0

    if player.rect.x > SCREEN_WIDTH - 35:
        player.rect.x = SCREEN_WIDTH - 35

    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    current_level.draw(screen)
    active_sprite_list.draw(screen)

    textsurface = level_font.render(current_level.level_name, False, RED)
    screen.blit(textsurface, (0, 0))

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()

