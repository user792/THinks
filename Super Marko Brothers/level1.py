import pygame, SuperMarkoBrothers
pygame.init()
sand10x = SuperMarkoBrothers.pygame.image.load("materials/sand10x.png").convert_alpha()  
sand10x = SuperMarkoBrothers.pygame.transform.scale(sand10x,(800,80))

    
rect_1 = pygame.Rect(SuperMarkoBrothers.global_x_offset, 400, 150, 100)
def collision():
    pass


def funkio():
    SuperMarkoBrothers.screen.blit(sand10x,(SuperMarkoBrothers.global_x_offset,400))
    pygame.draw.rect(SuperMarkoBrothers.screen, (255, 0, 255), rect_1)
