import pygame

class TextBox:
    def __init__(self, rect, font, default_text=''):
        self.rect = rect
        self.font = font
        self.text = default_text
        self.active = False

    def handle_event(self, event):
        pass

    def draw(self, screen):
        pass

    def get_value(self):
        pass

class FractalTree:
    def __init__(self, screen_size, start, end, max_gen = 8, angle1 = 30, angle2 = 30, ratio = 0.6):
        self.screen_size = screen_size
        self.start = start
        self.end = end
        self.max_gen = max_gen
        self.angle1 = angle1
        self.angle2 = angle2
        self.ratio = ratio
        self.animating = False
        self.current_gen = 0

    def draw(self, screen):
        pass

    def animate_stop(self):
        pass

    def reset(self):
        self.current_gen = 0
        self.animating = True

    def is_animating(self):
        return self.animating
        