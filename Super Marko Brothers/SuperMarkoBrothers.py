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
        self.rect = pygame.rect.Rect(self.x_pos,self.y_pos,80,80)

    def update_velocity(self, y_delta, x_delta):
        self.y_velocity += y_delta
        self.x_velocity = self.x_velocity / x_delta
        
        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity
        
        global global_x_offset
        
        if self.x_pos >= 550:
            self.x_pos = 549
            global_x_offset -= player.x_velocity
        if self.x_pos <= 0:
            self.x_pos = 1
    def set_on_ground(self, on_ground_status):
        self.on_ground = on_ground_status

    def set_speed(self, new_speed):
        self.speed = new_speed
    



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

polo_frames = []
for i in range(1, 8):
    frame = pygame.image.load(f'Polo/Polo{i}.png').convert_alpha()  
    frame = pygame.transform.scale(frame,(80,80))
    polo_frames.append(frame)

player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=1, max_speed=10,character =polo_frames,x_pos=0,y_pos=0)
player2 = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=1, max_speed=10,character =polo_frames,x_pos=0,y_pos=0)
jump = -10
run = True
clock = pygame.time.Clock()
delay = 0
frameid = 0

global_x_offset = 0

x_delta = 1.1
y_delta = 1.1

#level 1
import level1










while run:
    
    
    delay += 1
    if delay == 3:
        frameid += 1
        delay = 0
        if frameid >= 4:
            frameid = 0
    player.update_velocity(x_delta,y_delta)
    if player.x_pos >= 550:
        player.x_pos = 549
        global_x_offset -= player.x_velocity
    if player.x_pos <= 0:
        player.x_pos = 1
    
    player2.update_velocity(1.1,1.1)
    if player2.x_pos >= 550:
        player2.x_pos = 549
        global_x_offset -= player.x_velocity
    if player2.x_pos <= 0:
        player2.x_pos = 1
    screen.fill((0,0,0))
    
    level1.funkio()
    key = pygame.key.get_pressed()


    if (key[pygame.K_w] == True) and (player.on_ground == True):
        player.y_velocity = jump
        if (key[pygame.K_a] == True) and (key[pygame.K_d] == True):
            screen.blit(player.character[5],(player.x_pos,player.y_pos))
        elif key[pygame.K_a] == True:
            player.x_velocity += -player.speed
            screen.blit(pygame.transform.flip(player.character[5],True,False),(player.x_pos,player.y_pos))
        elif key[pygame.K_d] == True:
            player.x_velocity += player.speed
            screen.blit(player.character[5],(player.x_pos,player.y_pos))
        else:
            screen.blit(player.character[5],(player.x_pos,player.y_pos))



    elif (key[pygame.K_a] == True) and (key[pygame.K_d] == True):
        screen.blit(player.character[0],(player.x_pos,player.y_pos))
    elif key[pygame.K_a] == True:
        player.x_velocity += -player.speed
        screen.blit(pygame.transform.flip(player.character[frameid],True,False),(player.x_pos,player.y_pos))
    elif key[pygame.K_d] == True:
        player.x_velocity += player.speed
        screen.blit(player.character[frameid],(player.x_pos,player.y_pos))
    else:
        screen.blit(player.character[0],(player.x_pos,player.y_pos))

   
 






    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

 

    
    

    pygame.display.update()
    clock.tick(30)
pygame.quit()