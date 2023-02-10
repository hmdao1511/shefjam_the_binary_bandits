# import pygame, os, sys
# from pygame.locals import *

# pygame.init()
# fpsClock = pygame.time.Clock()
# surface = pygame.display.set_mode((1000, 600))
# background = pygame.Color(100, 149, 237)

# while True:
#     surface.fill(background)
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#     pygame.display.update()
#     fpsClock.tick(30)
import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption("Wicked Salvation")
clock = pygame.time.Clock()

test_surface = pygame.image.load("bgmain.png")


while True:
    # Get all events 
    for event in pygame.event.get():
        # If the player wants to quit, we terminate 
        # the app and close the window
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    # Stacking surface on another surface, initial position of the surface
    screen.blit(test_surface, (0,0))
    # Draw all elements
    # Update everything
    pygame.display.update()
    # This tell the While loop to not run faster than 60 times per seconds
    # AKA maximum frame rate
    clock.tick(60)
    