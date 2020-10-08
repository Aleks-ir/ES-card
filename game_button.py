import pygame

class Image_button:
    def __init__(self, with_guidance, img_way, x, y, text='', font_size=40, color=(0,0,0), font_preference = None):
        self.with_guidance = with_guidance
        self.image = pygame.image.load(img_way)
        size = self.image.get_size()
        self.width = size[0]
        self.height = size[1]
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font_preference = font_preference

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y, self.width, self.height))

        if self.text != '':
            font = self.make_font(self.font_preference, self.font_size)
            text = font.render(self.text, 1, self.color)
            surface.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def make_font(fonts, font_preferences, size):
        available = pygame.font.get_fonts()
        if font_preferences in available:
            return pygame.font.SysFont(font_preferences, size)
        return pygame.font.Font(None, size)

    def change_image(self, img_way):
        self.image = pygame.image.load(img_way)

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True