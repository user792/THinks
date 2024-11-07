import pygame, SuperMarkoBrothers
pygame.init()
sand10x = SuperMarkoBrothers.pygame.image.load("materials/sand10x.png").convert_alpha()  
sand10x = SuperMarkoBrothers.pygame.transform.scale(sand10x,(800,80))
while True:
    SuperMarkoBrothers.screen.blit(sand10x,(SuperMarkoBrothers.global_x_offset,400))