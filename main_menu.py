import socket
import time

import pygame

import strings_en
import strings_ru
from game_button import Simple_button, Image_button
from game_objects import Background
from info_menu import Info
from options_menu import Options
from settings import BLUE, BLACK
import settings


class Menu:

    def __init__(self, mainSurface):
        self.sound_menu = pygame.mixer.Sound('sound_menu.wav').play(-1)
        self.sound_menu.set_volume(0.1)
        self.sound_click = pygame.mixer.Sound('sound_click.wav')
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.menuSurface = mainSurface
        self.fpsClock = pygame.time.Clock()
        self.run = True
        self.is_animation_up = False
        self.is_animation_down = False
        self.type_menu = 1
        self.save_type_menu = 1
        self.is_start_game = False
        self.is_first_menu = True
        self.is_exit = False
        self.is_draw_buttons = False
        self.guidance_number = 0
        self.guidance_button = Image_button(True, 'img/point.png', 0, 0)
        self.menu_bg = pygame.image.load('img/menu_bg.png')
        self.menu_group = pygame.sprite.Group()
        self.menu = pygame.image.load('img/menu.png')
        self.velosity = 30
        self.y = -540
        self.type_card = 1
        self.type_background = 1
        self.type_cp = 1
        self.card_img = settings.card_img
        self.background_img = settings.background_img
        self.cp_img = settings.cp_img

        self.myfont = pygame.font.SysFont('serif', 30)
        self.text_count_rounds = self.myfont.render('Количество раундов:', 1, (0, 0, 0))
        self.text_side = self.myfont.render('Сторона:', 1, (0, 0, 0))
        self.text_mode = self.myfont.render('Режим игры:', 1, (0, 0, 0))
        self.text_ip = self.myfont.render('Введите ip-адрес сервера:', 1, (0, 0, 0))

        self.language_btn = Image_button(False, 'img/btn_ru.png', 640, 20)
        self.music_btn = Image_button(False, 'img/btn_music_on.png', 570, 20)
        self.start_btn = Image_button(True, 'img/paper_button_off.png', 250, 100, strings_ru.start_game)
        self.options_btn = Image_button(True, 'img/paper_button_off.png', 250, 180, strings_ru.options)
        self.about_game_btn = Image_button(True, 'img/paper_button_off.png', 250, 260, strings_ru.about_game)
        self.quit_btn = Image_button(True, 'img/paper_button_off.png', 250, 340, strings_ru.quit)
        self.main_menu_buttons = (self.language_btn, self.music_btn, self.start_btn, self.options_btn, self.about_game_btn, self.quit_btn)
        self.server_btn = Image_button(True, 'img/paper_button_off.png', 250, 50, strings_ru.server)
        self.client_btn = Image_button(True, 'img/paper_button_off.png', 250, 130, strings_ru.client)
        self.back_btn = Image_button(True, 'img/paper_button_off.png', 250, 450, strings_ru.back)
        self.net_menu_buttons = (self.server_btn, self.client_btn, self.back_btn)
        self.accept_btn = Image_button(True, 'img/paper_button_off.png', 250, 370, strings_ru.accept)

        self.heading_play_as = Image_button(False, 'img/heading_small.png', 110, 100, strings_ru.play_as)
        self.left_btn_one = Image_button(False, 'img/btn_left_off.png', 110, 170, strings_ru.emperor, 20)
        self.left_btn_two = Image_button(False, 'img/btn_left_off.png', 110, 230, strings_ru.slave, 20)
        self.point_left = Image_button(False,'img/point.png', 240, 180)

        self.heading_mode = Image_button(False, 'img/heading_small.png', 510, 100, strings_ru.mode)
        self.right_btn_one = Image_button(False, 'img/btn_right_off.png', 570, 170, strings_ru.usual, 20)
        self.right_btn_two = Image_button(False, 'img/btn_right_off.png', 570, 230, strings_ru.with_change, 20)
        self.point_right = Image_button(False, 'img/point.png', 530, 180)

        self.heading_count_rounds = Image_button(False, 'img/heading_small.png', 310, 100, strings_ru.count_round, 30)
        self.next_btn = Image_button(False, 'img/btn_next_off.png', 430, 210)
        self.prev_btn = Image_button(False, 'img/btn_prev_off.png', 340, 210)
        self.square = Image_button(False, 'img/square.png', 370, 200, "10", 20)

        self.title_server = Image_button(False, 'img/paper.png', 250, 0, strings_ru.server)

        self.server_menu_buttons = (self.title_server, self.accept_btn, self.back_btn,
                                    self.heading_play_as, self.left_btn_one, self.left_btn_two, self.point_left,
                                    self.heading_mode, self.right_btn_one, self.right_btn_two, self.point_right,
                                    self.heading_count_rounds, self.square, self.next_btn, self.prev_btn)

        self.title_client = Image_button(False, 'img/paper.png', 250, 0, strings_ru.client)
        self.heading_ip = Image_button(False, 'img/heading_big_left.png', 100, 150, strings_ru.info_ip, 25)
        self.field_ip = Image_button(False, 'img/field_ip_left.png', 130, 220, "", 30)
        self.heading_last_ip = Image_button(False, 'img/heading_big_rigth.png', 410, 150, strings_ru.info_last_ip, 25)
        self.last_ip_btn = Image_button(False, 'img/field_ip_rigth_off.png', 420, 220, settings.server_ip, 30)
        self.client_menu_buttons = (self.title_client, self.accept_btn, self.back_btn, self.heading_ip, self.field_ip, self.heading_last_ip, self.last_ip_btn)

        self.title_options = Image_button(False,'img/paper.png', 250, 0, strings_ru.options)
        self.prev_btn_options_1 = Image_button(False, 'img/btn_prev_off.png', 110, 200)
        self.card_view = Image_button(False, self.card_img, 150, 170)
        self.next_btn_options_1 = Image_button(False,'img/btn_next_off.png', 230, 200)
        self.prev_btn_options_2 = Image_button(False, 'img/btn_prev_off.png', 290, 200)
        self.background_view = Image_button(False, self.background_img, 330, 170)
        self.next_btn_options_2 = Image_button(False,'img/btn_next_off.png', 480, 200)
        self.prev_btn_options_3 = Image_button( False,'img/btn_prev_off.png', 540, 200)
        self.cp_view = Image_button(False, self.cp_img, 580, 170)
        self.next_btn_options_3 = Image_button(False, 'img/btn_next_off.png', 660, 200)
        self.options_menu_buttons = (self.title_options, self.accept_btn, self.back_btn,
                                     self.next_btn_options_1, self.card_view, self.prev_btn_options_1,
                                     self.next_btn_options_2, self.background_view, self.prev_btn_options_2,
                                     self.next_btn_options_3, self.cp_view, self.prev_btn_options_3)

        self.title_info = Image_button(False, 'img/paper.png', 250, 0, strings_ru.about_game)
        self.info_menu_buttons = (self.title_info, self.back_btn)

        self.connection_info = Image_button(False, 'img/connection_info.png', 250, 0, "Ожидайте подключения")

        self.array_items = (self.start_btn, self.options_btn, self.about_game_btn, self.quit_btn,
                             self.server_btn, self.client_btn, self.back_btn, self.accept_btn,
                            self.heading_play_as, self.heading_count_rounds, self.heading_mode,
                             self.left_btn_one, self.left_btn_two, self.right_btn_one, self.right_btn_two,
                             self.title_server, self.title_client, self.title_options, self.title_info,
                             self.heading_ip, self.heading_last_ip)

    def show_menu(self):
        self.is_first_menu = True
        while self.run:
            self.fpsClock.tick(30)
            current_group_buttons = self.determine_group(self.type_menu)
            if not self.is_animation_up and not self.is_animation_down:
                self.lisen_events()
            if self.is_start_game:
                return True
            if self.is_first_menu:
                self.move_down()
            elif self.is_exit:
                self.move_up()
            if self.is_animation_up:
                self.is_draw_buttons = False
                self.move_up()
            elif self.is_animation_down:
                self.move_down()

            self.menuSurface.blit(self.menu_bg, (0, 0))
            self.menuSurface.blit(self.menu, (50, self.y))
            if self.is_draw_buttons:
                self.draw_buttons(current_group_buttons)


            pygame.display.flip()
        return False

    def determine_group(self, type_menu):
        if type_menu == 1:
            return self.main_menu_buttons
        elif type_menu == 2:
            return self.net_menu_buttons
        elif type_menu == 3:
            return self.server_menu_buttons
        elif type_menu == 4:
            return self.client_menu_buttons
        elif type_menu == 5:
            return self.options_menu_buttons
        elif type_menu == 6:
            return self.info_menu_buttons

    def move_up(self):
        self.y -= self.velosity
        if self.y < -550:
            time.sleep(0.2)
            if self.is_exit:
                self.run = False
            self.is_animation_down = True
            self.is_animation_up = False
            self.type_menu = self.save_type_menu


    def move_down(self):
        self.y += self.velosity
        if self.y == 0:
            self.is_animation_down = False
            self.is_draw_buttons = True
            self.is_first_menu = False


    def draw_text(self):
        if self.type_menu == 3:
            pass
            #self.menuSurface.blit(self.text_count_rounds, (50, 50 + self.y))
            #self.menuSurface.blit(self.text_side, (50, 150 + self.y))
            #self.menuSurface.blit(self.text_mode, (50, 250 + self.y))
        elif self.type_menu == 4:
            pass
            #self.menuSurface.blit(self.text_ip, (50, 150 + self.y))

    def draw_buttons(self, current_group_buttons):
        for btn in current_group_buttons:
            btn.draw(self.menuSurface)


    def lisen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 self.run = False
            if self.type_menu == 1:
                self.main_menu(event)
            elif self.type_menu == 2:
                 self.net_menu(event)
            elif self.type_menu == 3:
                self.server_menu(event)
            elif self.type_menu == 4:
                 self.client_menu(event)
            elif self.type_menu == 5:
                 self.options_menu(event)
            elif self.type_menu == 6:
                 self.info_menu(event)


    def main_menu(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYUP and event.key == 27:
            self.run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sound_click.play()
            if self.start_btn.isOver(pos):
                self.is_animation_up = True
                self.save_type_menu = 2
            elif self.options_btn.isOver(pos):
                self.download_settings()
                self.is_animation_up = True
                self.save_type_menu = 5
            elif self.about_game_btn.isOver(pos):
                self.is_animation_up = True
                self.save_type_menu = 6
            elif self.quit_btn.isOver(pos):
                self.is_exit = True
                self.is_draw_buttons = False
                self.move_up()
            elif self.language_btn.isOver(pos):
                if settings.language == "ru":
                    self.language_btn.change_image('img/btn_en.png')
                    settings.language = "en"
                elif settings.language == "en":
                    self.language_btn.change_image('img/btn_ru.png')
                    settings.language = "ru"
                self.change_language(settings.language)
            elif self.music_btn.isOver(pos):
                if settings.music == "on":
                    self.sound_menu.set_volume(0)
                    self.music_btn.change_image('img/btn_music_off.png')
                    settings.music = "off"
                elif settings.music == "off":
                    self.sound_menu.set_volume(0.1)
                    self.music_btn.change_image('img/btn_music_on.png')
                    settings.music = "on"
                self.change_language(settings.language)

        elif event.type == pygame.MOUSEMOTION:
            self.guidance(self.main_menu_buttons, pos)

    def net_menu(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYUP and event.key == 27:
            self.is_animation_up = True
            self.save_type_menu = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.server_btn.isOver(pos):
                self.is_animation_up = True
                self.save_type_menu = 3
            elif self.client_btn.isOver(pos):
                self.last_ip_btn.text = settings.server_ip
                self.is_animation_up = True
                self.save_type_menu = 4
            elif self.back_btn.isOver(pos):
                self.is_animation_up = True
                self.save_type_menu = 1
        if event.type == pygame.MOUSEMOTION:
            self.guidance(self.net_menu_buttons, pos)

    def server_menu(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                self.start_server()
            elif event.key == pygame.K_ESCAPE:
                self.cancel_server()
        if event.type == pygame.MOUSEBUTTONUP:
            if self.next_btn.isOver(pos):
                self.next_btn.change_image('img/btn_next_off.png')
            elif self.prev_btn.isOver(pos):
                self.prev_btn.change_image('img/btn_prev_off.png')
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.accept_btn.isOver(pos):
                self.start_server()
            elif self.back_btn.isOver(pos):
                self.cancel_server()
            elif self.next_btn.isOver(pos):
                self.next_btn.change_image('img/btn_next_on.png')
                count = int(self.square.text) + 2
                settings.count_round = count
                self.square.text = str(count)
            elif self.prev_btn.isOver(pos):
                self.prev_btn.change_image('img/btn_prev_on.png')
                count = int(self.square.text) - 2
                settings.count_round = count
                self.square.text = str(count)
            elif self.left_btn_one.isOver(pos):
                self.point_left.y = 180
                settings.type_game = "Emperor"
            elif self.left_btn_two.isOver(pos):
                self.point_left.y = 240
                settings.type_game = "Slave"
            elif self.right_btn_one.isOver(pos):
                self.point_right.y = 180
                settings.mode_game = "Normal"
            elif self.right_btn_two.isOver(pos):
                self.point_right.y = 240
                settings.mode_game = "Change"
        if event.type == pygame.MOUSEMOTION:
            self.guidance(self.server_menu_buttons, pos)

    def start_server(self):
        settings.server_ip = self.HOST
        settings.is_server = True
        self.is_start_game = True
        self.is_draw_buttons = False
        self.sound_menu.stop()

    def cancel_server(self):
        self.is_animation_up = True
        self.save_type_menu = 2

    def client_menu(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                settings.server_ip = self.field_ip.text
                self.start_client()
            elif event.key == pygame.K_ESCAPE:
                self.cancel_client()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.accept_btn.isOver(pos):
                settings.server_ip = self.field_ip.text
                self.start_client()
            elif self.back_btn.isOver(pos):
                self.cancel_client()
            elif self.last_ip_btn.isOver(pos):
                self.start_client()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PERIOD:
                self.field_ip.text += "."
            elif event.key == pygame.K_BACKSPACE:
                self.field_ip.text = self.field_ip.text[:-1]
            elif event.key == pygame.K_0:
                self.field_ip.text += "0"
            elif event.key == pygame.K_1:
                self.field_ip.text += "1"
            elif event.key == pygame.K_2:
                self.field_ip.text += "2"
            elif event.key == pygame.K_3:
                self.field_ip.text += "3"
            elif event.key == pygame.K_4:
                self.field_ip.text += "4"
            elif event.key == pygame.K_5:
                self.field_ip.text += "5"
            elif event.key == pygame.K_6:
                self.field_ip.text += "6"
            elif event.key == pygame.K_7:
                self.field_ip.text += "7"
            elif event.key == pygame.K_8:
                self.field_ip.text += "8"
            elif event.key == pygame.K_9:
                self.field_ip.text += "9"
            if len(self.field_ip.text) > 15:
                self.field_ip.text = self.field_ip.text[:-1]

        if event.type == pygame.MOUSEMOTION:
            if self.last_ip_btn.isOver(pos):
                self.last_ip_btn.change_image('img/field_ip_rigth_on.png')
            else:
                self.last_ip_btn.change_image('img/field_ip_rigth_off.png')
        if event.type == pygame.MOUSEMOTION:
            self.guidance(self.client_menu_buttons, pos)

    def start_client(self):
        settings.is_server = False
        self.is_start_game = True
        self.is_draw_buttons = False
        self.sound_menu.stop()

    def cancel_client(self):
        self.is_animation_up = True
        self.save_type_menu = 2
        self.field_ip.text = ""

    def options_menu(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYUP and event.key == 27:
            self.is_animation_up = True
            self.save_type_menu = 1
        if event.type == pygame.MOUSEBUTTONUP:
            if self.next_btn_options_1.isOver(pos):
                self.next_btn_options_1.change_image('img/btn_next_off.png')
            elif self.prev_btn_options_1.isOver(pos):
                self.prev_btn_options_1.change_image('img/btn_prev_off.png')
            elif self.next_btn_options_2.isOver(pos):
                self.next_btn_options_2.change_image('img/btn_next_off.png')
            elif self.prev_btn_options_2.isOver(pos):
                self.prev_btn_options_2.change_image('img/btn_prev_off.png')
            elif self.next_btn_options_3.isOver(pos):
                self.next_btn_options_3.change_image('img/btn_next_off.png')
            elif self.prev_btn_options_3.isOver(pos):
                self.prev_btn_options_3.change_image('img/btn_prev_off.png')
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.accept_btn.isOver(pos):
                self.save_settings()
                self.is_animation_up = True
                self.save_type_menu = 1
            elif self.back_btn.isOver(pos):
                self.is_animation_up = True
                self.save_type_menu = 1
            elif self.next_btn_options_1.isOver(pos):
                self.next_btn_options_1.change_image('img/btn_next_on.png')
                self.type_card += 1
                self.save_card_image(self.type_card)
                self.update_view(self.card_view, self.card_img)
            elif self.prev_btn_options_1.isOver(pos):
                self.prev_btn_options_1.change_image('img/btn_prev_on.png')
                self.type_card -= 1
                self.save_card_image(self.type_card)
                self.update_view(self.card_view, self.card_img)
            elif self.next_btn_options_2.isOver(pos):
                self.next_btn_options_2.change_image('img/btn_next_on.png')
                self.type_background += 1
                self.save_background_image(self.type_background)
                self.update_view(self.background_view, self.background_img)
            elif self.prev_btn_options_2.isOver(pos):
                self.prev_btn_options_2.change_image('img/btn_prev_on.png')
                self.type_background -= 1
                self.save_background_image(self.type_background)
                self.update_view(self.background_view, self.background_img)
            elif self.next_btn_options_3.isOver(pos):
                self.next_btn_options_3.change_image('img/btn_next_on.png')
                self.type_cp += 1
                self.save_cp_image(self.type_cp)
                self.update_view(self.cp_view, self.cp_img)
            elif self.prev_btn_options_3.isOver(pos):
                self.prev_btn_options_3.change_image('img/btn_prev_on.png')
                self.type_cp -= 1
                self.save_cp_image(self.type_cp)
                self.update_view(self.cp_view, self.cp_img)
        if event.type == pygame.MOUSEMOTION:
            self.guidance(self.options_menu_buttons, pos)

    def download_settings(self):
        self.type_card = settings.type_card
        self.type_background = settings.type_background
        self.type_cp = settings.type_cp
        self.card_view.change_image(settings.card_img)
        self.background_view.change_image(settings.background_img)
        self.cp_view.change_image(settings.cp_img)

    def save_settings(self):
        settings.type_background = self.type_background
        settings.type_card = self.type_card
        settings.type_cp = self.type_cp
        settings.card_img = self.card_img
        settings.background_img = self.background_img
        settings.cp_img = self.cp_img

    def save_card_image(self, type):
        if type % 2 == 0:
            self.card_img = 'img/card_view_2.png'
        elif type % 2 == 1:
            self.card_img = 'img/card_view_1.png'

    def save_background_image(self, type):
        if type % 3 == 0:
            self.background_img = 'img/bg_view_3.png'
        elif type % 3 == 1:
            self.background_img = 'img/bg_view_1.png'
        elif type % 3 == 2:
            self.background_img = 'img/bg_view_2.png'

    def save_cp_image(self, type):
        if type % 3 == 0:
            self.cp_img = 'img/cp_view_3.png'
        elif type % 3 == 1:
            self.cp_img = 'img/cp_view_1.png'
        elif type % 3 == 2:
            self.cp_img = 'img/cp_view_2.png'

    def update_view(self, view, img_way):
        view.change_image(img_way)


    def info_menu(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYUP and event.key == 27:
            self.is_animation_up = True
            self.save_type_menu = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_btn.isOver(pos):
                self.is_animation_up = True
                self.save_type_menu = 1
        if event.type == pygame.MOUSEMOTION:
            self.guidance(self.info_menu_buttons, pos)

    def guidance(self, list, pos):
        for btn in list:
            if btn.is_mutable:
                if btn.isOver(pos):
                    btn.image = pygame.image.load('img/paper_button_off.png')
                    btn.font_size = 45
                    self.guidance_button = btn
                    self.guidance_number += 1
                else:
                    btn.image = pygame.image.load('img/paper_button_on.png')
                    btn.font_size = 40

        if not self.guidance_button.isOver(pos):
            self.guidance_number = 0
        if self.guidance_number == 1:
            self.sound_click.play()


    def change_language(self, language):
        if language == "en":
            for item in enumerate(self.array_items):
                item[1].text = strings_en.array_strings[item[0]]
        elif language == "ru":
            for item in enumerate(self.array_items):
                item[1].text = strings_ru.array_strings[item[0]]