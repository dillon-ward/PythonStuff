import pygame
from platformer_presets import *

# The following class is used to load images from a sprite sheet.
# A sprite sheet is one large image that contains all the separate images that we need
class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
    
    # This points to our sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Return the image
        return image
    
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
    image_frames = []
    image = ""
    def __init__(self):
        """ Constructor function """

        super().__init__()
        spritesheet = SpriteSheet("Images/cloud_spritesheet.png")

        # Add all the images from the sprite sheet
        image=spritesheet.get_image(0,0,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(300,0,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(600,0,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(900,0,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(0,300,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(300,300,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(600,300,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(900,300,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(0,600,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(300,600,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(600,600,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(900,600,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(0,900,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(300,900,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(600,900,300,300)
        self.image_frames.append(image)
        image=spritesheet.get_image(900,900,300,300)
        self.image_frames.append(image)

        # Set the first image
        self.image = self.image_frames[0]
        self.rect = self.image.get_rect()
        
        # Create an image of the block, and fill it with a color.
        # We could of course replace this with a bitmap
        width = 37
        height = 47
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

        # Position the images on the player
        pos = self.rect.x
        frame=(pos//30)%len(self.image_frames)
        self.image = self.image_frames[frame]
        
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
