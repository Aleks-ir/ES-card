import pygame

from game_button import Button
from settings import BLUE


class Options:

    def __init__(self, menuSurface):
        self.options_surface = menuSurface
        self.fpsClock = pygame.time.Clock()
        self.run = True
        self.menu_bg = pygame.image.load('img/options.png')

        self.back_btn = Button(BLUE, 300, 50, 300, 70, 'Назад')

    def show_menu(self):
        while self.run:
            self.fpsClock.tick(30)
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == 27:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_btn.isOver(pos):
                        return
            self.options_surface.blit(self.menu_bg, (0, 0))
            self.back_btn.draw(self.options_surface)
            pygame.display.flip()