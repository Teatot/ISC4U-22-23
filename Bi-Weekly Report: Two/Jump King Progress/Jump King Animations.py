import pygame
from sys import exit

pygame.init()  # Initializes Pygame
screen = pygame.display.set_mode((640, 400))
pygame.display.set_caption("Jump King")
clock = pygame.time.Clock()


# Class Initializations
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()  # Initalizes the inherited class
        # Sprite Image Import
        walk_1 = pygame.image.load("images/walk_1.png").convert_alpha()
        walk_idle = pygame.image.load("images/walk_2.png").convert_alpha()
        walk_3 = pygame.image.load("images/walk_3.png").convert_alpha()
        self.walk_frames = [walk_1, walk_idle, walk_3, walk_idle]
        self.index = 0 # 0-3
        self.walking = False # Using to determine if the player is waling
        self.face = False # True = Left, False = Right
        
        self.image = pygame.image.load("images/stand.png").convert_alpha() # Default State: Standing
        self.rect = self.image.get_rect(midbottom=(200, 200))

    def player_move(self):
        keys = pygame.key.get_pressed()  # List of Bools of keys pressed
        if keys[pygame.K_SPACE]: # Holding Space will increase the power of the jump
            self.image = pygame.image.load("images/charging.png").convert_alpha()
            self.rect = self.image.get_rect(midbottom=(200, 200))
        elif keys[pygame.K_d]: # Walking to the Right (D Key)
            self.walking = True
            self.face = False
        elif keys[pygame.K_a]: # Walking to the Left (A Key)
            self.walking = True  
            self.face = True
        else:   # Idle (No Specific Key pressed)
            self.walking = False  
            self.image = pygame.transform.flip(pygame.image.load("images/stand.png").convert_alpha(), self.face, False) 
            self.rect = self.image.get_rect(midbottom=(200, 200))

    def player_animation(self):
        if self.walking:
            self.index += 0.1
            if self.index > len(self.walk_frames): self.index = 0
            self.image = pygame.transform.flip(self.walk_frames[int(self.index)], self.face, False)
            self.rect = self.image.get_rect(midbottom=(200, 200))

    def update(self):
        self.player_move()  # Get Input
        self.player_animation()
        


# Creating Player Group
player = pygame.sprite.GroupSingle()  # Creates the sprite group
player.add(Player())  # Adds our class: player to sprite group

# Main Code
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("white")
    player.draw(screen)
    player.update()

    pygame.display.update()
    clock.tick(60)  # Runs at 60fps
