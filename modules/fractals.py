import pygame
import math

from modules.custLinAlg import *

class TextBox:
    def __init__(self, rect, font, default_text=''):
        self.rect = rect
        self.font = font
        self.text = default_text
        self.active = False
        self.color_active = pygame.Color(57, 255, 20)
        self.color_inactive = pygame.Color(255, 255, 255)
        self.color = self.color_inactive


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.text = ''
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isnumeric() or event.unicode in ['.', '-']:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 4)
        rendered_text = self.font.render(self.text, True, self.color)
        screen.blit(rendered_text, (self.rect.x + 5, self.rect.y + 5))
        self.rect.w = max(50, rendered_text.get_width() + 10)

    def get_value(self):
        default = 30
        try:
            return float(self.text)
        except ValueError:
            self.text = '30'
            return default

class FractalTree:
    def __init__(self, screen_size, start, end, max_gen = 8, angle1 = 30, angle2 = 30, ratio = 0.6):
        self.screen_size = screen_size
        self.start = start
        self.end = end
        self.max_gen = max_gen
        self.frst_angle = angle1
        self.sec_angle2 = angle2
        self.angles = [math.radians(self.frst_angle), -math.radians(self.sec_angle2)]

        self.ratio = ratio
        
        self.base_color = (57, 255, 20)
        self.animating = False
        self.current_gen = 0
        self.branch_thickness = 1

    def reset(self):
        self.current_gen = 1
        self.animating = True

    def update_params(self, angle1, angle2, ratio, max_gen):
        self.frst_angle = angle1
        self.sec_angle = angle2
        self.angles = [math.radians(self.frst_angle), -math.radians(self.sec_angle2)]

        self.ratio = ratio
        self.max_gen = max_gen
        self.reset()

    def draw(self, screen):
        pygame.draw.line(screen, self.base_color, self.start, self.end, self.branch_thickness)
        direction = [self.end[0] - self.start[0], self.end[1] - self.start[1]]
        self._draw_recursive(screen, self.end, direction, 1, self.current_gen)

    def animate_step(self):
        if self.animating:
            self.current_gen += 1
            if self.current_gen > self.max_gen:
                self.animating = False

    def is_animating(self):
        return self.animating

    def _draw_recursive(self, screen, start, direction, n, N):

        if n > N:
            return
    
        scaled = vectorScaling(direction, self.ratio)
        for angle in self.angles:
            rotated = vectorRotation(scaled, angle)
            new_end = [start[0] + rotated[0], start[1] + rotated[1]]
            pygame.draw.line(screen, self.base_color, start, new_end, self.branch_thickness)
            self._draw_recursive(screen, new_end, rotated, n + 1, N)




        