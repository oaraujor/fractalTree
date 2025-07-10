#   Interactive Fractal Canopy Visualization
#   Author: Octavio Araujo Rosales

import pygame
import os
import ctypes

from modules.fractals import TextBox, FractalTree

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
    button_font = pygame.font.SysFont('consolas', int(screen_height * 0.025))

    # auto adjust txtbxs h, w and padding based on users screen size 

    title_height = title_fnt.get_height()
    txtBox_height = font_tb.get_height() + 10
    spacing = int(screen_height * 0.01)

    title_y = spacing
    frstAngle_y = title_y + title_height + spacing
    secAngle_y = frstAngle_y + txtBox_height + spacing
    button_y = secAngle_y + txtBox_height + spacing
    export_y = button_y + txtBox_height + spacing

    x_padding = int(screen_width * 0.01)
    txtBox_width = int(screen_width * 0.05)

    # init txtboxes

    frstAngle_textbox = TextBox(
        pygame.Rect(x_padding, frstAngle_y, txtBox_width, txtBox_height),
        font_tb,
        '30'
        )
    secAngle_textbox = TextBox(
        pygame.Rect(x_padding, secAngle_y, txtBox_width, txtBox_height),
        font_tb,
        '30'
        )

    draw_button_rect = pygame.Rect(x_padding, button_y, txtBox_width * 2, txtBox_height)
    save_fractal_image = pygame.Rect(x_padding, export_y, txtBox_width * 2, txtBox_height)

    # set ratio
    ratio = 0.65

    #start in the middle
    x = screen_width / 2

    #set up for first branch
    start = [x, screen_height]
    end = [x, (screen_height) * ratio]

    # init fractal tree
    fractal = FractalTree(
        (screen_width, screen_height),
        start,
        end,
        9, #number of generations
        30,
        30,
        ratio
    )

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            
            if not fractal.is_animating():
                frstAngle_textbox.handle_event(event)
                secAngle_textbox.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if draw_button_rect.collidepoint(event.pos):
                        angle1 = frstAngle_textbox.get_value()
                        angle2 = secAngle_textbox.get_value()
                        fractal.update_angles(angle1, angle2)
                    if save_fractal_image.collidepoint(event.pos) and not fractal.is_animating():
                        pygame.image.save(screen, "fractal_export.png")

        screen.fill("black")
        #render section

        rendered_title = title_fnt.render("Fractal Canopy", True, (255, 255, 255))
        screen.blit(rendered_title, (x_padding, title_y))

        if not fractal.is_animating():
            frstAngle_textbox.draw(screen)
            secAngle_textbox.draw(screen)

        pygame.draw.rect(screen, (255, 255, 255), draw_button_rect)
        draw_text = button_font.render("Draw Fractal", True, (0, 0, 0))
        screen.blit(draw_text, (draw_button_rect.x + 5, draw_button_rect.y + 5))

        pygame.draw.rect(screen, (255, 255, 255), save_fractal_image)
        export_text = button_font.render("Save Fractal As Image", True, (0, 0, 0))
        screen.blit(export_text, (save_fractal_image.x + 5, save_fractal_image.y + 5))


        fractal.draw(screen)
        fractal.animate_step()

        #end render section
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()