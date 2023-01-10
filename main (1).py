import pygame
import math
from sys import exit

pygame.init()  # Initializes Pygame
screen = pygame.display.set_mode((700, 500))
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
        self.index = 0  # 0-3

        # Animated States
        self.walking = False
        self.left_blocked, self.right_blocked = False, False
        self.charging = False
        self.collision_fall = False
        self.face = False  # Where is the sprite facing (True = Left, False = Right)
        self.bounce = None

        # Positional Varibles
        self.x = 50
        self.y = 500
        self.jump_power = 0
        self.gravity = 0
        self.move_val = 3
        self.aerial = 0
        self.last_ground_pos = (self.x, self.y)

        self.image = pygame.image.load("images/stand.png").convert_alpha()  # Default State: Standing
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def player_move(self):
        keys = pygame.key.get_pressed()  # List of Bools of keys pressed

        if keys[pygame.K_a] and not self.bounce:
            self.face = True  # Change facing direction (Left)
        elif keys[pygame.K_d] and not self.bounce:
            self.face = False  # Change facing direction (Right)

        # Sprite Movements
        if not self.charging:  # Prevents Player to move when charging its jump
            if keys[pygame.K_a] and not self.right_blocked:
                self.rect.x -= self.move_val
                self.x -= self.move_val  # Towards the Left
            elif keys[pygame.K_d] and not self.left_blocked:
                self.rect.x += self.move_val
                self.x += self.move_val  # Towards the Right

        if self.rect.bottom == self.y:  # If the Player is on the ground

            if keys[pygame.K_SPACE] and not self.walking:  # Holding Space will increase the power of the jump
                if not self.charging:
                    self.start_time = pygame.time.get_ticks()  # Starts the Timer (Max of 1/2 second of charging);
                self.charging = True
                self.image = pygame.image.load("images/charging.png").convert_alpha()
                self.rect = self.image.get_rect(midbottom=(self.x, self.y))
                if int(pygame.time.get_ticks()) - int(self.start_time) < 400:
                    self.jump_power -= 1  # Increasing Jump Power

            elif self.rect.bottom + self.jump_power < self.y:  # The player is in the air
                # Updates new ground position
                self.last_ground_pos = self.rect.midbottom
                self.gravity = self.jump_power
                self.charging = False
                self.move_val = 6
                self.jump_power = 0  # Resets Jump Power
                self.image = pygame.transform.flip(pygame.image.load("images/jump.png").convert_alpha(), self.face,
                                                   False)
                self.rect = self.image.get_rect(midbottom=(self.x, self.y))

            elif (keys[pygame.K_a] or keys[pygame.K_d]) and not self.charging:  # Walking
                self.walking = True
                self.move_val = 2

            else:  # Idle (No Specific Key pressed)
                self.walking = False
                self.image = pygame.transform.flip(pygame.image.load("images/stand.png").convert_alpha(), self.face,
                                                   False)
                self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def player_animation(self):
        if self.walking:
            self.index += 0.1
            if self.index > len(self.walk_frames): self.index = 0
            self.image = pygame.transform.flip(self.walk_frames[int(self.index)], self.face, False)
            self.rect = self.image.get_rect(midbottom=(self.x, self.y))

        elif self.collision_fall:  # Sprite Falling (With Collision)
            self.image = pygame.transform.flip(pygame.image.load("images/fall_collision.png").convert_alpha(),
                                               self.face, False)

        elif self.gravity > 0:  # Sprite Falling (No Collision)
            self.image = pygame.transform.flip(pygame.image.load("images/fall.png").convert_alpha(), self.face, False)

    def Bounce_off_wall(self):
        self.collision_fall = True
        # Bouncing off Right Wall
        if self.face:
            if self.last_ground_pos[0] + 50 > self.rect.midbottom[0] + 6:
                if self.closest_leftRect.left < self.rect.right and self.closest_leftRect.top < self.rect.bottom and self.rect.midbottom[0] + 6 > self.last_ground_pos[0]:
                    self.bounce = False
                    self.y = 500  # Sets the user to fall
                else:
                    self.x += 6
                    self.rect.x += 6
                    self.y -= round(math.log(6, self.base_values[-1]), 2)
                    self.rect.y -= round(math.log(6, self.base_values[-1]), 2)
                    self.base_values.pop()
            else:
                self.bounce = False
                self.y = 500  # Sets the user to fall

        # Bouncing off Left Wall
        elif not self.face:
            if self.last_ground_pos[0] - 50 < self.rect.midbottom[0] - 6:
                if self.closest_rightRect.right > self.rect.left and self.closest_rightRect.top < self.rect.bottom and self.rect.midbottom[0] - 6 < self.last_ground_pos[0]:
                    self.bounce = False
                    self.y = 500
                else:
                    self.x -= 6
                    self.rect.x -= 6
                    self.y -= round(math.log(6, self.base_values[-1]), 2)
                    self.rect.y -= round(math.log(6, self.base_values[-1]), 2)
                    self.base_values.pop()
            else:
                self.bounce = False
                self.y = 500

    def Find_Closest(self, rects, index):
        global pos_rects, ref_value
        if index == 0:  # Inspecting Top Side
            pos_rects = [x.top for x in rects]
            ref_value = self.rect.bottom

        elif index == 1:  # Inspecting Left Side
            pos_rects = [x.left for x in rects]
            ref_value = self.rect.right

        elif index == 2:  # Inspecting Right Side
            pos_rects = [x.right for x in rects]
            ref_value = self.rect.left

        elif index == 3:  # Inspecting Bottom Side
            pos_rects = [x.bottom for x in rects]
            ref_value = self.rect.top

        # Finding The Closest Floor through Height
        for i in range(1, len(rects)):
            j = i - 1
            key_pos = pos_rects[i]
            key_rect = rects[i]
            while j >= 0 and abs(ref_value - key_pos) < abs(ref_value - pos_rects[j]):
                pos_rects[j + 1] = pos_rects[j]
                rects[j + 1] = rects[j]
                j -= 1
            pos_rects[j + 1] = key_pos
            rects[j + 1] = key_rect
        return rects[0]

    def check_collision(self, rects):
        """
        Sorts the obstacle rectangles based off the current position of the player rectangle (sorted(...))
        """
        self.closest_topRect = self.Find_Closest(sorted(rects, key=lambda x: abs(self.rect.x - x.x)), 0)
        self.closest_bottomRect = self.Find_Closest(sorted(rects, key=lambda x: abs(self.rect.x - x.x)), 3)
        self.closest_leftRect = self.Find_Closest(sorted(rects, key=lambda x: abs(self.rect.y - x.y)), 1)
        self.closest_rightRect = self.Find_Closest(sorted(rects, key=lambda x: abs(self.rect.y - x.y)), 2)

        # Hitting Head Against the Top of the Floor
        if self.rect.clipline(self.closest_bottomRect.left, self.closest_bottomRect.bottom,
                              self.closest_bottomRect.right,
                              self.closest_bottomRect.bottom) and self.rect.top >= self.closest_bottomRect.bottom + self.gravity:
            self.gravity = 5
            self.collision_fall = True

        # Landing on an elevated Floor
        if self.rect.clipline(self.closest_topRect.left + 1, self.closest_topRect.top - self.gravity,
                              self.closest_topRect.right - 1,
                              self.closest_topRect.top - self.gravity) and self.rect.bottom <= self.closest_topRect.top:
            self.y = self.closest_topRect.top

        # Colliding with the Right side of a wall
        if self.rect.clipline(self.closest_rightRect.right, self.closest_rightRect.top, self.closest_rightRect.right,
                              self.closest_rightRect.bottom) and not self.collision_fall:
            if self.rect.bottom == self.y:  # Player on standing
                self.rect.left = self.closest_rightRect.right
                self.x += 2
                self.right_blocked = True
            elif self.gravity < 0:  # Bouncing
                self.gravity = 0  # Resets the gravity value
                self.bounce = True  # Initiates the bouncing off the wall phase
                self.face = True  # Change facing direction to Left
                self.base_values = [1 + (x * 0.05) for x in
                                    range(int(abs(self.last_ground_pos[0] + 50 - self.closest_rightRect.right) / 6), 0,
                                          -1)]
            elif self.gravity > 0:  # User is falling
                print("CLIP RIGHT")
                self.move_val = 0  # Cannot Move in the air
                self.rect.x += 6  # Energy Released back (Prevents further bugs)

        # Colliding with the Left side of a wall
        if self.rect.clipline(self.closest_leftRect.left, self.closest_leftRect.top, self.closest_leftRect.left,
                              self.closest_leftRect.bottom) and not self.collision_fall:
            if self.rect.bottom == self.y:  # Player Standing
                self.rect.right = self.closest_leftRect.left
                self.x -= 2
                self.left_blocked = True
            elif self.gravity < 0:  # Bouncing
                self.gravity = 0  # Resets the gravity value
                self.bounce = True  # Initiates the bouncing off the wall Phase
                self.face = False  # Change facing direction to Right
                self.base_values = [1 + (x * 0.05) for x in
                                    range(int(abs(self.last_ground_pos[0] - 50 - self.closest_leftRect.left) / 6), 0,
                                          -1)]
            elif self.gravity > 0:  # User is falling
                print("CLIP LEFT")
                self.move_val = 0  # Cannot Move in the air
                self.rect.x -= 6  # Energy Released back (Prevents further bugs)

        # Falling off a platform
        elif self.rect.right < self.closest_topRect.left or self.rect.left > self.closest_topRect.right:
            self.y = 500

        # Allowing Movement when not near an opposing wall (Facing Left)
        if self.rect.right != self.closest_leftRect.left or self.rect.bottom < self.closest_leftRect.top:
            self.left_blocked = False

        # Allowing Movemet when not near an opposing wall (Facing Right)
        if self.rect.left != self.closest_rightRect.right or self.rect.bottom < self.closest_rightRect.top:
            self.right_blocked = False

    def apply_gravity(self):
        self.rect.y += self.gravity
        if self.rect.bottom < self.y:
            self.gravity += 1
            self.walking = False
        else:
            self.gravity = 0
            self.rect.bottom = self.y
            self.collision_fall = False

    def update(self, objs):
        self.player_move()  # Get Input
        self.player_animation()  # Display Animations
        self.check_collision(objs)
        if self.bounce:
            self.move_val = 0
            self.Bounce_off_wall()
        else:
            self.apply_gravity()  #


