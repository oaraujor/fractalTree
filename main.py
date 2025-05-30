#   Fractal Canopy Visualization
#   Author: Octavio Araujo Rosales
#   Date: 05/28/2025
#   Last edited: 05/29/2025

import pygame
import os
import ctypes

from custLinAlg import *

def draw_linesR(screen, color, start, direction, n, N):
    if n > N:
        return
    
    # Compute new direction
    scaled = vectorScaling(direction, 0.65)
    
    for angle in [math.radians(60), -math.radians(40)]:
        rotated = vectorRotation(scaled, angle)
        new_end = [start[0] + rotated[0], start[1] + rotated[1]]
        pygame.draw.line(screen, color, start, new_end, 1)
        draw_linesR(screen, color, new_end, rotated, n + 1, N)


def main():

    #get users screen size
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Fractal Canopy")
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    font = pygame.font.SysFont('consolas', 24)
    clock = pygame.time.Clock()
    run = True

    x = screen_width / 2    #start in the middle
    y = (screen_height) * 0.65

    #set up first branch
    color = (57,255,20)
    start = [x, screen_height]
    end = [x, y]
    n = 1
    max_generations = 8

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #close if ESC is pressed
                    run = False

        screen.fill("black")
        #render section

        text_surface = font.render("Fractal Canopy", True, (255,255,255))
        screen.blit(text_surface, (10,10))

        pygame.draw.line(screen, (57,255,20), start, end, 1)
        initial_direction = [0, -(screen_height / 4)] # Vector pointing upward
        draw_linesR(screen, color, end, initial_direction, n, max_generations)
        
        #end render section
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
