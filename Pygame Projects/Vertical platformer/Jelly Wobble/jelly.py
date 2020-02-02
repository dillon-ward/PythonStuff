
import pygame
pygame.init()
BLACK=(0,0,0)
WHITE=(255,255,255)
SCREEN_HEIGHT=500
SCREEN_WIDTH=700
#The following class is used to load images from a sprite sheet.
#A sprite sheet is one large image that contains all the separate images that we need
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

        # Assuming black works as the transparent color
        image.set_colorkey(WHITE)

        # Return the image
        return image

#Create the Class for the player object, called Jelly
class Jelly(pygame.sprite.Sprite):
    change_x=0
    change_y=0
    image_frames=[]#The object will be animated.  This list holds all the images for this
    image=""
    def __init__(self):
        super().__init__()
        spritesheet=SpriteSheet("drops.png")
        #Add all the images from the sprite sheet
        image=spritesheet.get_image(0,0,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(37,0,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(74,0,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(111,0,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(0,47,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(37,47,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(74,47,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(111,47,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(0,94,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(37,94,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(74,94,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(111,94,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(0,141,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(37,141,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(74,141,37,47)
        self.image_frames.append(image)
        image=spritesheet.get_image(111,141,37,47)
        self.image_frames.append(image)
        #set the first image
        self.image=self.image_frames[0]
        self.rect=self.image.get_rect()

    def update(self):
        self.rect.x+=self.change_x
        self.rect.y+=self.change_y
        pos=self.rect.x
        frame=(pos//30)%len(self.image_frames)
        self.image=self.image_frames[frame]

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

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
        
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
        
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

screen=pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Jelly wobble")
sprites_list=pygame.sprite.Group()
jelly=Jelly()
sprites_list.add(jelly)
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                jelly.go_left()
            if event.key==pygame.K_RIGHT:
                jelly.go_right()
            if event.key==pygame.K_SPACE:
                jelly.jump()
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT:
                jelly.stop()
            if event.key==pygame.K_RIGHT:
                jelly.stop()
    screen.fill(WHITE)
    jelly.calc_grav()
    jelly.update()
    sprites_list.draw(screen)
    clock.tick(60)
    pygame.display.flip()
    
pygame.quit()
