import pygame
import math

from modules.vectorManip import vectorRotation, vectorScaling
        
class Slider:
    def __init__(self, rect, font, label, sliderType):
        self.rect = rect
        self.font = font
        self.label = label
        self.sliderType = sliderType

        if sliderType == "ratio":
            self.value = 0.65
            self.min_value = 0.0
            self.max_value = 1.0
        else:
            self.value = 0
            self.min_value = 0
            self.max_value = 180

        self.handle_radius = 8
        self.bar_color = (255, 255, 255)
        self.handle_color = (57, 255, 20)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_hitbox().collidepoint(event.pos):
                self.active = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.active = False
        elif event.type == pygame.MOUSEMOTION:
            if self.active:
                pos = max(self.rect.left, min(event.pos[0], self.rect.right))
                percent = (pos - self.rect.left) / self.rect.w

                if self.sliderType == "ratio":
                    self.value = round(self.min_value + percent * (self.max_value - self.min_value), 2)
                else:
                    self.value = round(self.min_value + percent * (self.max_value - self.min_value))

    def handle_hitbox(self):
        x = self.rect.left + (self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.w
        y = self.rect.centery
        sliderRect = pygame.Rect(x - self.handle_radius, y - self.handle_radius, self.handle_radius * 2, self.handle_radius * 2)

        return sliderRect

    def draw(self, screen):

        pygame.draw.line(screen, self.bar_color, (self.rect.left, self.rect.centery), (self.rect.right, self.rect.centery), 4)

        x = self.rect.left + (self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.w
        pygame.draw.circle(screen, self.handle_color, (int(x), self.rect.centery), self.handle_radius)

        if self.sliderType == "ratio":
            label_text = f"{self.label}: {self.value:.2f}"
        else:
            label_text = f"{self.label}: {self.value}°"

        renderedSlider = self.font.render(label_text, True, (255, 255, 255))
        screen.blit(renderedSlider, (self.rect.x, self.rect.y - self.font.get_height() - 5))

    def get_value(self):
        return self.value
    
    def update_label(self, new_label):
        self.label = new_label

class FractalTree:
    def __init__(self, screen_size, max_gen , angle1, angle2, left_ratio, right_ratio, is_triary):
        self.screen_size = screen_size
        self.start = []
        self.end = []
        self.max_gen = max_gen
        self.frst_angle = angle1
        self.sec_angle = angle2
        self.angles = [math.radians(self.frst_angle), -math.radians(self.sec_angle)]

        self.left_ratio = left_ratio
        self.right_ratio = right_ratio
        
        self.base_color = (57, 255, 20)
        self.animating = False
        self.current_gen = 1
        self.branch_thickness = 1
        self.is_triary = is_triary

    def reset(self):
        self.current_gen = 1
        self.animating = True

    def update_angles(self, angle1, angle2):
        self.frst_angle = angle1
        self.sec_angle = angle2
        self.angles = [math.radians(self.frst_angle), -math.radians(self.sec_angle)]

        self.reset()

    def update_ratios(self, left_ratio, right_ratio):
        self.left_ratio = left_ratio
        self.right_ratio = right_ratio
        self.reset()

    def draw(self, screen):
        direction = [self.end[0] - self.start[0], self.end[1] - self.start[1]]
        normdepth = 1 / self.max_gen
        trunk_color = self.color_linIntpltn((255, 190, 150), (0, 255, 0), normdepth)
        pygame.draw.line(screen, trunk_color, self.start, self.end, self.branch_thickness)

        self.draw_recursive(screen, self.end, direction, 2)

    def animate_step(self):
        if self.animating:
            self.current_gen += 1
            if self.current_gen > self.max_gen:
                self.animating = False

    def is_animating(self):
        return self.animating
    
    def color_linIntpltn(self, brownColor: tuple[int,int,int], greenColor: tuple[int,int,int], normdepth: int) -> tuple[int, int, int]:
        return (
            int(brownColor[0] + (greenColor[0] - brownColor[0]) * normdepth),
            int(brownColor[1] + (greenColor[1] - brownColor[1]) * normdepth),
            int(brownColor[2] + (greenColor[2] - brownColor[2]) * normdepth),
        )

    def draw_recursive(self, screen, start, direction, curr_gen):
        if curr_gen > self.current_gen or curr_gen > self.max_gen:
            return
        
        if curr_gen >= self.max_gen:
            return

        normdepth = curr_gen / self.max_gen
        color = self.color_linIntpltn((255, 190, 150), (0, 255, 0), normdepth)
        
        ratios = [self.right_ratio, self.left_ratio]
        
        if self.is_triary:

            mid_scaled = vectorScaling(direction, self.left_ratio)
            mid_end = [start[0] + mid_scaled[0], start[1] + mid_scaled[1]]
            pygame.draw.line(screen, color, start, mid_end, self.branch_thickness)
            self.draw_recursive(screen, mid_end, mid_scaled, curr_gen + 1)

        for i, angle in enumerate(self.angles):
            scaled = vectorScaling(direction, ratios[i])
            rotated = vectorRotation(scaled, angle)
            new_end = [start[0] + rotated[0], start[1] + rotated[1]]
            pygame.draw.line(screen, color, start, new_end, self.branch_thickness)
            self.draw_recursive(screen, new_end, rotated, curr_gen + 1)

    def is_Ftriary(self):
        return self.is_triary
    
    def update_triary(self, new_triary):
        self.is_triary = new_triary

    def initialize_fractal(self):
        x = self.screen_size[0] / 2
        self.start = [x, self.screen_size[1]]
        self.end = [x, (self.screen_size[1]) * self.left_ratio]

class Button:
    def __init__(self, rect, font, text, on_click = None):
        self.rect = rect
        self.font = font
        self.text = text
        self.on_click = on_click

        self.base_color = (255, 255, 255)
        self.hover_color = (128, 128, 128)
        self.click_color = (57, 255, 20)
        self.text_color = (0, 0, 0)

        self.hovered = False
        self.clicked = False
    
    def draw(self, screen):
        
        if self.clicked:
            color = self.click_color
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.base_color

        pygame.draw.rect(screen, color, self.rect)

        rendered_text = self.font.render(self.text, True, self.text_color)
        self.rect.w = max(10, rendered_text.get_width() + 10)

        text_rect = rendered_text.get_rect(center=self.rect.center)
        screen.blit(rendered_text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and event.button == 1:
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.clicked and self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
            self.clicked = False

    def update_text(self, new_text):
        self.text = new_text