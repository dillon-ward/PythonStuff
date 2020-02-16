import os
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
    image = ""

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

        # Set the first frame for the player at the start
        self.image = self.image_frames_r[0]

    def calc_grav(self):
        """ Calculate effect of gravity. """

        # Checks if gravity acts upon the player
        grounded = False
        if self.change_y == 0:
            self.change_y = 1 # Speed at which the player falls
        else:
            self.change_y += .35 # Reduces the speed of the player when they jump

        # Checks if the player is on the ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0 # Y-coordinate doesn't change when player is grounded
            grounded = True 

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

    def jump(self):
        """ Called when user hits 'jump' button. """

        # Checks when player hits a platform
        self.rect.y += 2 # Moves down by two pixels to check
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2 # Moves back up to realign the player

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -9 # Player goes up by 9 pixels
            
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6 # Player goes left by 6
        self.dir = -1 # Direction turns left

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6 # Player goes right by 6
        self.dir = 1 # Direction turns right

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
        
    # --- Plays sprites animation
    # Plays idle animation
    # From either left or right frames depending on direction
    def anim_idle(self, idle_count):
        if (self.dir == 1):
            self.image = self.image_frames_r[idle_count]
        else:
            self.image = self.image_frames_l[idle_count]

    # Plays jump animation
    def anim_jump(self, jump_count):
        if (self.dir == 1):
            self.image = self.image_frames_r[jump_count]
        else:
            self.image = self.image_frames_l[jump_count]

    # Plays startup move animation
    def anim_move(self, move_count):
        if (self.dir == 1):
            self.image = self.image_frames_r[move_count]
        else:
            self.image = self.image_frames_l[move_count]
                
# Create the platform Class
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        
        super().__init__()

        # Create a block for the platforms
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()

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

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(GREY)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)

    def shift_world(self, shift_y):
        """ When the user moves up/down and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_y

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.y += shift_y
