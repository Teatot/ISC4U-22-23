import pygame
from sys import exit 
from random import randint, choice

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Initilizes the inherited sprite class
        player_walk1 = pygame.image.load("Graphic Images/player/player_walk1.png").convert_alpha() # Imports the 1st Walking Image
        player_walk2 = pygame.image.load("Graphic Images/player/player_walk2.png").convert_alpha() # Imports the 2nd Walking Image
        self.player_walk = [player_walk1, player_walk2] # Combines both imported Images into a list
        self.player_index = 0 # An Index used for Animating 
        self.player_jump = pygame.image.load("Graphic Images/player/player_jump.png").convert_alpha() # Imports the Jumping Image

        self.image = self.player_walk[self.player_index]  # Default Image for the Player Surface
        self.rect = self.image.get_rect(midbottom=(80, 300)) # Rectangle for the Player

        self.gravity = 0 # Value for Gravity 
        self.jump_sound = pygame.mixer.Sound("audio/audio_jump.mp3") # Imports Jump Sound Effect
        self.jump_sound.set_volume(0.2)  # Modifies the Volume
      

    def animation_state(self): # Function that handles animation
        if self.rect.bottom == 300: #If the Player is on the ground
            # Walking 
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)] # int() can be also used as floor (Always Rounded Down)
        else:
            # Jumping
            self.image = self.player_jump

    def key_input (self):  # Takes in Player Input
        keys = pygame.key.get_pressed()  # Collects key data
        # Spacebar
        if keys[pygame.K_SPACE] and self.rect.bottom == 300: 
            self.gravity = -20
            self.jump_sound.play() # Plays Jumping Sound Effect

    def apply_gravity(self): # Manages the ingame gravity 
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 300: self.rect.bottom = 300 # Ensures the Player Does not fall through the floor

    def update(self):
        self.key_input()
        self.apply_gravity()
        self.animation_state()
        
# Obstacles Class
class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            aerial_enemy_v1 = pygame.image.load('Graphic Images/fly/Fly1.png').convert_alpha() # Imports fly files
            aerial_enemy_v2 = pygame.image.load('Graphic Images/fly/Fly2.png').convert_alpha()
            self.frames = [aerial_enemy_v1, aerial_enemy_v2] 
            y_pos = 210
        else: # Snail Type
            ground_enemy_v1 = pygame.image.load('Graphic Images/snail/snail1.png').convert_alpha() # Imports snail files
            ground_enemy_v2 = pygame.image.load('Graphic Images/snail/snail2.png').convert_alpha()
            self.frames = [ground_enemy_v1, ground_enemy_v2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0 
        self.image = self.frames[int(self.animation_index)]

    def destory(self):
        if self.rect.right < 0:
            self.kill() # Removes sprite off the screen

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destory()
    
def display_score():
    current_time = pygame.time.get_ticks() - start_time 
    score_surf = font.render(f'Score: {current_time//1000}', False, "black")
    score_rect = score_surf.get_rect(center=(400, 25))
    screen.blit(score_surf, score_rect)
    return current_time

def IntroScreen():
    # Creating Texts
    title = font.render("Jumper", False, "#008080") # Title
    title_rect = title.get_rect(center=(400, 50))
    action = sub_font.render("Press 'spacebar' to begin", False, "#008080") # Sub caption to instruc the player to begin 
    action_rect = action.get_rect(center=(400, 325))
    # Creating Character Graphic
    char_stand = pygame.image.load("Graphic Images/player/player_stand.png").convert_alpha() # Used for the Home Screen
    char_stand_scaled = pygame.transform.rotozoom(char_stand, 0, 2)
    char_stand_rect = char_stand_scaled.get_rect(center=(400, 200))

    # Displaying Surface(s)
    screen.fill("#F5F5DC")
    screen.blit(title, title_rect)
    screen.blit(char_stand_scaled, char_stand_rect)
    # Displaying Starting Instruction if player hasn't played 
    if high_score == 0:
        screen.blit(action, action_rect)
    else: # Displays the high score and score once the user plays atleast one round
        high_score_result = sub_font.render(f"High Score: {high_score//1000}", False, "#008080")
        high_score_result_rect = high_score_result.get_rect(center=(400, 325))
      
        score_result = sub_font.render(f"Score: {score//1000}", False, "#008080")
        score_result_rect = score_result.get_rect(center=(400, 360))
      
        screen.blit(high_score_result, high_score_result_rect)
        screen.blit(score_result, score_result_rect)

def sprite_collisions():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, True): 
        obstacle_group.empty() # Removes all the sprites in Obstacle_group
        return False
    return True



# Creating Pygame Window 
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption ("Jumper") # Title
clock = pygame.time.Clock()
start_time = 0
high_score = 0
bg_music = pygame.mixer.Sound("audio/music.wav") # Importing bg Music
bg_music.set_volume(0.5)


# Game State
game_state = False 

# Font
font = pygame.font.Font('Fonts/COMIC.TTF', 35)
sub_font = pygame.font.Font("Fonts/COMIC.TTF", 24)

# Background
sky = pygame.image.load('Graphic Images/Sky.png').convert()
ground = pygame.image.load('Graphic Images/ground.png').convert()

# Timer (EVENTS)
obstacle_timer = pygame.USEREVENT + 1


# Player (Character)
player = pygame.sprite.GroupSingle() 
player.add(Player()) # Adds created player sprite to pygame

# Obstacles (Snail, Fly)
obstacle_group = pygame.sprite.Group()


# Main Loop
while True:
    for event in pygame.event.get():
        # Quiting the Game/Program 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_state:
            if event.type == obstacle_timer: # Creating obstacle rectangles
                obstacle_group.add(Obstacles(choice(['fly', 'snail', 'snail', 'snail'])))


        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_state: # Space button to start the game 
            game_state = True
            bg_music.play(loops=-1) # Begins the Music
          

    if game_state: # Game is being Played
        # Displaying the Background
        screen.blit (sky, (0, 0))
        screen.blit (ground, (0, 300))
        # Displaying the Player
        player.update()
        player.draw(screen)
        # Displaying the Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()
        # Displaying the Score
        high_score = display_score() if display_score() > high_score else high_score # Managing the Highscore
        score = display_score() # Holds Previous Score

        # Checking Collisions
        game_state = sprite_collisions()
  
    else: # Intro/Outro Screen
        pygame.mixer.stop() # Stops the Music from Playing
        pygame.time.set_timer(obstacle_timer, 1500) # Frequency of Obstacles Approaching
        start_time = pygame.time.get_ticks()
        IntroScreen()
        
       
    pygame.display.update()
    clock.tick(60)