#   Interactive Fractal Canopy Visualization
#   Author: Octavio Araujo Rosales

import pygame
import os
import ctypes

from modules.fractals import Slider, FractalTree, Button

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

    title_font = pygame.font.SysFont('consolas', int(screen_height * 0.04))
    slider_font = pygame.font.SysFont('consolas', int(screen_height * 0.02))
    button_font = pygame.font.SysFont('consolas', int(screen_height * 0.025))

    # auto adjust txtbxs h, w and padding based on users screen size 
    x_padding = int(screen_width * 0.01)
    txtBox_width = int(screen_width * 0.05)
    y_padding = int(screen_height * 0.01)

    title_height = title_font.get_height()
    button_height = button_font.get_height()
    slider_height = slider_font.get_height() + 10

    right_slider_x = screen_width - (txtBox_width * 4 + x_padding)

    export_y = title_height + (y_padding * 2)
    slider_y = screen_height - slider_height - y_padding

    frstAngle_slider = Slider(
        pygame.Rect(right_slider_x, slider_y, txtBox_width * 4, slider_height),
        slider_font,
        "Right Angle",
    )
    secAngle_slider = Slider(
        pygame.Rect(x_padding, slider_y, txtBox_width * 4, slider_height),
        slider_font,
        "Left Angle",
    )

    save_button = Button(
        pygame.Rect(x_padding, export_y, txtBox_width * 2, button_height),
        button_font,
        "Save Fractal As Image",
        on_click = lambda: pygame.image.save(screen, "pictures/fractal_export.png")
    )

    # Fractal setup
    ratio = 0.65
    x = screen_width / 2
    start = [x, screen_height]
    end = [x, (screen_height) * ratio]

    fractal = FractalTree(
        (screen_width, screen_height),
        start,
        end,
        9, #number of generations
        frstAngle_slider.get_value(),
        secAngle_slider.get_value(),
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
                frstAngle_slider.handle_event(event)
                secAngle_slider.handle_event(event)
                save_button.handle_event(event)

        screen.fill("black")
        #render section

        rendered_title = title_font.render("Fractal Canopy", True, (255, 255, 255))
        screen.blit(rendered_title, (x_padding, y_padding))

        new_angle1 = frstAngle_slider.get_value()
        new_angle2 = secAngle_slider.get_value()

        if (new_angle1 != fractal.frst_angle or new_angle2 != fractal.sec_angle) and not fractal.is_animating():
            fractal.update_angles(new_angle1, new_angle2)

        if not fractal.is_animating():
            save_button.draw(screen)

        frstAngle_slider.draw(screen)
        secAngle_slider.draw(screen)
        fractal.draw(screen)
        fractal.animate_step()

        #end render section
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()