import pygame

from game_button import Button
from info_menu import Info
from options_menu import Options
from settings import BLUE, BLACK
import settings


class Menu:

    def __init__(self, mainSurface):

        self.menuSurface = mainSurface
        self.fpsClock = pygame.time.Clock()
        self.run = True
        self.is_first_menu = False
        self.is_start_game = False
        self.is_second_menu = False
        self.menu_bg = pygame.image.load('img/menu.png')

        self.start_btn = Button(BLUE, 300, 50, 300, 70, 'Начать игру')
        self.options_btn = Button(BLUE, 300, 150, 300, 70, 'Опции')
        self.info_btn = Button(BLUE, 300, 250, 300, 70, 'Об игре')
        self.quit_btn = Button(BLUE, 300, 350, 300, 70, 'Выход')
        self.btn_list = (self.start_btn, self.options_btn, self.info_btn, self.quit_btn)
        self.server_btn = Button(BLUE, 300, 50, 300, 70, 'Сервер')
        self.client_btn = Button(BLUE, 300, 150, 300, 70, 'Клиент')
        self.back_btn = Button(BLUE, 300, 350, 300, 70, 'Назад')
        self.btn_list_cs = (self.server_btn, self.client_btn, self.back_btn)

    def guidance(self, list, pos):
        for btn in list:
            if btn.isOver(pos):
                btn.color = BLACK
            else:
                btn.color = BLUE

    def show_menu(self):
        self.is_first_menu = True
        while self.run:
            self.fpsClock.tick(30)
            self.lisen_events()

            if self.is_start_game:
                self.is_start_game = False
                return True

            self.menuSurface.blit(self.menu_bg, (0, 0))
            self.draw_btns()
            pygame.display.flip()
        return False

    def draw_btns(self):
        if self.is_first_menu:
            for btn in self.btn_list:
                btn.draw(self.menuSurface)
        else:
            for btn in self.btn_list_cs:
                btn.draw(self.menuSurface)
        pygame.display.flip()

    def lisen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if self.is_first_menu:
                self.first_menu(event)
            elif self.is_second_menu:
                 self.second_menu(event)

    def first_menu(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYUP and event.key == 27:
            self.run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_btn.isOver(pos):
                self.is_first_menu = False
                self.is_second_menu = True
            elif self.quit_btn.isOver(pos):
                self.run = False
            elif self.options_btn.isOver(pos):
                options = Options(self.menuSurface)
                options.show_menu()
            elif self.info_btn.isOver(pos):
                info = Info(self.menuSurface)
                info.show_menu()
        elif event.type == pygame.MOUSEMOTION:
            self.guidance(self.btn_list, pos)

    def second_menu(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYUP and event.key == 27:
            self.is_first_menu = True
            self.is_second_menu = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.server_btn.isOver(pos):
                settings.is_server = True
                self.is_start_game = True
            elif self.client_btn.isOver(pos):
                settings.is_server = False
                self.is_start_game = True
            elif self.back_btn.isOver(pos):
                self.is_first_menu = True
                self.is_second_menu = False
        if event.type == pygame.MOUSEMOTION:
            self.guidance(self.btn_list_cs, pos)