#   Fractal Canopy Visualization
#   Author: Octavio Araujo Rosales
#   Date: 05/28/2025
#   Last edited: 05/29/2025

import pygame
import os
import ctypes

from custLinAlg import *

ratio = .66
angle1 = 45
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
    pygame.display.set_caption("Fractal Canopy")
    clock = pygame.time.Clock()
    title_fnt = pygame.font.SysFont('consolas', 56)
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    usr_frstAngle_txt = '30'
    frstAngle_fnt = pygame.font.SysFont('consolas', 40)
    frstAngle_rect = pygame.Rect(x_padding, 20, 60, 40)
    is_activeFrstAngle = False

    usr_secAngle_txt = '60'
    secAngle_fnt = pygame.font.SysFont('consolas', 40)
    secAngle_rect = pygame.Rect(x_padding, 80, 60, 40)
    is_activeSecAngle = False


    x = screen_width / 2    #start in the middle
    y = (screen_height) /2

    #set up first branch
    color = (57,255,20) #neon green color
    start = [x, screen_height]
    end = [x, y]
    n = 1

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #close if ESC is pressed
                    run = False
                if is_activeFrstAngle:
                    if event.key == pygame.K_BACKSPACE:
                        usr_frstAngle_txt = usr_frstAngle_txt[:-1]
                    else:
                        usr_frstAngle_txt += event.unicode
                if is_activeSecAngle:
                    if event.key == pygame.K_BACKSPACE:
                        usr_secAngle_txt = usr_secAngle_txt[:-1]
                    else:
                        usr_secAngle_txt += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if frstAngle_rect.collidepoint(event.pos):
                    is_activeFrstAngle = True
                else:
                    is_activeFrstAngle = False
                if secAngle_rect.collidepoint(event.pos):
                    is_activeSecAngle = True
                else:
                    is_activeSecAngle = False

        screen.fill("black")
        #render section

        if is_activeFrstAngle:
            color_FrstAngle = pygame.Color(255,255,255)
        else:
            color_FrstAngle = pygame.Color(57,255,20)

        if is_activeSecAngle:
            color_SecAngle = pygame.Color(255,255,255)
        else:
            color_SecAngle = pygame.Color(57,255,20)

        pygame.draw.rect(screen, color_FrstAngle, frstAngle_rect, 4) #draw first anglebox
        pygame.draw.rect(screen, color_SecAngle, secAngle_rect, 4) #draw second anglebox

        rendered_title = title_fnt.render("Fractal Canopy", True, (255,255,255))
        rendered_frstAngle = frstAngle_fnt.render(usr_frstAngle_txt, True, (255,255,255))
        rendered_secAngle = secAngle_fnt.render(usr_secAngle_txt, True, (255,255,255))

        screen.blit(rendered_title, (x_padding, 10))
        screen.blit(rendered_frstAngle, (frstAngle_rect.x + 5, frstAngle_rect.y + 5))
        screen.blit(rendered_secAngle, (secAngle_rect.x + 5, secAngle_rect.y + 5))
        
        frstAngle_rect.w = max(50, rendered_frstAngle.get_width() + 10)
        secAngle_rect.w = max(50, rendered_secAngle.get_width() + 10)


        pygame.draw.line(screen, (57,255,20), start, end, 1)
        initial_direction = [0, -(screen_height / 4)] # Vector pointing upward
        draw_linesR(screen, color, end, initial_direction, n, max_generations)
        
        #end render section
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
