#   Interactive Fractal Canopy Visualization
#   Author: Octavio Araujo Rosales

import pygame
import os
import ctypes

from modules.fractals import Slider, FractalTree, Button

def main():

    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Fractal Canopy")
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont('consolas', int(screen_height * 0.04))
    slider_font = pygame.font.SysFont('consolas', int(screen_height * 0.02))
    button_font = pygame.font.SysFont('consolas', int(screen_height * 0.025))

    x_padding = int(screen_width * 0.01)
    txtBox_width = int(screen_width * 0.05)
    y_padding = int(screen_height * 0.01)

    title_height = title_font.get_height()
    button_height = button_font.get_height()
    slider_height = slider_font.get_height() + 10

    right_slider_x = screen_width - (txtBox_width * 4 + x_padding)

    export_y = title_height + (y_padding * 2)
    toggle_y = export_y + button_height + y_padding
    triary_toggle_y = toggle_y + button_height + y_padding

    slider_y = screen_height - slider_height - y_padding
    ratio_slider_y = slider_y - slider_height - (2.5 * y_padding)

    rightAngle_slider = Slider(
        pygame.Rect(right_slider_x, slider_y, txtBox_width * 4, slider_height),
        slider_font,
        "Right Angle",
        "angle"
    )

    leftAngle_slider = Slider(
        pygame.Rect(x_padding, slider_y, txtBox_width * 4, slider_height),
        slider_font,
        "Left Angle",
        "angle"
    )

    leftRatio_Slider = Slider(
        pygame.Rect(x_padding , ratio_slider_y, txtBox_width * 4, slider_height),
        slider_font,
        "Left Ratio",
        "ratio"
    )

    rightRatio_Slider = Slider(
        pygame.Rect(right_slider_x, ratio_slider_y, txtBox_width * 4, slider_height),
        slider_font,
        "Right Ratio",
        "ratio"
    )

    save_button = Button(
        pygame.Rect(x_padding, export_y, txtBox_width * 2, button_height),
        button_font,
        "Save Fractal As Image",
        on_click = lambda: pygame.image.save(screen, "pictures/fractal_export.png")
    )

    is_symmetric = True
    def toggle_mode():
        nonlocal is_symmetric
        is_symmetric = not is_symmetric

    toggle_button = Button(
        pygame.Rect(x_padding, toggle_y, txtBox_width * 2, button_height),
        button_font,
        "Symmetric Tree Mode" if is_symmetric else "Asymmetric Tree Mode",
        on_click = toggle_mode
    )

    is_triary = False
    def toggle_triary():
        nonlocal is_triary
        is_triary = not is_triary

    triary_toggle_button = Button(
        pygame.Rect(x_padding, triary_toggle_y, txtBox_width * 2, button_height),
        button_font,
        "Triary Tree Mode" if is_symmetric else "Binary Tree Mode",
        on_click = toggle_triary
    )
    
    fractal = FractalTree(
        (screen_width, screen_height),
        9,
        rightAngle_slider.get_value(),
        leftAngle_slider.get_value(),
        leftRatio_Slider.get_value(),
        rightRatio_Slider.get_value(),
        is_triary
    )

    fractal.initialize_fractal()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            
            if not fractal.is_animating():
                leftAngle_slider.handle_event(event)
                leftRatio_Slider.handle_event(event)
                if not is_symmetric:
                    rightAngle_slider.handle_event(event)
                    rightRatio_Slider.handle_event(event)
                save_button.handle_event(event)
                toggle_button.handle_event(event)
                triary_toggle_button.handle_event(event)

        screen.fill("black")
        #render section

        rendered_title = title_font.render("Fractal Canopy", True, (255, 255, 255))
        screen.blit(rendered_title, (x_padding, y_padding))

        new_left_angle = leftAngle_slider.get_value()
        new_left_ratio = leftRatio_Slider.get_value()
        if is_symmetric:
            new_right_ratio = new_left_ratio
            new_right_angle = new_left_angle
        else:
            new_right_ratio = rightRatio_Slider.get_value()
            new_right_angle = rightAngle_slider.get_value()

        if fractal.is_Ftriary() != is_triary:
            fractal.update_triary(is_triary)
            fractal.reset()

        if (new_right_angle != fractal.frst_angle or new_left_angle != fractal.sec_angle) and not fractal.is_animating():
            fractal.update_angles(new_right_angle, new_left_angle)

        if (new_left_ratio != fractal.left_ratio or new_right_ratio != fractal.right_ratio) and not fractal.is_animating():
            fractal.update_ratios(new_left_ratio, new_right_ratio)

        save_button.draw(screen)

        if is_triary:
            triary_toggle_button.update_text("Triary Tree Mode")
        else:
            triary_toggle_button.update_text("Binary Tree Mode")

        if is_symmetric:
            toggle_button.update_text("Symmetric Tree Mode")
            leftAngle_slider.update_label("Angle")
            leftRatio_Slider.update_label("Ratio")
            triary_toggle_button.draw(screen)

        else:
            toggle_button.update_text("Asymmetric Tree Mode")
            leftAngle_slider.update_label("Left Angle")
            leftRatio_Slider.update_label("Left Ratio")
            rightRatio_Slider.draw(screen)
            rightAngle_slider.draw(screen)
            if is_triary:
                toggle_triary()
                
        toggle_button.draw(screen)
        leftAngle_slider.draw(screen)
        leftRatio_Slider.draw(screen)

        fractal.draw(screen)
        fractal.animate_step()

        #end render section
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()