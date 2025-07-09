#   Interactive Fractal Canopy Visualization
#   Author: Octavio Araujo Rosales

import pygame
import os
import ctypes

from custLinAlg import *
from fractals import *

def draw_linesR(screen, color, start, direction, n, N, angle1, angle2, ratio):
    if n > N:
        return
    
    # Compute new direction
    scaled = vectorScaling(direction, ratio)

    for angle in [math.radians(angle1), -math.radians(angle2)]:
        rotated = vectorRotation(scaled, angle)
        new_end = [start[0] + rotated[0], start[1] + rotated[1]]
        pygame.draw.line(screen, color, start, new_end, 4)
        draw_linesR(screen, color, new_end, rotated, n + 1, N, angle1, angle2, ratio)


def main():

    #get users screen size
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Fractal Canopy")
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    clock = pygame.time.Clock()

    title_fnt = pygame.font.SysFont('consolas', int(screen_height * 0.04))
    font_tb = pygame.font.SysFont('consolas', int(screen_height * 0.035))

    title_height = title_fnt.get_height()
    txtBox_height = font_tb.get_height() + 10
    spacing = int(screen_height * 0.01)

    title_y = spacing
    frstAngle_y = title_y + title_height + spacing
    secAngle_y = frstAngle_y + txtBox_height + spacing
    #button_y = secAngle_y + txtBox_height + spacing
    x_padding = int(screen_width * 0.01)
    txtBox_width = int(screen_width * 0.05)


    frstAngle_rect = pygame.Rect(x_padding, frstAngle_y, txtBox_width, txtBox_height)
    secAngle_rect = pygame.Rect(x_padding, secAngle_y, txtBox_width, txtBox_height)
    frstAngle_textbox = TextBox(frstAngle_rect, font_tb, default_text = '30')
    secAngle_textbox = TextBox(secAngle_rect, font_tb, default_text = '30')

    ratio = .60
    max_generations = 9
    color = (57,255,20) #neon green color

    #set up first branch
    x = screen_width / 2    #start in the middle
    y = (screen_height) * ratio
    start = [x, screen_height]
    end = [x, y]
    n = 1

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            
            frstAngle_textbox.handle_event(event)
            secAngle_textbox.handle_event(event)

        screen.fill("black")
        #render section

        #if is_activeFrstAngle:
            #color_FrstAngle = pygame.Color(57,255,20)
        #else:
            #color_FrstAngle = pygame.Color(255,255,255)

        #if is_activeSecAngle:
            #color_SecAngle = pygame.Color(57,255,20)
        #else:
            #color_SecAngle = pygame.Color(255,255,255)

        #pygame.draw.rect(screen, color_FrstAngle, frstAngle_rect, 4) #draw first anglebox
        #pygame.draw.rect(screen, color_SecAngle, secAngle_rect, 4) #draw second anglebox
        #pygame.draw.rect(screen, (255,255,255), updateButton_rect, 0) #draw update button

        rendered_title = title_fnt.render("Fractal Canopy", True, (255,255,255))
        screen.blit(rendered_title, (x_padding, title_y))

        frstAngle_textbox.draw(screen)
        secAngle_textbox.draw(screen)

        pygame.draw.line(screen, (57,255,20), start, end, 4)
        initial_direction = [end[0] - start[0], end[1] - start[1]]

        frst_angle = frstAngle_textbox.get_value()
        sec_angle = secAngle_textbox.get_value()


        draw_linesR(screen, color, end, initial_direction, n, max_generations, frst_angle, sec_angle, ratio)

        #rendered_frstAngle = frstAngle_fnt.render(usr_frstAngle_txt, True, color_FrstAngle)
        #rendered_secAngle = secAngle_fnt.render(usr_secAngle_txt, True, color_SecAngle)
        #rendered_updtBttn = updtButton_fnt.render("Update Fractal", True, (0,0,0))

        #screen.blit(rendered_frstAngle, (frstAngle_rect.x + 5, frstAngle_rect.y + 5))
        #screen.blit(rendered_secAngle, (secAngle_rect.x + 5, secAngle_rect.y + 5))
        #screen.blit(rendered_updtBttn, (updateButton_rect.x + 5, updateButton_rect.y + 5))

        #frstAngle_rect.w = max(50, rendered_frstAngle.get_width() + 10)
        #secAngle_rect.w = max(50, rendered_secAngle.get_width() + 10)
        #updateButton_rect.w = max(10, rendered_updtBttn.get_width() + 10)


        #try:
            #flt_fsrtAngle = float(usr_frstAngle_txt)
            #flt_secAngle = float(usr_secAngle_txt)
            #button
        #except ValueError:
            #flt_fsrtAngle = 30
            #flt_secAngle = 30




        
        #end render section
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()