import pygame

from game import Game
from main_menu import Menu
from settings import SIZE



if __name__ == '__main__':
    pygame.init()
    mainSurface = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("ES-card")
    menu = Menu(mainSurface)
    game = Game(mainSurface)
    run = True
    while run:
        run = menu.show_menu()
        if run:
            run = game.play()
    pygame.quit()