# Levels
class Levels:

    def __init__(self):
        self.name = "Tony"
        self.bg = pygame.image.load("images/background.png").convert_alpha()

    def Beginner_Room(self):  # Level One

        screen.blit(self.bg, (0, 0))

        wall_left = pygame.Rect(-10, 0, 10, 500)
        wall_right = pygame.Rect(700, 0, 710, 500)
        # Platforms
        block1 = pygame.Rect(100, 350, 50, 50)
        block2 = pygame.Rect(100, 150, 50, 50)
        block3 = pygame.Rect(50, 450, 200, 10)

        pygame.draw.rect(screen, "orange", wall_left)
        pygame.draw.rect(screen, "orange", wall_right)
        pygame.draw.rect(screen, "white", block1)
        pygame.draw.rect(screen, "white", block2)
        pygame.draw.rect(screen, "white", block3)
        return [wall_right, wall_left, block1, block2, block3]


# Initialization of Levels
room = Levels()

# Creating Player Group
player = pygame.sprite.GroupSingle()  # Creates the sprite group
player.add(Player())  # Adds our class: player to sprite group
broad = []
# Main Code
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    hazards = room.Beginner_Room()

    player.draw(screen)
    player.update(hazards)

    pygame.display.update()
    clock.tick(60)  # Runs at 60fps
