#the code goes here

#pygamen tuontis
import pygame

#pygamen initialisaatio
pygame.init()
pygame.mixer.init()
is_running = True
lives = 3
level = 1
score = 0
pygame.mixer.music.load("sound/background_music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
jump_sound = pygame.mixer.Sound("sound/jump.wav")
jump_sound.set_volume(0.05)
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

            self.frameid = 0
            self.delay = 0
            self.frame_count = 4

        def update_velocity(self, x_delta, y_delta):
            if self.y_velocity > 9:
                self.y_velocity = 9
            else:
                self.y_velocity += y_delta
            self.x_velocity = self.x_velocity / x_delta
            
            self.x_pos += self.x_velocity
            self.y_pos += self.y_velocity
            
            self.rect = pygame.rect.Rect(self.x_pos,self.y_pos,80,80)

            


        def camera(self):
            global global_x_offset
            global global_y_offset
            
            if self.x_pos >= 400:
                self.x_pos = 399
                global_x_offset -= self.x_velocity
            if self.y_pos <= 50:
                self.y_pos = 49
                global_y_offset -= self.y_velocity
            if (self.y_pos >= 50) and (not global_y_offset < 1):
                self.y_pos = 50
                global_y_offset -= self.y_velocity
            if global_y_offset <= 0:
                global_y_offset = 0
            if self.x_pos <= 0:
                self.x_pos = 1
            if self.x_pos >= 800:
                self.x_pos = 799
        def movement(self):
            global global_x_offset
            self.delay += 1
            if self.delay == 6:
                self.frameid += 1
                self.delay = 0
                if self.frameid >= self.frame_count:
                    self.frameid = 0
        
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
                jump_sound.play()
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
                screen.blit(pygame.transform.flip(self.character[self.frameid],True,False),(self.x_pos,self.y_pos))
            elif key[pygame.K_d] == True:
                self.x_velocity += self.speed
                screen.blit(self.character[self.frameid],(self.x_pos,self.y_pos))
            else:
                screen.blit(self.character[0],(self.x_pos,self.y_pos))

    class Object:
        def __init__(self,width:int,height:int,texture,loot:str=None,can_walk_through=False):
            self.width = width
            self.height = height
            self.loot = loot
            self.texture = pygame.transform.scale(texture,(self.width,self.height))
            self.can_walk_through = can_walk_through
        def draw(self,lista:list,entities:list=None,can_walk:bool=None):
            global global_x_offset
            global touch
            
            for location in lista:
                screen.blit(self.texture,location)
                if self.can_walk_through == False:
                    #osumat palikan päällä
                    if (location[1] < player.y_pos + 80 < location[1] +20) and (location[0]-80+10 < player.x_pos < location[0]+self.width-10):
                        player.y_pos = location[1] - self.height
                        player.y_velocity = 0
                        player.on_ground = True
                        touch = True

                    #osumat palikan alla
                    if (location[1] +self.height >= player.y_pos >= location[1] +self.height -20) and (location[0]-80+10 <= player.x_pos <= location[0]+self.width-10):
                        player.y_pos = location[1] +self.height
                        if not self.loot == None:
                            items.append(Item(type=f"{self.loot}",x_pos=location[0]-global_x_offset,y_pos=location[1]-80-global_y_offset))
                            self.loot = None

                    #osumat palikan vasen laita
                    if (location[0] <= player.x_pos+80 <= location[0] +20) and (location[1]+10 <= player.y_pos +80 <= location[1]+self.height+80-10):
                        player.x_pos = location[0] -80

                    #osumat palikan oikea laita
                    if (location[0] + self.width >= player.x_pos >= location[0]-20) and (location[1]+10 <= player.y_pos +80 <= location[1]+self.height+80-10):
                        player.x_pos = location[0] +self.width

                if not entities == None:
                #npc osumat        
                    for entity in entities:
                        for location in lista:
                            #osumat palikan päällä
                            if (location[1] < entity.y_pos + 80+global_y_offset < location[1] +20) and (location[0]-80 < entity.x_pos + global_x_offset < location[0]+self.width):
                                entity.y_pos = location[1] - self.height -global_y_offset
                                entity.y_velocity = 0


                            #osumat palikan alla
                            if (location[1] +self.height >= entity.y_pos+global_y_offset >= location[1] +self.height -20) and (location[0]-80 <= entity.x_pos + global_x_offset <= location[0]+self.width):
                                entity.y_pos = location[1] +self.height -global_y_offset

                            #osumat palikan vasen laita
                            if (location[0] <= entity.x_pos + global_x_offset+80 <= location[0] +20) and (location[1]+10 <= entity.y_pos+global_y_offset +80 <= location[1]+self.height+80-10):
                                entity.x_pos = location[0] -80 -global_x_offset
                                entity.x_velocity = -entity.x_velocity
                            #osumat palikan oikea laita
                            if (location[0] + self.width >= entity.x_pos + global_x_offset >= location[0]-20) and (location[1]+10 <= entity.y_pos+global_y_offset +80 <= location[1]+self.height+80-10):
                                entity.x_pos = location[0] +self.width - global_x_offset
                                entity.x_velocity = -entity.x_velocity
    class Enemy:
        def __init__(self, y_velocity:float, x_velocity:float,x_pos:int,y_pos:int, frame_count:int, anim_speed:int, type:str, character:list):
            self.y_velocity = y_velocity
            self.x_velocity = x_velocity
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.frameid = 0
            self.delay = 0
            self.anim_speed = anim_speed
            self.frame_count = frame_count
            self.character = character
            self.rect = pygame.rect.Rect(self.x_pos+10+global_x_offset,self.y_pos+global_y_offset+10,60,60)
            self.type = type
            self.flip = False
        def update(self,y_delta:float):
            if self.y_velocity > 9:
                self.y_velocity = 9
            else:
                self.y_velocity += y_delta
            
            
            self.x_pos += self.x_velocity
            self.y_pos += self.y_velocity
            
            self.rect = pygame.rect.Rect(self.x_pos+10+global_x_offset,self.y_pos+global_y_offset+10,60,60)
            
            self.delay += 1
            if self.delay == self.anim_speed:
                self.frameid += 1
                self.delay = 0
                if self.frameid >= self.frame_count:
                    self.frameid = 0
            if self.x_velocity <= 0:
                screen.blit(pygame.transform.flip(self.character[self.frameid],False,self.flip),(self.x_pos+global_x_offset,self.y_pos+global_y_offset))
            else:
                screen.blit(pygame.transform.flip(self.character[self.frameid],True,self.flip),(self.x_pos+global_x_offset,self.y_pos+global_y_offset))
            
    class Item:
        def __init__(self,type:str,x_pos:int,y_pos:int):
            self.type = type
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.texture = pygame.transform.scale(pygame.image.load(f'items/{type}.png').convert_alpha(),(80,80))
            self.rect =pygame.rect.Rect(self.x_pos+global_x_offset,self.y_pos+global_y_offset,80,80)
        
        def draw(self):
            screen.blit(self.texture,(self.x_pos+global_x_offset,self.y_pos+global_y_offset))
            self.rect =pygame.rect.Rect(self.x_pos+global_x_offset,self.y_pos+global_y_offset,80,80)


    def drawer(level:int,entities:list,items:list):
        global lives
        global run
        global current_level_score
        global win
        global food

        #items
        collect = []
        for item in items:
            if pygame.Rect.colliderect(item.rect,player.rect):
                collect.append(item)
                if item.type == "bucket":
                    win = True
                elif item.type == "taco":
                    food += 1000
                    lives += 1
                elif item.type == "sauce":
                    lives += 1
        for take in collect:
            items.remove(take)
        for item in items:
            if (item.x_pos <= -global_x_offset + 800):
                item.draw()
                




        ded = []
        # npc kuolemat ja tapot
        for entity in entities:
            if entity.y_pos >= 700:
                ded.append(entity)
            if entity.type == "doge":
                if (entity.x_pos + global_x_offset+5 <= player.x_pos+80 <= entity.x_pos +160+ global_x_offset-5) and (entity.y_pos+global_y_offset-80-20 <= player.y_pos <= entity.y_pos+global_y_offset-80): 
                    ded.append(entity)
                    player.y_velocity = player.jump
                    current_level_score += 100
                    
                elif pygame.Rect.colliderect(entity.rect,player.rect):
                    
                    lives -= 1
                    run = False
            
            elif entity.type == "car":
                if (entity.x_pos + global_x_offset+10 <= player.x_pos+80 <= entity.x_pos +160+ global_x_offset-10) and (entity.y_pos+global_y_offset-80-20 <= player.y_pos <= entity.y_pos+global_y_offset-80): 
                    player.y_velocity = player.jump
                    if entity.flip == False:
                        entity.flip = True
                        current_level_score += 100
                        entity.x_velocity = entity.x_velocity *10
                elif pygame.Rect.colliderect(entity.rect,player.rect):
                    
                    lives -= 1
                    run = False
            for upsidedown in entities:
                if (upsidedown.flip == True) and (not upsidedown == entity):
                    if pygame.Rect.colliderect(entity.rect,upsidedown.rect):
                        if entity.flip == True:
                            ded.append(upsidedown)
                            current_level_score += 100
                        ded.append(entity)
                        current_level_score += 100
            for i in entities:
                if not i == entity and (not i.flip and not entity.flip):
                    #osumat olion päältä
                    if (i.y_pos + global_y_offset < entity.y_pos + 80 < i.y_pos + global_y_offset +20) and (i.x_pos + global_x_offset-80 < entity.x_pos + global_x_offset < i.x_pos + global_x_offset+80):
                        entity.y_pos = i.y_pos -80
                        entity.y_velocity = 0
                    #osumat olion alla
                    if (i.y_pos+ global_y_offset +80 >= entity.y_pos >= i.y_pos+ global_y_offset +80 -20) and (i.x_pos + global_x_offset-80 <= entity.x_pos + global_x_offset <= i.x_pos + global_x_offset+80):
                        entity.y_pos = i.y_pos +80

                    #osumat olion vasen laita
                    if (i.x_pos+ + global_x_offset <= entity.x_pos + global_x_offset+80 <= i.x_pos + global_x_offset +20) and (i.y_pos+10+global_y_offset <= entity.y_pos +80 <= i.y_pos+80+80-10+global_y_offset):
                        entity.x_pos = i.x_pos -80 
                        if entity.x_velocity > 0:
                            entity.x_velocity = -entity.x_velocity

                    #osumat polion oikea laita
                    if (i.x_pos + global_x_offset + 80 >= entity.x_pos + global_x_offset >= i.x_pos + global_x_offset-20) and (i.y_pos+10+global_y_offset <= entity.y_pos +80 <= i.y_pos+80+80-10+global_y_offset):
                        entity.x_pos = i.x_pos +80
                        if entity.x_velocity < 0:
                            entity.x_velocity = -entity.x_velocity
        for bury in ded:
            entities.remove(bury)
        for entity in entities:
            if not entity.x_pos >= -global_x_offset + 1000:
                entity.update(y_delta)

        if level == 1:
            global touch
            touch = False

            sand10x.draw([
                (global_x_offset+0,global_y_offset+520),
                (global_x_offset+800,global_y_offset+520),
                (global_x_offset+1840,global_y_offset+520),
                (global_x_offset+2880,global_y_offset+520),
                (global_x_offset+4000,global_y_offset+520),
                (global_x_offset+4800,global_y_offset+520),
                (global_x_offset+7200,global_y_offset+520)
                ],entities)
            
            sand.draw([
                (global_x_offset+5920,global_y_offset+520),
                (global_x_offset+6480,global_y_offset+520)
                ],entities)
            
            brick3x.draw([
                (global_x_offset+6640,global_y_offset+280)
                ],entities)
            
            brick.draw([
                (global_x_offset+6080,global_y_offset+280)
                ],entities)
            lootbox_taco.draw([
                (global_x_offset+360,global_y_offset+280),
                (global_x_offset+360+80,global_y_offset+280)
            ],entities)
            well.draw([
                (global_x_offset+800,global_y_offset+440),
                (global_x_offset+1440,global_y_offset+440),
                (global_x_offset+1440,global_y_offset+360),
                (global_x_offset+1440,global_y_offset+280)
            ],entities)
            canopy.draw([
            (global_x_offset+800,global_y_offset+280),
            (global_x_offset+1440,global_y_offset+100)
            ],entities)
            if touch == False:
                player.on_ground = False
        elif level == 2:
            touch = False

            sand10x.draw([
                (global_x_offset+0,global_y_offset+520),
                (global_x_offset+800,global_y_offset+520),
                (global_x_offset+1840,global_y_offset+520),
                (global_x_offset+2880,global_y_offset+520),
                (global_x_offset+4000,global_y_offset+520),
                (global_x_offset+4800,global_y_offset+520),
                (global_x_offset+7200,global_y_offset+520)
                ],entities)
            
            sand.draw([
                (global_x_offset+5920,global_y_offset+520),
                (global_x_offset+6480,global_y_offset+520)
                ],entities)
            
            brick3x.draw([
                (global_x_offset+6640,global_y_offset+280)
                ],entities)
            
            brick.draw([
                (global_x_offset+6080,global_y_offset+280)
                ],entities)
            lootbox_taco1.draw([
                (global_x_offset+360,global_y_offset+280),
                (global_x_offset+360+80,global_y_offset+280)
            ],entities)
            lootbox_taco2.draw([
                (global_x_offset+360,global_y_offset+280),
                (global_x_offset+360+80,global_y_offset+280)
            ],entities)
            
            if touch == False:
                player.on_ground = False
    #näytön asetuksia

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #ikkunan nimi
    pygame.display.set_caption("Super Marko Brothers")
    #ikkunan kuvake
    pygame.display.set_icon(pygame.image.load('Smb_ico.png'))
    #pelaajan polo animaatio framejen tuonti
    polo_frames = []
    for i in range(1, 8):
        frame = pygame.image.load(f'Polo/Polo{i}.png').convert_alpha()  
        frame = pygame.transform.scale(frame,(80,80))
        polo_frames.append(frame)
    #pelaajan polo animaatio framejen tuonti
    marko_frames = []
    for i in range(1, 8):
        frame = pygame.image.load(f'marko/marko{i}.png').convert_alpha()  
        frame = pygame.transform.scale(frame,(80,80))
        marko_frames.append(frame)
    #koiruli framet
    doge_frames = []
    for i in range(1, 3):
        frame = pygame.image.load(f'doge/doge{i}.png').convert_alpha()  
        frame = pygame.transform.scale(frame,(80,80))
        doge_frames.append(frame)
    #auton framet
    car_frames = []
    for i in range(1, 7):
        frame = pygame.image.load(f'car/car{i}.png').convert_alpha()  
        frame = pygame.transform.scale(frame,(80,80))
        car_frames.append(frame)

    #juttu hyppelyyn
    touch = False

    #pelin ajamiseen tarvittava muuttuja
    run = True

    # voittiko pelaaja
    win = False
    #kello tarvitaan kaikeen
    clock = pygame.time.Clock()

    # asioiden lokaatiot suhteessa kameran 0 kohtaan
    global_x_offset = int(0)

    # asioiden lokaatiot suhteessa kameran 0 kohtaa
    global_y_offset = int()

    # nykyisen tason score
    current_level_score = 0

    #kitka
    x_delta = 1.1
    #putoamis nopeus pixeliä framessa
    y_delta = 1.1
    #fontti
    font =pygame.font.Font('freesansbold.ttf', 32)
    fontxl =pygame.font.Font('freesansbold.ttf', 100)
    #level 1
    if level == 1:

        #pelaajan alustaminen
        player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=0.5,character =polo_frames,x_pos=0,y_pos=0,can_jump=False,jump_time=0,jump=-10,max_jump=30)

        sand10x = Object(width=800,height=80,texture=pygame.image.load("materials/sand10x.png").convert_alpha())
        sand = Object(width=80,height=80,texture=pygame.image.load("materials/sand.png").convert_alpha())
        brick = Object(width=80,height=80,texture=pygame.image.load("materials/brick.png").convert_alpha())
        brick3x = Object(width=240,height=80,texture=pygame.image.load("materials/brick3x.png").convert_alpha())
        lootbox_taco = Object(width=80,height=80,texture=pygame.image.load("materials/brick.png").convert_alpha(),loot="taco")
        well = Object(width=160,height=80,texture=pygame.image.load("materials/well.png").convert_alpha())
        canopy = Object(width=160,height=160,texture=pygame.image.load("materials/canopy.png").convert_alpha(),can_walk_through=True)


        level1_bg = pygame.image.load('materials/background.png')
        level1_bg = pygame.transform.scale(level1_bg, (8000, 600))

        food = 3000
        entities = [
            Enemy(x_pos=700,y_pos=440,x_velocity=-1,y_velocity=0,frame_count=6,anim_speed=6,type="car",character=car_frames),
            Enemy(x_pos=600,y_pos=440,x_velocity=-1,y_velocity=0,frame_count=2,anim_speed=6,type="doge",character=doge_frames)
            
                    ]
        items = [
            Item(type="bucket",x_pos=7600,y_pos=440)
        ]
    elif level == 2:

        #pelaajan alustaminen
        player = Attribute(y_velocity=0.0, x_velocity=0.0, on_ground=True, speed=0.5,character =marko_frames,x_pos=0,y_pos=0,can_jump=False,jump_time=0,jump=-10,max_jump=30)

        sand10x = Object(width=800,height=80,texture=pygame.image.load("materials/sand10x.png").convert_alpha())
        sand = Object(width=80,height=80,texture=pygame.image.load("materials/sand.png").convert_alpha())
        brick = Object(width=80,height=80,texture=pygame.image.load("materials/brick.png").convert_alpha())
        brick3x = Object(width=240,height=80,texture=pygame.image.load("materials/brick3x.png").convert_alpha())
        lootbox_taco1 = Object(width=80,height=80,texture=pygame.image.load("materials/brick.png").convert_alpha(),loot="taco")
        lootbox_taco2 = Object(width=80,height=80,texture=pygame.image.load("materials/brick.png").convert_alpha(),loot="taco")

        level1_bg = pygame.image.load('materials/background.png')
        level1_bg = pygame.transform.scale(level1_bg, (8000, 600))

        food = 3000.0
        entities = [
            Enemy(x_pos=100,y_pos=40,x_velocity=1,y_velocity=0,frame_count=2,anim_speed=6,type="doge",character=doge_frames),
            Enemy(x_pos=200,y_pos=40,x_velocity=1,y_velocity=0,frame_count=6,anim_speed=6,type="car",character=car_frames)
                    ]
    # live counter

    if lives == 0:
        run = False
        is_running = False
    while run:
        food -= 1
        #näytön tyhjennys
        screen.fill((0,0,0))

            #level 1 tausta
        if level == 1:
            screen.fill((105,192,186))
            screen.blit(level1_bg, (global_x_offset,global_y_offset))
            if global_x_offset <= -7200:
                global_x_offset = -7200
            

                
        elif level == 2:
            screen.fill((105,192,186))
            screen.blit(level1_bg, (global_x_offset,global_y_offset))
            if global_x_offset <= -7200:
                global_x_offset = -7200

        if win:    
            level += 1
            current_level_score += food//10*10
            score += current_level_score
            pygame.time.delay(1000) 
            run = False
        #hud
        screen.blit(font.render("lives",False,(0,0,0)),(650,0))
        screen.blit(font.render(f"{lives}",False,(0,0,0)),(700,50))
        screen.blit(font.render("food",False,(0,0,0)),(250,0))
        screen.blit(font.render(f"{int(food//10)}",False,(0,0,0)),(300,50))
        screen.blit(font.render("level",False,(0,0,0)),(450,0))
        screen.blit(font.render(f"{level}",False,(0,0,0)),(500,50))
        screen.blit(font.render("score",False,(0,0,0)),(50,0))
        screen.blit(font.render(f"{score+current_level_score}",False,(0,0,0)),(100,50))
        #pelaajan fysiikat ja kamera
        player.update_velocity(x_delta,y_delta)

        #drawer pirtää ja testaa törmäykset pelaajan kanssa
        drawer(level,entities,items)
        #kameran liikket
        
        player.camera()

        #pelaajan syötteet pittää olla alimpana muuten ongelmia eisaa siirtää
        
        player.movement()

        #ikkunan sulkeminen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                run = False
        #pelaajan kuolema pudotukseen
        if (player.y_pos > 700+global_y_offset) or (food < 0):
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
