import pygame

# Define some colors and sprites
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

def drawStickFigure(screen, x, y):
    # Head
    pygame.draw.ellipse(screen, BLACK, [1 + x, y, 10, 10], 0)
    # Legs
    pygame.draw.line(screen, BLACK, [5 + x, 17 + y], [10 + x, 27 + y], 2)
    pygame.draw.line(screen, BLACK, [5 + x, 17 + y], [x, 27 + y], 2)
    # Body
    pygame.draw.line(screen, RED, [5 + x, 17 + y], [5 + x, 7 + y], 2)
    # Arms
    pygame.draw.line(screen, RED, [5 + x, 7 + y], [9 + x, 17 + y], 2)
    pygame.draw.line(screen, RED, [5 + x, 7 + y], [1 + x, 17 + y], 2)
    
pygame.init()

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

pygame.mouse.set_visible(False)

# Speed in pixels per frame
x_speed = 0
y_speed = 0

# Current position
x_coord = 10
y_coord = 10

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        # User presses a key
        if event.type == pygame.KEYDOWN:
            # If key pressed is an arrow key, the speed is adjusted
            if event.key == pygame.K_LEFT:
                x_speed = -3
            if event.key == pygame.K_RIGHT:
                x_speed = 3
            if event.key == pygame.K_UP:
                y_speed = -3
            if event.key == pygame.K_DOWN:
                y_speed = 3
        # User lets go of key
        if event.type == pygame.KEYUP:
            # If key is an arrow key, vector is set to zero
            if event.key == pygame.K_LEFT or event.key ==  pygame.K_RIGHT:
                x_speed = 0
            if event.key == pygame.K_UP or event.key ==  pygame.K_DOWN:
                y_speed = 0
            
    # --- Game logic should go here
    pos = pygame.mouse.get_pos()
    x = pos[0]
    y = pos[1]
    
    x_coord += x_speed
    y_coord += y_speed

    if x_coord < 25:
        x_coord = 25
    if x_coord > 675:
        x_coord = 675
    if y_coord < 0:
        y_coord = 0
    if y_coord > 475:
        y_coord = 475

    # --- Drawing code should go here

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    
    drawStickFigure(screen, x_coord, y_coord)
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

