#Demonstrates basic Platforms
from platformer_classes import *

# Define some music
cave_theme = pygame.mixer.Sound(os.path.join(dirname, "Music/cave_theme.ogg"))

# Assign font for text
pygame.font.init()
level_font = pygame.font.SysFont('Comic Sans MS', 30)

# Checks animation frames
anim_idle_check = False
anim_jump_check = False
anim_move_check = False
time = 0

# Frame check for idle animation
idle_count = 0
idle_check = False

# Frame check for jump animation
jump_count = 4
jump_check = False

# Frame check for move animation
move_count = 8
move_check = False

# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_name = 'Level 1'

        # Set the level's platforms to the stone platform image
        pixel_platform = SpriteSheet(os.path.join(dirname, "Images/platform_stone.png"))

        # Cut out the platform from the image
        platform_image = pixel_platform.get_image(37, 113, 271-37, 149-113)

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
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            pygame.transform.scale(platform_image, (platform[0], platform[1]), block.image)
            self.platform_list.add(block)
            
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 2. """

        Level.__init__(self, player)

        self.level_name = 'Level 2'

        pixel_platform = SpriteSheet(os.path.join(dirname,"Images/platform_stone.png"))

        image = pixel_platform.get_image(37, 113, 271-37, 149-113)

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
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            pygame.transform.scale(image, (platform[0], platform[1]), block.image)
            self.platform_list.add(block)

class Level_03(Level):
    """ Definition for level 3."""

    def __init__(self, player):
        """ Create level 3."""

    # Call the parent constructor
        Level.__init__(self, player)

        self.level_name = 'Level 3'

        # Set the level's platforms to the stone platform image
        pixel_platform = SpriteSheet(os.path.join(dirname,"Images/platform_stone.png"))

        # Cut out the platform from the image
        image = pixel_platform.get_image(37, 113, 271-37, 149-113)

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
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            pygame.transform.scale(image, (platform[0], platform[1]), block.image)
            self.platform_list.add(block)

""" Main Program """
pygame.init()

# Set the height and width of the screen
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Platformer Jumper")

# Create the player
player = Player()

# Assign sprite list to player
sprites_list = pygame.sprite.Group()
sprites_list.add(player)

# Create all the levels
level_list = []
level_list.append(Level_01(player))
level_list.append(Level_02(player))
level_list.append(Level_03(player))

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
    time += 1
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
                move_check = True
                jump_check = False
                idle_check = False
            if event.key == pygame.K_RIGHT:
                player.go_right()
                move_check = True
                jump_check = False
                idle_check = False
            if event.key == pygame.K_UP:
                player.jump()
                jump_check = True
                move_check = False
                idle_check = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.change_x < 0:
                player.stop()
                idle_check = True
            if event.key == pygame.K_RIGHT and player.change_x > 0:
                player.stop()
                idle_check = True
            move_check = False

    # --- Calculate animation frames
    # Calculates when idle animation will play
    if time % 30 == 0:
        anim_idle_check = True
    else:
        anim_idle_check = False

    # Calculates when jump animation will play
    if time % 6 == 0:
        anim_jump_check = True
    else:
        anim_jump_check = False

    # Calculates when move animation will play
    if time % 8 == 0:
        anim_move_check = True
    else:
        anim_move_check = False

    # --- Checks if animation will play
    # Checks if the idle animation will play
    if idle_check:
        if anim_idle_check:
            player.anim_idle(idle_count)
            if idle_count == 3:
                idle_count = 0
            else:
                idle_count += 1
    else:
        idle_count = 0

    # Checks if the jump animation will play
    if jump_check:
        if anim_jump_check:
            player.anim_jump(jump_count)
            if jump_count == 7:
                jump_count = 7
            else:
                jump_count += 1
    else:
        jump_count = 4

    # Checks if the move animation will play
    if move_check:
        if anim_move_check:
            player.anim_move(move_count)
            if move_count == 15:
                move_count = 12
            else:
                move_count += 1
    else:
        move_count = 8
    
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

    if player.rect.x < -25:
        player.rect.x = SCREEN_WIDTH - 90

    if player.rect.x > SCREEN_WIDTH - 90:
        player.rect.x = -25

    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    current_level.draw(screen)
    active_sprite_list.draw(screen)

    textsurface = level_font.render(current_level.level_name, False, RED)
    screen.blit(textsurface, (0, 0))

    sprites_list.draw(screen)

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Play music
    cave_theme.play()
    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
