import pygame

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
            else:
                self.active = False
            self.color = self.color_inactive if self.active else self.color_inactive

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

    def get_value(self, default = 30):
        try:
            return float(self.text)
        except ValueError:
            return default

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
        