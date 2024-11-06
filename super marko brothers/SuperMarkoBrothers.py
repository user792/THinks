#the code goes here
import pygame
pygame.init()

class Attribute:
    def __init__(self, y_velocity:float, x_velocity:float, on_ground:bool, speed:float, max_speed:float,character, x_pos:float, y_pos:float):
        self.y_velocity = y_velocity
        self.x_velocity = x_velocity
        self.on_ground = on_ground
        self.speed = speed
        self.max_speed = max_speed
        self.character = character
        self.x_pos = x_pos
        self.y_pos = y_pos
    def __repr__(self):
        return (f"Attribute(y_velocity={self.y_velocity}, x_velocity={self.x_velocity}, "
                f"on_ground={self.on_ground}, speed={self.speed})")


    def update_velocity(self, y_delta, x_delta):
        self.y_velocity += y_delta
        self.x_velocity = self.x_velocity / x_delta
        
        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity

    def set_on_ground(self, on_ground_status):
        self.on_ground = on_ground_status

    def set_speed(self, new_speed):
        self.speed = new_speed



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

polo_frames = []
for i in range(1, 5):
    frame = pygame.image.load(f'Polo/Polo{i}.png').convert_alpha()  
    frame = pygame.transform.scale(frame,(100,100))
    polo_frames.append(frame)

player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=1, max_speed=10,character =pygame.Rect((300, 250, 50, 50)),x_pos=0,y_pos=0)
jump = -10
run = True
clock = pygame.time.Clock()
while run:

    player.update_velocity(1.1,1.1)

    screen.fill((0,0,0))
    screen.blit(polo_frames[0],(player.x_pos,player.y_pos))
    pygame.draw.rect(screen, (255, 0, 0), player.character)

    key = pygame.key.get_pressed()
    if (key[pygame.K_a] == True) and (key[pygame.K_d] == True):
        pass
    elif key[pygame.K_a] == True:
        player.x_velocity += -player.speed
        
    elif key[pygame.K_d] == True:
        player.x_velocity += player.speed
    
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
    clock.tick(30)
pygame.quit()
