import pygame
from sys import exit 

# Creating Pygame Window
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption ("Jumper") # Title
clock = pygame.time.Clock()

# Game State
game_state = False 

# Font
font = pygame.font.Font('Fonts/COMIC.TTF', 35)
title = font.render('Avoid the Hazards', False, 'black')
title_rect = title.get_rect(center = (400, 25))

intro = font.render('Press Space to Begin', False, "black")
intro_rect = intro.get_rect(center=(400, 100))
instruc_one = font.render("'d' Key to move Forward", False, "Black")
instruc_one_rect = instruc_one.get_rect(center=(400, 250))
instruc_two = font.render("'spacebar' Key to Jump", False, "black")
instruc_two_rect = instruc_two.get_rect(center=(400, 300))


# Background
sky = pygame.image.load('Graphic Images/Sky.png').convert()
ground = pygame.image.load('Graphic Images/ground.png').convert()
switch = 0

# Snail
ground_enemy_v1 = pygame.image.load('Graphic Images/snail/snail1.png').convert_alpha()
ground_enemy_v2 = pygame.image.load('Graphic Images/snail/snail2.png').convert_alpha()
snails = [ground_enemy_v1, ground_enemy_v2]
# Rectangle (Share one rectangle, since both screens are the same dimensions)
ground_rect = ground_enemy_v1.get_rect(bottomright=(750, 300))


# Fly
aerial_enemy_v1 = pygame.image.load('Graphic Images/fly/Fly1.png').convert_alpha()
aerial_enemy_v2 = pygame.image.load('Graphic Images/fly/Fly2.png').convert_alpha()
flys = [aerial_enemy_v1, aerial_enemy_v2]
# Rectangle (Share one rectangle, since both screens are the same dimensions)
aerial_rect = aerial_enemy_v1.get_rect(bottomright=(750, 150))


# Player (Character)
char_walking_v1 = pygame.image.load('Graphic Images/player/player_walk1.png').convert_alpha()
char_walking_v2 = pygame.image.load('Graphic Images/player/player_walk2.png').convert_alpha()
players = [char_walking_v1, char_walking_v2]
# Rectangle (Share one rectangle, since all screens are the same dimension)
char_rect = char_walking_v1.get_rect(bottomright=(50, 300))
# Physics of our Game
char_gravity = 0

move = 0 # Used for Player Animation 

# Main Loop
while True:
    for event in pygame.event.get():
        # Quiting the Game/Program 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_state: # Space button to start the game 
            game_state = True
            # Reseting all sprites to orginal position 
            ground_rect.left = 800
            aerial_rect.left = 800
            char_rect.right = 100

    if game_state: # Game is being Played
        # Displaying the Background
        screen.blit (sky, (0, 0))
        screen.blit (ground, (0, 300))
        # Displaying/Updating the Hazards (Snail, Fly)
        screen.blit(snails[switch], ground_rect)
        screen.blit(flys[switch], aerial_rect)
        # Displaying the Character
        screen.blit(players[switch], char_rect)
        # Displaying the Font
        screen.blit(title, title_rect)
    
        # Movements
        ground_rect.x -= 1 # Snail Move
        aerial_rect.x -= 4 # Fly move 
        # User Keyboard Movements
        keys = pygame.key.get_pressed() # Collects data on keys
        # Forward
        if keys[pygame.K_d]: # if 'd' is pressed 
            char_rect.x += 8
        # Jumping
        if keys[pygame.K_SPACE] and char_rect.bottom == 300: # Space bar
            char_gravity += -15
    
    
        # Gravity
        char_rect.bottom += char_gravity
        if char_rect.bottom < 300: # if the player is in the air
            char_gravity += 1 
        else: # if the player is on the ground
            char_gravity = 0 # Gravity is reseted
    
        # Collisions
        if char_rect.colliderect(ground_rect) or char_rect.colliderect(aerial_rect):
            game_state = False # Game Over

      
        # Creating an Infinite Loop (Make sures that the hazards reappear on the screen after exiting through the left side)
        if ground_rect.right < 0: # Snail
            ground_rect.left = 800
        if aerial_rect.right < 0: # Fly
            aerial_rect.left = 800
        if char_rect.left > 800: # Character (Left Side)
            char_rect.right = 0
        elif char_rect.right < 0: # Character (Right Side)
            char_rect.left = 800
        # Making the Screens animate (Switching between each screen)
        if move == 10:
            switch = 0 if switch == 1 else 1
            move = 0
        move += 1
      
    else: # Intro/Outro Screen
        screen.fill("white")
        screen.blit(intro, intro_rect)
        screen.blit(instruc_one, instruc_one_rect)
        screen.blit(instruc_two, instruc_two_rect)
       
    pygame.display.update()
    clock.tick(60)