import pygame, os, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock();
screen = pygame.display.set_mode((800,600))
background = pygame.Color(50, 50 ,50)
sprite_sheet_image = pygame.image.load('spritesheet.png').convert_alpha()
BLACK = (0,0,0)

def get_image(sheet, frame, width, height, scale, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)
    return image

frame_1 = get_image(sprite_sheet_image, 0, 30, 48, 2.5, BLACK)
frame_2 = get_image(sprite_sheet_image, 1, 30, 48, 2.5, BLACK)
frame_3 = get_image(sprite_sheet_image, 2, 30, 48, 2.5, BLACK)
run = True
while run:
    screen.fill(background);
    screen.blit(frame_1, (0,0))
    screen.blit(frame_2, (200,200))
    screen.blit(frame_3, (300,200))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(30)