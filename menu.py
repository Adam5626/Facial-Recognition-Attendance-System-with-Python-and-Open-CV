import pygame
import sys
from pygame.locals import *

from facial_recognition import FacialRecognition

pygame.init()

window_width = 1280
window_height = 720


# initializing the constructor
pygame.init()

# screen resolution
res = (720, 720)

# opens up a window
screen = pygame.display.set_mode(res)

# white color
color = (255, 255, 255)
size = (window_width, window_height)
screen = pygame.display.set_mode(size)
color_light = (150, 150, 0)

smallfont = pygame.font.SysFont('Arial', 20, bold=True)
text = smallfont.render('START ATTENDANCE', True, color)


background_image = pygame.image.load("bg.png").convert()

dead = False
while(dead == False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True
        if event.type == pygame.MOUSEBUTTONDOWN and start.collidepoint(mouse):
            FacialRecognition()
            dead = True
    pygame.display.flip()
    screen.blit(background_image, [0, 0])
    start = pygame.draw.rect(screen, color_light, [
        window_width/2 - 110, window_height/2 + 100, 200, 60])

    mouse = pygame.mouse.get_pos()
    screen.blit(text, (window_width/2 - 95, window_height/2 + 115))
