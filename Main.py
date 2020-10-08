import pygame

from main_loop import Main_loop
from main_menu import Menu
from settings import SIZE



if __name__ == '__main__':
    pygame.init()
    mainSurface = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("ES-card")
    #menu = Menu(mainSurface)
    game = Main_loop(mainSurface)
    run = True
    while run:
        run = Menu(mainSurface).show_menu()
        if run:
            run = game.start()
    pygame.quit()