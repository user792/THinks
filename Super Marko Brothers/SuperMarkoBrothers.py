#the code goes here

#pygamen tuonti
import pygame

#pygamen initialisaatio
pygame.init()

#pelin elollisten olijoiden attributejen tallennukseen käytettävä classi
class Attribute:
    def __init__(self, y_velocity:float, x_velocity:float, on_ground:bool, speed:float, max_speed:float,character, x_pos:float, y_pos:float,can_jump:bool,jump_time:int,jump:int,max_jump:int):
        self.y_velocity = y_velocity
        self.x_velocity = x_velocity
        self.on_ground = on_ground
        self.speed = speed
        self.max_speed = max_speed
        self.character = character
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = pygame.rect.Rect(self.x_pos,self.y_pos,80,80)
        self.can_jump = can_jump
        self.jump_time = jump_time
        self.jump = jump
        self.max_jump = max_jump

    def update_velocity(self, y_delta, x_delta):
        self.y_velocity += y_delta
        self.x_velocity = self.x_velocity / x_delta
        
        self.x_pos += self.x_velocity
        self.y_pos += self.y_velocity
        
        self.rect = pygame.rect.Rect(self.x_pos,self.y_pos,80,80)
        global global_x_offset
        
        if self.x_pos >= 550:
            self.x_pos = 549
            global_x_offset -= self.x_velocity
        if self.x_pos <= 0:
            self.x_pos = 1
    def camera(self):
        global global_x_offset
       
        if self.x_pos >= 400:
            self.x_pos = 399
            global_x_offset -= self.x_velocity
        if self.x_pos <= 0:
            self.x_pos = 1
    def movement(self):
        global global_x_offset
        
     
         #pelaajan syötteet
        key = pygame.key.get_pressed()

        if self.on_ground:
            self.can_jump = True
            self.jump_time = 0
        elif 0 < self.jump_time < self.max_jump:
            self.can_jump = True
        else:
            self.on_ground = False
            self.can_jump = False
            

        #hyppiminen
        if (key[pygame.K_w] == True) and (self.can_jump == True):
            self.y_velocity = self.jump
            self.jump_time += 1
            if (key[pygame.K_a] == True) and (key[pygame.K_d] == True):
                screen.blit(self.character[5],(self.x_pos,self.y_pos))
            elif key[pygame.K_a] == True:
                self.x_velocity += -self.speed
                screen.blit(pygame.transform.flip(self.character[5],True,False),(self.x_pos,self.y_pos))
            elif key[pygame.K_d] == True:
                self.x_velocity += self.speed
                screen.blit(self.character[5],(self.x_pos,self.y_pos))
            else:
                screen.blit(self.character[5],(self.x_pos,self.y_pos))
        elif (self.jump_time > 0) and (self.can_jump):
            self.jump_time += self.max_jump
            screen.blit(self.character[5],(self.x_pos,self.y_pos))   
        #kävely
        elif (key[pygame.K_a] == True) and (key[pygame.K_d] == True):
            screen.blit(self.character[0],(self.x_pos,self.y_pos))
        elif key[pygame.K_a] == True:
            self.x_velocity += -self.speed
            screen.blit(pygame.transform.flip(self.character[frameid],True,False),(self.x_pos,self.y_pos))
        elif key[pygame.K_d] == True:
            self.x_velocity += self.speed
            screen.blit(self.character[frameid],(self.x_pos,self.y_pos))
        else:
            screen.blit(self.character[0],(self.x_pos,self.y_pos))
class Object:
    def __init__(self,width:int,height:int,texture):
        self.width = width
        self.height = height
        self.texture = pygame.transform.scale(texture,(self.width,self.height))
    def draw(self,lista):
        global global_x_offset
       
        for location in lista:
            screen.blit(self.texture,location)

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
player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=1, max_speed=10,character =polo_frames,x_pos=0,y_pos=0,can_jump=False,jump_time=0,jump=-10,max_jump=30)


#pelin ajamiseen tarvittava muuttuja
run = True

#toiston nopeus
clock = pygame.time.Clock()

#animaation muuttujia
delay = 0
frameid = 0

# asioiden lokaatiot suhteessa kameran 0 kohtaan
global_x_offset = 0


#kitka
x_delta = 1.1
y_delta = 1.1

#level 1
sand10x = Object(width=800,height=80,texture=pygame.image.load("materials/sand10x.png").convert_alpha())

level1_bg = pygame.image.load('materials/background.png')
level1_bg = pygame.transform.scale(level1_bg, (8000, 600))
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

    #level 1 jutut
    if level == 1:
        player.camera()
        screen.blit(level1_bg, (global_x_offset,0))
        sand10x.draw([(global_x_offset+0,520),(global_x_offset+70,120)])
        
        if pygame.Rect.colliderect(pygame.rect.Rect(global_x_offset,520,800,80),player.rect):
            player.y_pos = 440
            player.y_velocity = 0
            player.on_ground = True
        else:
            player.on_ground = False
    #pelaajan syötteet
    player.movement()




    #ikkunan sulkeminen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if player.y_pos > 700:
            run = False
 

    
    
    #näytön päyivitys
    pygame.display.update()

    #suorituksen nopeus
    clock.tick(30)

#sulkee pygamen
pygame.quit()
