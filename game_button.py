import pygame
from pygame.rect import Rect


class Simple_button:
    def __init__(self, color, x, y, width, height, text='', font_size = 40):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.font_size)
            text = font.render(self.text, 1, (0, 0, 0))
            surface.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True


class Image_button:
    def __init__(self,is_mutable, img_way, x, y, text='', font_size=40):
        self.is_mutable = is_mutable
        self.image = pygame.image.load(img_way)
        size = self.image.get_size()
        self.width = size[0]
        self.height = size[1]
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y, self.width, self.height))

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.font_size)
            text = font.render(self.text, 1, (0, 0, 0))
            surface.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


    def change_image(self, img_way):
        self.image = pygame.image.load(img_way)

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True