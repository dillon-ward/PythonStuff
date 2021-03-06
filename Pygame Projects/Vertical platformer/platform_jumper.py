#Demonstrates basic Platforms
from platformer_classes import *

# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_name = 'Level 1'

        # Array with width, height, x, and y of platforms
        level = [[210, 20, 400, 100],
                 [210, 20, 150, 180],
                 [210, 20, 350, 250],
                 [210, 20,   0, 300],
                 [210, 20, 600, 300],
                 [210, 20, 200, 400],
                 [210, 20, 500, 500],
                 [210, 20, -10, 520],
                 [800, 20,   0, 600]
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], platform[2], platform[3])
            self.platform_list.add(block)
            
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 2. """

        Level.__init__(self, player)

        self.level_name = 'Level 2'

        level = [[210, 20, 300, 100],
                 [210, 20, 550, 195],
                 [210, 20,  10, 300],
                 [210, 20, 450, 375],
                 [210, 20, 210, 450],
                 [210, 20,  50, 550],
                 [210, 20, 500, 650],
                 [210, 20,  50, 700],
                 [800, 20,   0, 800]
                ]   

        for platform in level:
            block = Platform(platform[0], platform[1], platform[2], platform[3])
            self.platform_list.add(block)

class Level_03(Level):
    """ Definition for level 3."""

    def __init__(self, player):
        """ Create level 3."""

    # Call the parent constructor
        Level.__init__(self, player)

        self.level_name = 'Level 3'

        level = [[210, 20,  10, 100],
                 [210, 20, 550, 200],
                 [210, 20,  10, 300],
                 [210, 20, 550, 400],
                 [210, 20,  10, 500],
                 [210, 20, 550, 600],
                 [210, 20,  10, 700],
                 [800, 20,   0, 800]
                ]

        for platform in level:
            block = Platform(platform[0], platform[1], platform[2], platform[3])
            self.platform_list.add(block)

""" Main Program """
# Initialise pygame
pygame.init()

# Define some background music
cave_theme = pygame.mixer.Sound(os.path.join(dirname, "Music/cave_theme.wav"))

# Assign font for text
pygame.font.init()
level_font = pygame.font.SysFont('Comic Sans MS', 30)

# Set the height and width of the screen
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

# Set window title
pygame.display.set_caption("Platformer Jumper")

# Create the player
player = Player()

# Create all the levels
level_list = []
level_list.append(Level_01(player))
level_list.append(Level_02(player))
level_list.append(Level_03(player))

# Set the current level
current_level_no = 0
current_level = level_list[current_level_no]
player.level = current_level

# Creates an active sprite list and adds player to it
active_sprite_list = pygame.sprite.Group()
active_sprite_list.add(player)

# Set starting position for the player
player.rect.x = 340
player.rect.y = SCREEN_HEIGHT - player.rect.height

# Creates a clock for game timing
clock = pygame.time.Clock()

# Play background music on a loop
cave_theme.play(-1)

# -------- Main Program Loop -----------
done = False

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

    # If player goes to the top, start at the bottom of the next level
    current_position = player.rect.y - current_level.world_shift
    if current_position < -50:
        player.rect.y = SCREEN_HEIGHT
        if current_level_no < len(level_list) -1:
            current_level_no += 1

    current_level = level_list[current_level_no]
    player.level = current_level

    # Update items in the level
    current_level.update()

    # Draw the level
    current_level.draw(screen)

    # Draw the active sprites
    active_sprite_list.draw(screen)

    # Draw the level name
    textsurface = level_font.render(current_level.level_name, False, RED)
    screen.blit(textsurface, (0, 0))
    
    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
