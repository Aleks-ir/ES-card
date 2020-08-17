import pygame


class Game_over:

    def __init__(self, menuSurface):
        self.info_surface = menuSurface
        self.fpsClock = pygame.time.Clock()
        self.run = True
        self.menu_bg = pygame.image.load('img/info.png')

    def show_menu(self):
        while self.run:
            self.fpsClock.tick(30)
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == 27:
                    pass
            self.info_surface.blit(self.menu_bg, (0, 0))
            pygame.display.flip()