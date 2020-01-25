#Demonstrates basic Platforms

import pygame

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)


SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """

    
    def __init__(self):
        """ Constructor function """

        super().__init__()

        # Create an image of the block, and fill it with a color.
        # We could of course replace this with a bitmap
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        
        self.change_x = 0
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None


    def update(self):
        """ Move the player. """
        
        self.calc_grav()

        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -9
            
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

#Create the platform Class.  This uses simple block but we could have used
#bitmaps from a sprite sheet.
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    # Lists of sprites used in all levels. Add or remove
    # lists as needed for your code.
    platform_list = None
    enemy_list = None
    background = None

    # How far this world has been scrolled up/down
    world_shift = 0

    def __init__(self, player):
        
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(BLUE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_y):
        """ When the user moves up/down and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_y

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.y += shift_y

        for enemy in self.enemy_list:
            enemy.rect.y += shift_y


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

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
    else:
        # If player falls to the bottom, start at the top of the last level
        current_position = player.rect.y + current_level.world_shift
        if player.rect.y > 500:
            player.rect.y = 0
            current_level_no -= 1

    current_level = level_list[current_level_no]
    player.level = current_level

    if player.rect.x < 0:
        player.rect.x = SCREEN_WIDTH

    if player.rect.x > SCREEN_WIDTH:
        player.rect.x = 0

    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    current_level.draw(screen)
    active_sprite_list.draw(screen)

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()

