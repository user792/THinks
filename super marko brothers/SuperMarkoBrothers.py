import pygame
import spritesheet
pygame.init()

class Attribute:
    def __init__(self, y_velocity:float, x_velocity:float, on_ground:bool, speed:float, max_speed:float,character):
        self.y_velocity = y_velocity
        self.x_velocity = x_velocity
        self.on_ground = on_ground
        self.speed = speed
        self.max_speed = max_speed
        self.character = character



    def __repr__(self):
        return (f"Attribute(y_velocity={self.y_velocity}, x_velocity={self.x_velocity}, "
                f"on_ground={self.on_ground}, speed={self.speed})")


    def update_velocity(self, y_delta, x_delta):
        self.y_velocity += y_delta
        self.x_velocity += x_delta
        if self.x_velocity > self.max_speed:
            self.x_velocity = self.max_speed

    def set_on_ground(self, on_ground_status):
        self.on_ground = on_ground_status

    def set_speed(self, new_speed):
        self.speed = new_speed


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('doux.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

frames = []
frame_0 = sprite_sheet.get_image(0, 16, 16, 3)
frames.append(frame_0)
frame_1 = sprite_sheet.get_image(1, 16, 16, 3)
frames.append(frame_1)
frame_2 = sprite_sheet.get_image(2, 16, 16, 3)
frames.append(frame_2)
frame_3 = sprite_sheet.get_image(3, 16, 16, 3)
frames.append(frame_3)


clock = pygame.time.Clock()

player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=1, max_speed=10,character =pygame.Rect((300, 250, 50, 50)))
jump = 10
run = True
while run:

    screen.fill((0,0,0))

    screen.blit(frame_0, (0,  0))
    pygame.draw.rect(screen, (255, 0, 0), player.character)

    key = pygame.key.get_pressed()
    if (key[pygame.K_a] == True) and (key[pygame.K_d] == True):
        pass
    elif key[pygame.K_a] == True:
        player.character.move_ip(-player.speed, 0)
    elif key[pygame.K_d] == True:
        player.character.move_ip(player.speed, 0)
    if (key[pygame.K_a] == True) and (key[pygame.K_d] == True):
        pass
    elif key[pygame.K_w] == True:
        if player.on_ground == True:
             player.y_velocity = jump
             
    elif key[pygame.K_s] == True:
        pass
    else:
        frame_0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(30)
pygame.quit()
