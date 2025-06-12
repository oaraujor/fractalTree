#   Fractal Canopy Visualization
#   Author: Octavio Araujo Rosales
#   Date: 05/28/2025
#   Last edited: 05/29/2025

import pygame
import os
import ctypes

from custLinAlg import *

ratio = .70
angle1 = 90
angle2 = 90
max_generations = 9


def draw_linesR(screen, color, start, direction, n, N):
    if n > N:
        return
    
    # Compute new direction
    scaled = vectorScaling(direction, ratio)

    for angle in [math.radians(angle1), -math.radians(angle2)]:
        rotated = vectorRotation(scaled, angle)
        new_end = [start[0] + rotated[0], start[1] + rotated[1]]
        #newColor = changeColor(color)
        pygame.draw.line(screen, color, start, new_end, 1)
        draw_linesR(screen, color, new_end, rotated, n + 1, N)


def main():

    #get users screen size
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    x_padding = 10

    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height), pygame.RESIZABLE)
    title_fnt = pygame.font.SysFont('consolas', 56)
    frstAngle_fnt = pygame.font.Font(None, 40)
    secAngle_fnt = pygame.font.Font(None, 40)
    usr_frstAngle_txt = 'First Angle'
    usr_secAngle_txt = 'Second Angle'
    pygame.display.set_caption("Fractal Canopy")
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    clock = pygame.time.Clock()
    run = True

    x = screen_width / 2    #start in the middle
    y = (screen_height) /2

    #set up first branch
    color = (57,255,20) #neon green color
    start = [x, screen_height]
    end = [x, y]
    n = 1

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #close if ESC is pressed
                    run = False
            #if event.type == pygame.KEYDOWN

        screen.fill("black")
        #render section

        rendered_title = title_fnt.render("Fractal Canopy", True, (255,255,255))
        rendered_frstAngle = frstAngle_fnt.render(usr_frstAngle_txt, True, (255,255,255))
        rendered_secAngle = secAngle_fnt.render(usr_secAngle_txt, True, (255,255,255))

        screen.blit(rendered_title, (x_padding, 10))
        screen.blit(rendered_frstAngle, (x_padding, screen_height / 2))
        screen.blit(rendered_secAngle, (x_padding, screen_height / 1.7))

        pygame.draw.line(screen, (57,255,20), start, end, 1)
        initial_direction = [0, -(screen_height / 4)] # Vector pointing upward
        draw_linesR(screen, color, end, initial_direction, n, max_generations)
        
        #end render section
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
