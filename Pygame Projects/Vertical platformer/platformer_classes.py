import os
import math
from platformer_presets import *

# Gets the path of a directory
dirname = os.path.dirname(__file__)

# The following class is used to load images from a sprite sheet
# A sprite sheet is one large image that contains all the separate images that we need
class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
    
    # This points to our sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha() # This gives the image an alpha channel

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([width, height], pygame.SRCALPHA) # The alpha channel causes the background to be clear

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Return the image
        return image
    
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
    image_frames_r = [] # Frames of images facing right
    image_frames_l = [] # Frames of images facing left
    image = ''

    def __init__(self):
        """ Constructor function """

        super().__init__()
        # Imports the spritesheet of the play
        spritesheet = SpriteSheet(os.path.join(dirname,"Images/cloud_spritesheet.png"))

        # Frames fom the player sprite sheet are initially all facing right
        # Add all the images from the sprite sheet to the right facing image frames list
        image=spritesheet.get_image(100,120,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(400,120,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(700,120,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(1000,120,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(100,420,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(400,420,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(700,420,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(1000,420,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(100,720,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(400,720,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(700,720,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(1000,720,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(100,1020,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(400,1020,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(700,1020,100,100)
        self.image_frames_r.append(image)
        image=spritesheet.get_image(1000,1020,100,100)
        self.image_frames_r.append(image)
        
        # Flips the images in the right frames list to face left
        # Which are then stored in the left frames list
        for i in self.image_frames_r:
            self.image_frames_l.append(pygame.transform.flip(i, True, False)) # True for horizontal flip

        # Create a block of the player
        width = 100
        height = 60
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()

        # Assigns the direction of the player
        self.dir = 1 # 1 is right

        # Used as the change in distance of the player
        self.change_x = 0
        self.change_y = 0

        # Set animation timer to zero
        self.time = 0

        # Frame number for move animation
        self.move_count = 8

        # Frame number for idle animation
        self.idle_count = 0

        # Frame number for jump animation
        self.jump_count = 4

        # Set the first frame for the player at the start
        self.image = self.image_frames_r[0]

    def calc_grav(self):
        """ Calculate effect of gravity. """

        # Checks if gravity acts upon the player
        if self.change_y == 0:
            self.change_y = 1 # Speed at which the player falls
        else:
            self.change_y += .35 # Reduces the speed of the player when they jump

        # Checks if the player is on the ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0 # Y-coordinate doesn't change when player is grounded

    def update(self):
        """ Move the player. """
        
        # Gravity method is called
        self.calc_grav()

        # Player moves horizontally
        self.rect.x += self.change_x
        
        # Checks if the player collides with an object
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Player moves vertically
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

        # If the player gets near the top, shift the world down (+y)
        if self.rect.y <= 200:
            diff = self.rect.y - 200
            self.rect.y = 200
            self.level.shift_world(-diff)

        # If the player gets near the bottom, shift the world up (-y)
        if self.rect.y >= 400:
            diff = 400 - self.rect.y
            self.rect.y = 400
            self.level.shift_world(diff)

        if self.rect.x < -25:
            self.rect.x = SCREEN_WIDTH - 90

        if self.rect.x > SCREEN_WIDTH - 90:
            self.rect.x = -25

        # Animation
        self.time = self.time + 1

        if self.change_y != 0:
            # Play jumping animation if moving vertically
            if self.time % 6 == 0:
                self.anim_jump(self.jump_count)
                if self.jump_count != 7:
                    self.jump_count += 1
            self.move_count = 8
        elif self.change_x != 0:
            # Play move animation if moving horizontally
            if self.time % 8 == 0:
                self.anim_move(self.move_count)
                if self.move_count == 15:
                    self.move_count = 12
                else:
                    self.move_count += 1
            self.jump_count = 4

        if self.change_x == 0 and self.change_y == 0:
            # Play idle animation if not moving at all
            if self.time % 30 == 0:
                self.anim_idle(self.idle_count)
                if self.idle_count == 3:
                    self.idle_count = 0
                else:
                    self.idle_count += 1
                self.move_count = 8
                self.jump_count = 4
        else:
            # Reset idle counter
            self.idle_count = 0

    def go_right(self):
        self.change_x = 6 # Player goes right by 6
        self.dir = 1 # Direction turns right

    def go_left(self):
        self.change_x = -6 # Player goes left by 6
        self.dir = -1 # Direction turns left

    def jump(self):
        """ Called when user hits 'jump' button. """

        # Checks when player hits a platform
        self.rect.y += 2 # Moves down by two pixels to check
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2 # Moves back up to realign the player

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -9 # Player goes up by 9 pixels
            

    def stop(self):
        """ Called when the user lets go of an arrow key. """
        self.change_x = 0

    def anim_move(self, move_count):
        if self.dir == 1:
            self.image = self.image_frames_r[move_count]
        else:
            self.image = self.image_frames_l[move_count]

    def anim_jump(self, jump_count):
        if self.dir == 1:
            self.image = self.image_frames_r[jump_count]
        else:
            self.image = self.image_frames_l[jump_count]

    def anim_idle(self, idle_count):
        if self.dir == 1:
            self.image = self.image_frames_r[idle_count]
        else:
            self.image = self.image_frames_l[idle_count]

# Create the platform Class
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    image = None

    def __init__(self, width, height, x, y):
        
        super().__init__()

        if Platform.image == None:
            # Set the level's platforms to the stone platform image
            pixel_platform = SpriteSheet(os.path.join(dirname, "Images/platform_stone.png"))

            # Cut out the platform from the image
            Platform.image = pixel_platform.get_image(37, 113, 271-37, 149-113)

        # Create a block for the platforms
        self.image = pygame.Surface([width, height])

        # Create surface scaled for platform height
        # Calculates how many pixels wide the scaled up image needs to be to maintain the aspect ratio
        scale_width = int((height / Platform.image.get_height()) * Platform.image.get_width())
        # Create a surface to take the scaled up image
        scale_surface = pygame.Surface([scale_width, height])
        # Scale the image up
        pygame.transform.scale(Platform.image, (scale_width, height), scale_surface)

        # Calculate number of pixels in the scaled up image for 10 source pixels
        lr_width = (height / Platform.image.get_height()) * 10
        # Calculate the minumum number of pixels
        lr_width_min = int(math.floor(lr_width))
        # Calculate the maximum number of pixels
        lr_width_max = int(math.ceil(lr_width))

        # self.image.fill(RED)

        # Draw the leftmost 10 pixels (scaled up minimum) in to the destination surface
        self.image.blit(scale_surface, (0, 0), (0, 0, lr_width_min, height))
        # Draw the rightmost 10 pixels (scaled up minimum) in to the destination surface
        self.image.blit(scale_surface, (width - lr_width_min, 0), (scale_width - lr_width_min, 0, lr_width_min, height))

        # Calculate number of pixels left to draw in the platform
        width_left = width - (lr_width_min * 2)
        # Calculate the x position to draw the next segment at
        out_left = lr_width_min
        # Calculate the number of source pixels to use for the middle (using the max scaled pixels)
        inner_width = scale_width - (lr_width_max * 2)
        # Draw the middle tiles
        while width_left > 0:
            # Calculate how much to draw
            blit_width = min(width_left, inner_width)
            # Draw the segment
            self.image.blit(scale_surface, (out_left, 0), (lr_width_max, 0, blit_width, height))
            # Increase x position by the amount we drew
            out_left += blit_width
            # Decrease the amount to draw by how much we drew
            width_left -= blit_width

        # Set self rectangle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    # Lists of sprites used in all levels
    platform_list = None
    background = None
    # How far this world has been scrolled up/down
    world_shift = 0

    def __init__(self, player):
        
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.player = player

        # Create background surface
        stone_background = SpriteSheet(os.path.join(dirname,"Images/stone_background.png"))
        background_img = stone_background.get_image(0, 0, 480, 480)
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_WIDTH * 2))
        background_tile = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_WIDTH))
        self.background.blit(background_tile, [0, 0])
        self.background.blit(background_tile, [0, SCREEN_WIDTH])

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Load and draw background
        screen.blit(self.background, [0, -(SCREEN_WIDTH / 2) + self.world_shift])

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)

    def shift_world(self, shift_y):
        """ When the user moves up/down and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_y

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.y += shift_y
