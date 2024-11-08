#the code goes here

#pygamen tuonti
import pygame

#pygamen initialisaatio
pygame.init()

#pelin elollisten olijoiden attributejen tallennukseen käytettävä classi
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
    

#näytön asetuksia

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#pelaajan polo animaatio framejen tuonti
polo_frames = []
for i in range(1, 8):
    frame = pygame.image.load(f'Polo/Polo{i}.png').convert_alpha()  
    frame = pygame.transform.scale(frame,(80,80))
    polo_frames.append(frame)

#pelaajan alustaminen
player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=1, max_speed=10,character =polo_frames,x_pos=0,y_pos=0)
player2 = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=1, max_speed=10,character =polo_frames,x_pos=0,y_pos=0)
#pelaajan hyppy voima
jump = -10

#pelin ajamiseen tarvittava muuttuja
run = True

#toiston nopeus
clock = pygame.time.Clock()

#animaation muuttujia
delay = 0
frameid = 0

# asioiden lokaatiot suhteessa kameran 0 kohtaan
global_x_offset = 0
global_y_offset = 0

#kitka
x_delta = 1.1
y_delta = 1.1

#level 1
sand10x = pygame.image.load("materials/sand10x.png").convert_alpha()  
sand10x = pygame.transform.scale(sand10x,(800,80))







# level counter
level = 1


while run:
    #näytön tyhjennys
    screen.fill((0,0,0))
    #animaation juttuja
    delay += 1
    if delay == 3:
        frameid += 1
        delay = 0
        if frameid >= 4:
            frameid = 0
    #pelaajan fysiikat ja kamera
    player.update_velocity(x_delta,y_delta)
    if player.x_pos >= 400:
        player.x_pos = 399
        global_x_offset -= player.x_velocity
    if player.x_pos <= 0:
        player.x_pos = 1
    


    





    #level 1 jutut
    if level == 1:
        screen.blit(sand10x,(global_x_offset,400))
        
        if pygame.Rect.colliderect(pygame.rect.Rect(global_x_offset,400,800,80),pygame.rect.Rect(player.x_pos,player.y_pos,80,80)):
            player.y_pos = 320
            player.y_velocity = 0

    #pelaajan syötteet
    key = pygame.key.get_pressed()

    #hyppiminen
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
    #kävely
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

   
 





    #ikkunan sulkeminen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

 

    
    
    #näytön päyivitys
    pygame.display.update()
    #suorituksen nopeus
    clock.tick(30)
#sulkee pygamen
pygame.quit()
