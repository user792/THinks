#the code goes here

#pygamen tuonti
import pygame

#pygamen initialisaatio
pygame.init()
is_running = True
lives = 3
while is_running:
    #pelin elollisten olijoiden attributejen tallennukseen käytettävä classi
    class Attribute:
        def __init__(self, y_velocity:float, x_velocity:float, on_ground:bool, speed:float,character, x_pos:float, y_pos:float,can_jump:bool,jump_time:int,jump:int,max_jump:int):
            self.y_velocity = y_velocity
            self.x_velocity = x_velocity
            self.on_ground = on_ground
            self.speed = speed
            self.character = character
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.rect = pygame.rect.Rect(self.x_pos,self.y_pos,80,80)
            self.can_jump = can_jump
            self.jump_time = jump_time
            self.jump = jump
            self.max_jump = max_jump

        def update_velocity(self, x_delta, y_delta):
            if self.y_velocity > 9:
                self.y_velocity = 9
            else:
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
                self.jump_time += self.max_jump + 100
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
            global touch
            for location in lista:
                screen.blit(self.texture,location)
                #osumat palikan päällä
                if (location[1] < player.y_pos + 80 < location[1] +20) and (location[0]-80 < player.x_pos < location[0]+self.width):
                    player.y_pos = location[1] - self.height
                    player.y_velocity = 0
                    player.on_ground = True
                    touch = True

                #osumat palikan alla
                if (location[1] +self.height >= player.y_pos >= location[1] +self.height -20) and (location[0]-80 <= player.x_pos <= location[0]+self.width):
                    player.y_pos = location[1] +self.height

                #osumat palikan vasen laita
                if (location[0] <= player.x_pos+80 <= location[0] +20) and (location[1]+10 <= player.y_pos +80 <= location[1]+self.height+80-10):
                    player.x_pos = location[0] -80

                #osumat palikan oikea laita
                if (location[0] + self.width >= player.x_pos >= location[0]-20) and (location[1]+10 <= player.y_pos +80 <= location[1]+self.height+80-10):
                    player.x_pos = location[0] +self.width
        

                
    def drawer(level):
        if level == 1:
            global touch
            touch = False
            sand10x.draw([(global_x_offset+0,520),(global_x_offset+800,520),(global_x_offset+1840,520),(global_x_offset+2880,520),(global_x_offset+4000,520),(global_x_offset+4800,520),(global_x_offset+7200,520)])
            sand.draw([(global_x_offset+5920,520),(global_x_offset+6480,520)])
            brick3x.draw([(global_x_offset+6560,280)])
            brick.draw([(global_x_offset+6000,280)])
            if touch == False:
                player.on_ground = False
    #näytön asetuksia

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #ikkunan nimi
    pygame.display.set_caption("Super Marko Brothers")
    #pelaajan polo animaatio framejen tuonti
    polo_frames = []
    for i in range(1, 8):
        frame = pygame.image.load(f'Polo/Polo{i}.png').convert_alpha()  
        frame = pygame.transform.scale(frame,(80,80))
        polo_frames.append(frame)

    #pelaajan alustaminen
    player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=0.5,character =polo_frames,x_pos=0,y_pos=0,can_jump=False,jump_time=0,jump=-10,max_jump=30)

    #juttu hyppelyyn
    touch = False

    #pelin ajamiseen tarvittava muuttuja
    run = True

    #toiston nopeus
    clock = pygame.time.Clock()

    #animaation muuttujia
    delay = 0
    frameid = 0

    # asioiden lokaatiot suhteessa kameran 0 kohtaan
    global_x_offset = 0

    developper_man_mode = False
    #kitka
    x_delta = 1.1
    #putoamis nopeus pixeliä framessa
    y_delta = 1.1
    #fontti
    font =pygame.font.Font('freesansbold.ttf', 32)
    fontxl =pygame.font.Font('freesansbold.ttf', 100)
    #level 1
    sand10x = Object(width=800,height=80,texture=pygame.image.load("materials/sand10x.png").convert_alpha())
    sand = Object(width=80,height=80,texture=pygame.image.load("materials/sand.png").convert_alpha())
    brick = Object(width=80,height=80,texture=pygame.image.load("materials/brick.png").convert_alpha())
    brick3x = Object(width=240,height=80,texture=pygame.image.load("materials/brick3x.png").convert_alpha())

    level1_bg = pygame.image.load('materials/background.png')
    level1_bg = pygame.transform.scale(level1_bg, (8000, 600))
    # level counter
    level = 1
    if lives == 0:
        run = False
        is_running = False
    while run:
        #näytön tyhjennys
        screen.fill((0,0,0))

            #level 1 tausta
        if level == 1:
            screen.fill((105,192,186))
            screen.blit(level1_bg, (global_x_offset,0))
            if global_x_offset  <= -7200:

                screen.blit(font.render('You win :D',False,(0,0,0)),(0,0))
        #hud
        screen.blit(font.render("lives",False,(0,0,0)),(650,0))
        screen.blit(font.render(f"{lives}",False,(0,0,0)),(700,50))
        # antaa katsella maailmaa ilman pelaaja hahmoa
        if developper_man_mode == True:
            key = pygame.key.get_pressed()
            if key[pygame.K_d]:
                global_x_offset -= 100
            elif key[pygame.K_a]:
                global_x_offset += 100
        else:
            #pelaajan fysiikat ja kamera
            player.update_velocity(x_delta,y_delta)
            
        #drawer pirtää ja testaa törmäykset pelaajan kanssa
        drawer(level)
        #level 1 jutut
        if level == 1:
            player.camera()
        
            


        #animaation juttuja
        delay += 1
        if delay == 6:
            frameid += 1
            delay = 0
            if frameid >= 4:
                frameid = 1








        #pelaajan syötteet pittää olla alimpana muuten ongelmia eisaa siirtää
        #pelaajan syötteet pittää olla alimpana muuten ongelmia eisaa siirtää
        #pelaajan syötteet pittää olla alimpana muuten ongelmia eisaa siirtää
        #pelaajan syötteet pittää olla alimpana muuten ongelmia eisaa siirtää
        #pelaajan syötteet pittää olla alimpana muuten ongelmia eisaa siirtää
        #pelaajan syötteet pittää olla alimpana muuten ongelmia eisaa siirtää
        if developper_man_mode == False:
            player.movement()


        #ikkunan sulkeminen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                run = False
        if player.y_pos > 700:
                lives -= 1
                run = False
    

        
        
        #näytön päyivitys
        pygame.display.update()

        #suorituksen nopeus
        clock.tick(60)
if lives == 0:
    screen.fill((0,0,0))
    screen.blit(fontxl.render('GAME OVER',False,(255,255,255)),(80,250))
    pygame.display.update()
    pygame.time.delay(1000)
#sulkee pygamen
pygame.quit()
