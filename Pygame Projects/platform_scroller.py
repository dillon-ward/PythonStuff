#This introduces the ability to scrool the world sideways
import pygame

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """

    def __init__(self):
        """ Constructor function """

        super().__init__()

        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

        self.level = None

    def update(self):
        """ Move the player. """
        
        self.calc_grav()

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
               
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    
    platform_list = None
    enemy_list = None

    # How far this world has been scrolled left/right
    world_shift = 0

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        screen.fill(BLUE)

        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        Level.__init__(self, player)

        self.level_limit = -1000

        level = [[210, 70, 500, 500],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        Level.__init__(self, player)

        self.level_limit = -1000

        level = [[210, 30, 450, 570],
                 [210, 30, 850, 420],
                 [210, 30, 1000, 520],
                 [210, 30, 1120, 280],
                 ]

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


""" Main Program """
pygame.init()

size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Side-scrolling Platformer")

# Create the player
player = Player()

# Create all the levels
level_list = []
level_list.append(Level_01(player))
level_list.append(Level_02(player))

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
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True 

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
    
    # If the player gets near the right side, shift the world left (-x)
    if player.rect.right >= 500:
        diff = player.rect.right - 500
        player.rect.right = 500
        current_level.shift_world(-diff)

    # If the player gets near the left side, shift the world right (+x)
    if player.rect.left <= 120:
        diff = 120 - player.rect.left
        player.rect.left = 120
        current_level.shift_world(diff)

    # If the player gets to the end of the level, go to the next level
    current_position = player.rect.x + current_level.world_shift
    if current_position < current_level.level_limit:
        player.rect.x = 120
        if current_level_no < len(level_list)-1:
            current_level_no += 1
            current_level = level_list[current_level_no]
            player.level = current_level

    current_level.draw(screen)
    active_sprite_list.draw(screen)

    clock.tick(60)

    pygame.display.flip()

pygame.quit()

