#the code goes here
import pygame
pygame.init()

class Attribute:
    def __init__(self, y_velocity:float, x_velocity:float, on_ground:bool, speed:float, max_speed:float):
        self.y_velocity = y_velocity
        self.x_velocity = x_velocity
        self.on_ground = on_ground
        self.speed = speed
        self.max_speed = max_speed

    def __repr__(self):
        return (f"Attribute(y_velocity={self.y_velocity}, x_velocity={self.x_velocity}, "
                f"on_ground={self.on_ground}, speed={self.speed})")

    # Example of methods you might add
    def update_velocity(self, y_delta, x_delta):
        self.y_velocity += y_delta
        self.x_velocity += x_delta

    def set_on_ground(self, on_ground_status):
        self.on_ground = on_ground_status

    def set_speed(self, new_speed):
        self.speed = new_speed

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = pygame.Rect((300, 250, 50, 50))
player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=0.25, max_speed=1)
jump = 10
run = True
while run:

    screen.fill((0,0,0))

    pygame.draw.rect(screen, (255, 0, 0), player)

    key = pygame.key.get_pressed()
    if (key[pygame.K_a] == True) and (key[pygame.K_d] == True):
        pass
    elif key[pygame.K_a] == True:
        player.move_ip(-player.speed, 0)
    elif key[pygame.K_d] == True:
        player.move_ip(player.speed, 0)
    if (key[pygame.K_a] == True) and (key[pygame.K_d] == True):
        pass
    elif key[pygame.K_w] == True:
        if player.on_ground == True:
             player.y_velocity = jump
             
    elif key[pygame.K_s] == True:
        pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    
pygame.quit()
