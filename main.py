import pygame
from sys import exit

pygame.init()
pygame.display.set_caption("Flappy Bird")
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# Font
font = pygame.font.Font('COMIC.TTF', 35)
mp_title = font.render("Trashy Bird", False, "white") # Main Page Title
mp_title_rect = mp_title.get_rect (center=(400, 50))
mp_instruc = font.render ("Press 'SPACE' to Begin", False, "white") # Main Page Instruction
mp_instruc_rect = mp_instruc.get_rect (center=(400, 150))

# Background
background = pygame.image.load("FlappyBackground.png").convert() # For Game

# Bird
bird = pygame.image.load("TrashyBird.png").convert_alpha()
bird_rect = bird.get_rect(center=(150, 200))

# Obstacles
top_pipe = pygame.image.load('TopPipe.png').convert_alpha()
bottom_pipe = pygame.image.load('BottomPipe.png').convert_alpha()
# First Set of Pipes
top_pipe_rect_1 = top_pipe.get_rect(bottomleft=(600, 100))
bottom_pipe_rect_1 = bottom_pipe.get_rect(topleft=(600, 300))
# Second Set of Pipes
top_pipe_rect_2 = top_pipe.get_rect(bottomleft=(900, 50))
bottom_pipe_rect_2 = bottom_pipe.get_rect(topleft=(900, 250))
# Thrid Set of Pipes
top_pipe_rect_3 = top_pipe.get_rect(bottomleft=(1200, 175))
bottom_pipe_rect_3 = bottom_pipe.get_rect(topleft=(1200, 375))

# Data Set to hold the Pipe variables (Used for Pipe Movement and Collisions)
top_pipes = [top_pipe_rect_1, top_pipe_rect_2, top_pipe_rect_3]
bottom_pipes = [bottom_pipe_rect_1, bottom_pipe_rect_2, bottom_pipe_rect_3]

# Movements
gravity = 0
# Switch
game_state = False

# Heart of the Code
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if not game_state and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # To Begin the Game
            game_state = True 
          
        if game_state and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Make the Bird Fly 
            gravity = -11
          
    # Displaying
    screen.blit(background, (0,0)) # Background
    screen.blit(bird, bird_rect) # Bird
    screen.blit(top_pipe, top_pipe_rect_1) # Top Pipe
    screen.blit(bottom_pipe, bottom_pipe_rect_1) # Bottom Pipe
  
    if not game_state: # Play/Play Again Screen
        screen.blit(mp_title, mp_title_rect)
        screen.blit(mp_instruc, mp_instruc_rect)
        # Reseting 
        bird_rect.centery = 200 # Bird's position
        top_pipes[0].left = 600 # Pipe One
        bottom_pipes[0].left = 600
        top_pipes[1].left = 900 # Pipe Two
        bottom_pipes[1].left = 900
        top_pipes[2].left = 1200 # Pipe Three
        bottom_pipes[2].left = 1200
          
    elif game_state: # Actual Game
        # Gravity 
        bird_rect.y += gravity
        gravity += 1
    
        # Boundaries 
        if bird_rect.bottom > 400 or bird_rect.top < 0:
            game_state = False # Game Over

        # Pipe Movement
        for i in range(len(top_pipes)):
            # Top
            if top_pipes[i].right < 0:
                top_pipes[i].left = 800 # Reseting back to Original Position 
            else:
                top_pipes[i].x -= 1

            # Bottom 
            if bottom_pipes[i].right < 0:
                bottom_pipes[i].left = 800 # Reseting back to Original Position 
            else:
                bottom_pipes[i].x -= 1

            # Pipe Collisions
            if bird_rect.colliderect(top_pipes[i]) or bird_rect.colliderect(bottom_pipes[i]): # IF the the bird hits the top or bottom pipe
                game_state = False # Game Over

            # Displaying Pipes
            screen.blit(top_pipe, top_pipes[i])
            screen.blit(bottom_pipe, bottom_pipes[i])

    pygame.display.update()
    clock.tick(60)