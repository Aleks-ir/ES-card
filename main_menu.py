import socket
import time

import pygame

import constants
import strings_en
import strings_ru
from game_button import Image_button
import settings


class Menu:

    def __init__(self, mainSurface):

        self.reset_server_settings()
        self.init_sound()
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.menuSurface = mainSurface
        self.fpsClock = pygame.time.Clock()
        self.run = True
        self.is_animation_up = False
        self.is_animation_down = False
        self.type_menu = 1
        self.save_type_menu = 1
        self.type_info_menu = 2
        self.is_start_game = False
        self.is_first_menu = True
        self.is_exit = False
        self.is_draw_buttons = False
        self.guidance_number = 0
        self.myfont = pygame.font.SysFont(constants.MONOTYPECORSIVA, 25)
        self.is_draw_info_text = False
        self.guidance_button = Image_button(False, constants.POINT_IMG, 0, 0)
        self.menu_bg = pygame.image.load(constants.MENU_BG_IMG)
        self.menu_group = pygame.sprite.Group()
        self.menu = pygame.image.load(constants.MENU_IMG)
        self.velosity = 30
        self.y = -540
        self.type_box = settings.type_box
        self.type_card = settings.type_card
        self.type_bg = settings.type_bg
        self.type_cp = settings.type_cp
        self.card_img = settings.card_view_img
        self.bg_img = settings.bg_view_img
        self.box_img = settings.box_view_img
        self.cp_img = settings.cp_view_img
        self.init_object()
        self.load_settings()


    def reset_server_settings(self):
        settings.type_game = constants.EMPEROR
        settings.mode_game = constants.NORMAL
        settings.count_round = 10

    def init_sound(self):
        self.sound_menu = pygame.mixer.Sound(constants.SOUND_MENU).play(-1)
        self.sound_menu.set_volume(0.1)
        self.sound_click = pygame.mixer.Sound(constants.SOUND_CLICK)
        self.sound_click.set_volume(1)

    def init_object(self):
        self.language_btn = Image_button(False, constants.BTN_RU_IMG, 640, 20)
        self.btn_music = Image_button(False, constants.BTN_MUSIC_ON_IMG, 570, 20)
        self.start_btn = Image_button(True, constants.BUTTON_OFF_IMG, 250, 100, strings_ru.start_game, 40, constants.BLACK, constants.GABRIOLA)
        self.options_btn = Image_button(True, constants.BUTTON_OFF_IMG, 250, 180, strings_ru.options, 40, constants.BLACK, constants.GABRIOLA)
        self.about_game_btn = Image_button(True, constants.BUTTON_OFF_IMG, 250, 260, strings_ru.about_game, 40, constants.BLACK, constants.GABRIOLA)
        self.quit_btn = Image_button(True, constants.BUTTON_OFF_IMG, 250, 340, strings_ru.quit, 40, constants.BLACK, constants.GABRIOLA)
        self.main_menu_buttons = (
        self.language_btn, self.btn_music, self.start_btn, self.options_btn, self.about_game_btn, self.quit_btn)
        self.server_btn = Image_button(True, constants.BUTTON_OFF_IMG, 250, 50, strings_ru.server, 35, constants.BLACK, constants.GABRIOLA)
        self.client_btn = Image_button(True, constants.BUTTON_OFF_IMG, 250, 130, strings_ru.client, 35, constants.BLACK, constants.GABRIOLA)
        self.back_btn = Image_button(True, constants.BUTTON_OFF_IMG, 250, 450, strings_ru.back, 40, constants.BLACK, constants.GABRIOLA)
        self.net_menu_buttons = (self.server_btn, self.client_btn, self.back_btn)
        self.accept_btn = Image_button(True, constants.BUTTON_OFF_IMG, 250, 370, strings_ru.accept, 40, constants.BLACK, constants.GABRIOLA)

        self.heading_play_as = Image_button(False, constants.HEADING_SMALL_IMG, 110, 100, strings_ru.play_as, 30, constants.BLACK, constants.MONOTYPECORSIVA)
        self.left_btn_one = Image_button(False, constants.BTN_LEFT_IMG, 110, 170, strings_ru.emperor, 20, constants.BLACK, constants.GABRIOLA)
        self.left_btn_two = Image_button(False, constants.BTN_LEFT_IMG, 110, 230, strings_ru.slave, 20, constants.BLACK, constants.GABRIOLA)
        self.point_left = Image_button(False, constants.POINT_IMG, 240, 180)

        self.heading_mode = Image_button(False, constants.HEADING_SMALL_IMG, 510, 100, strings_ru.mode, 30, constants.BLACK, constants.MONOTYPECORSIVA)
        self.right_btn_one = Image_button(False, constants.BTN_RIGHT_IMG, 570, 170, strings_ru.usual, 20, constants.BLACK, constants.GABRIOLA)
        self.right_btn_two = Image_button(False, constants.BTN_RIGHT_IMG, 570, 230, strings_ru.with_change, 20, constants.BLACK, constants.GABRIOLA)
        self.point_right = Image_button(False, constants.POINT_IMG, 530, 180)

        self.heading_count_rounds = Image_button(False, constants.HEADING_SMALL_IMG, 310, 100, strings_ru.count_round, 30, constants.BLACK, constants.MONOTYPECORSIVA)
        self.next_btn = Image_button(False, constants.BTN_NEXT_OFF_IMG, 430, 180)
        self.prev_btn = Image_button(False, constants.BTN_PREV_OFF_IMG, 340, 180)
        self.square = Image_button(False, constants.SQUARE_IMG, 370, 170, str(settings.count_round), 20, constants.BLACK, constants.GABRIOLA)

        self.center_btn = Image_button(False, constants.BTN_CENTER_ON_IMG if settings.is_multiplayer else constants.BTN_CENTER_OFF_IMG, 350, 280, "", 20)
        self.title_server = Image_button(False, constants.PAPER_TITLE_IMG, 275, 10, strings_ru.server, 35, constants.BLACK, constants.TITLE_FONT)

        self.server_menu_buttons = (self.title_server, self.accept_btn, self.back_btn, self.center_btn,
                                    self.heading_play_as, self.left_btn_one, self.left_btn_two, self.point_left,
                                    self.heading_mode, self.right_btn_one, self.right_btn_two, self.point_right,
                                    self.heading_count_rounds, self.square, self.next_btn, self.prev_btn)

        self.title_client = Image_button(False, constants.PAPER_TITLE_IMG, 275, 10, strings_ru.client, 35, constants.BLACK, constants.TITLE_FONT)
        self.heading_ip = Image_button(False, constants.HEADING_BIG_LEFT_IMG, 100, 150, strings_ru.info_ip, 20, constants.BLACK, constants.MONOTYPECORSIVA)
        self.field_ip = Image_button(False, constants.FIELD_IP_LEFT_IMG, 130, 220, "", 25, constants.BLACK, constants.TITLE_FONT)
        self.heading_last_ip = Image_button(False, constants.HEADING_BIG_RIGTH_IMG, 410, 150, strings_ru.info_last_ip, 20, constants.BLACK, constants.MONOTYPECORSIVA)
        self.last_ip_btn = Image_button(False, constants.FIELD_IP_RIGTH_OFF_IMG, 420, 220, settings.server_ip, 25, constants.BLACK, constants.TITLE_FONT)
        self.client_menu_buttons = (
        self.title_client, self.accept_btn, self.back_btn, self.heading_ip, self.field_ip, self.heading_last_ip,
        self.last_ip_btn)

        self.title_options = Image_button(False, constants.PAPER_TITLE_IMG, 275, 10, strings_ru.options, 35, constants.BLACK, constants.TITLE_FONT)
        self.prev_btn_background_view = Image_button(False, constants.BTN_PREV_OFF_IMG, 290, 260)
        self.background_view = Image_button(False, self.bg_img, 330, 230)
        self.next_btn_background_view = Image_button(False, constants.BTN_NEXT_OFF_IMG, 480, 260)
        self.prev_btn_box_view = Image_button(False, constants.BTN_PREV_OFF_IMG, 120, 120)
        self.box_view = Image_button(False, self.box_img, 165, 90)
        self.next_btn_box_view = Image_button(False, constants.BTN_NEXT_OFF_IMG, 250, 120)
        self.prev_btn_card_view = Image_button(False, constants.BTN_PREV_OFF_IMG, 320, 120)
        self.card_view = Image_button(False, self.card_img, 365, 90)
        self.next_btn_card_view = Image_button(False, constants.BTN_NEXT_OFF_IMG, 450, 120)
        self.prev_btn_cp_view = Image_button(False, constants.BTN_PREV_OFF_IMG, 520, 120)
        self.cp_view = Image_button(False, self.cp_img, 565, 90)
        self.next_btn_cp_view = Image_button(False, constants.BTN_NEXT_OFF_IMG, 650, 120)
        self.options_menu_buttons = (self.title_options, self.accept_btn, self.back_btn,
                                     self.prev_btn_card_view, self.card_view, self.next_btn_card_view,
                                     self.prev_btn_box_view, self.box_view, self.next_btn_box_view,
                                     self.prev_btn_background_view, self.background_view, self.next_btn_background_view,
                                     self.prev_btn_cp_view, self.cp_view, self.next_btn_cp_view)

        self.title_info = Image_button(False, constants.PAPER_TITLE_IMG, 250, 10, strings_ru.about_game, 35, constants.BLACK, constants.TITLE_FONT)
        self.about_cards_btn = Image_button(False, constants.PAPER_INFO_OFF_IMG, 100, 20, strings_ru.about_cards, 25, constants.BLACK, constants.GABRIOLA)
        self.rules_game_btn = Image_button(False, constants.PAPER_INFO_ON_IMG, 300, 20, strings_ru.rules_game, 25, constants.BLACK, constants.GABRIOLA)
        self.control_btn = Image_button(False, constants.PAPER_INFO_OFF_IMG, 500, 20, strings_ru.control, 25, constants.BLACK, constants.GABRIOLA)
        self.info_menu_buttons = (self.back_btn, self.about_cards_btn, self.rules_game_btn, self.control_btn)
        self.about_cards_text = strings_ru.array_about_cards
        self.rules_game_text = strings_ru.array_rules_game
        self.control_text = strings_ru.array_control
        self.about_author_text = strings_ru.array_about_author
        self.array_info_text = (self.about_cards_text, self.rules_game_text, self.control_text, self.about_author_text)


        self.array_items = (self.start_btn, self.options_btn, self.about_game_btn, self.quit_btn,
                            self.server_btn, self.client_btn, self.back_btn, self.accept_btn,
                            self.heading_play_as, self.heading_count_rounds, self.heading_mode,
                            self.left_btn_one, self.left_btn_two, self.right_btn_one, self.right_btn_two,
                            self.title_server, self.title_client, self.title_options, self.title_info,
                            self.heading_ip, self.heading_last_ip,
                            self.about_cards_btn, self.rules_game_btn, self.control_btn)
    def show_menu(self):
        while self.run:
            self.fpsClock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif self.is_draw_buttons:
                    self.lisen_events(event)
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
            if self.is_draw_info_text:
                self.draw_info_text()
            if self.is_draw_buttons:
                self.draw_buttons(self.determine_group(self.type_menu))
            pygame.display.flip()

        if self.is_exit:
            return False
        else:
            return True

    def load_settings(self):
        self.type_menu = settings.type_menu
        self.set_language(settings.language)
        if settings.is_music:
            self.turn_volume(self.sound_menu, 0.1)
            self.turn_volume(self.sound_click, 1)
        else:
            self.turn_volume(self.sound_menu, 0)
            self.turn_volume(self.sound_click, 0)

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
            if self.is_exit or self.is_start_game:
                self.is_animation_up = False
                self.run = False
            else:
                time.sleep(0.2)
                self.is_animation_down = True
                self.is_animation_up = False
                self.type_menu = self.save_type_menu


    def move_down(self):
        self.y += self.velosity
        if self.y == 0:
            self.is_animation_down = False
            self.is_draw_buttons = True
            self.is_first_menu = False
            if self.type_menu == 6:
                self.is_draw_info_text = True


    def draw_buttons(self, current_group_buttons):
        for btn in current_group_buttons:
            btn.draw(self.menuSurface)


    def lisen_events(self, event):
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
            self.is_exit = True
            self.is_draw_buttons = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sound_click.play()
            if self.start_btn.isOver(pos):
                self.is_animation_up = True
                self.save_type_menu = 2
            elif self.options_btn.isOver(pos):
                self.load_options()
                self.is_animation_up = True
                self.save_type_menu = 5
            elif self.about_game_btn.isOver(pos):
                self.is_animation_up = True
                self.save_type_menu = 6
            elif self.quit_btn.isOver(pos):
                self.is_exit = True
                self.is_draw_buttons = False
            elif self.language_btn.isOver(pos):
                self.change_language()
            elif self.btn_music.isOver(pos):
                if settings.is_music:
                    settings.is_music = False
                    self.turn_volume(self.sound_menu, 0)
                    self.turn_volume(self.sound_click, 0)
                else:
                    settings.is_music = True
                    self.turn_volume(self.sound_menu, 0.1)
                    self.turn_volume(self.sound_click, 1)

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
                self.next_btn.change_image(constants.BTN_NEXT_OFF_IMG)
            elif self.prev_btn.isOver(pos):
                self.prev_btn.change_image(constants.BTN_PREV_OFF_IMG)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sound_click.play()
            if self.accept_btn.isOver(pos):
                self.start_server()
            elif self.back_btn.isOver(pos):
                self.cancel_server()
            elif self.next_btn.isOver(pos) and settings.count_round >= 2 and settings.count_round < 30:
                self.next_btn.change_image(constants.BTN_NEXT_ON_IMG)
                settings.count_round += 2
                self.square.text = str(settings.count_round)
            elif self.prev_btn.isOver(pos) and settings.count_round > 2 and settings.count_round <= 30:
                self.prev_btn.change_image(constants.BTN_PREV_ON_IMG)
                settings.count_round -= 2
                self.square.text = str(settings.count_round)
            elif self.left_btn_one.isOver(pos):
                self.point_left.y = 180
                settings.type_game = constants.EMPEROR
            elif self.left_btn_two.isOver(pos):
                self.point_left.y = 240
                settings.type_game = constants.SLAVE
            elif self.right_btn_one.isOver(pos):
                self.point_right.y = 180
                settings.mode_game = constants.NORMAL
            elif self.right_btn_two.isOver(pos):
                self.point_right.y = 240
                settings.mode_game = constants.CHANGE
            elif self.center_btn.isOver(pos):
                if settings.is_multiplayer:
                    self.center_btn.change_image(constants.BTN_CENTER_OFF_IMG)
                    settings.is_multiplayer = False
                else:
                    self.center_btn.change_image(constants.BTN_CENTER_ON_IMG)
                    settings.is_multiplayer = True
        if event.type == pygame.MOUSEMOTION:
            self.guidance(self.server_menu_buttons, pos)

    def start_server(self):
        settings.server_ip = self.HOST
        settings.is_server = True
        settings.type_menu = self.type_menu
        self.is_start_game = True
        self.sound_menu.stop()
        self.is_animation_up = True

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
            self.sound_click.play()
            if self.accept_btn.isOver(pos) and self.field_ip.text != '':
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
                self.last_ip_btn.change_image(constants.FIELD_IP_RIGTH_ON_IMG)
            else:
                self.last_ip_btn.change_image(constants.FIELD_IP_RIGTH_OFF_IMG)
        if event.type == pygame.MOUSEMOTION:
            self.guidance(self.client_menu_buttons, pos)

    def start_client(self):
        settings.is_server = False
        settings.type_menu = self.type_menu
        self.is_start_game = True
        self.sound_menu.stop()
        self.is_animation_up = True

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
            if self.next_btn_box_view.isOver(pos):
                self.next_btn_box_view.change_image(constants.BTN_NEXT_OFF_IMG)
            elif self.prev_btn_box_view.isOver(pos):
                self.prev_btn_box_view.change_image(constants.BTN_PREV_OFF_IMG)
            elif self.next_btn_card_view.isOver(pos):
                self.next_btn_card_view.change_image(constants.BTN_NEXT_OFF_IMG)
            elif self.prev_btn_card_view.isOver(pos):
                self.prev_btn_card_view.change_image(constants.BTN_PREV_OFF_IMG)
            elif self.next_btn_background_view.isOver(pos):
                self.next_btn_background_view.change_image(constants.BTN_NEXT_OFF_IMG)
            elif self.prev_btn_background_view.isOver(pos):
                self.prev_btn_background_view.change_image(constants.BTN_PREV_OFF_IMG)
            elif self.next_btn_cp_view.isOver(pos):
                self.next_btn_cp_view.change_image(constants.BTN_NEXT_OFF_IMG)
            elif self.prev_btn_cp_view.isOver(pos):
                self.prev_btn_cp_view.change_image(constants.BTN_PREV_OFF_IMG)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sound_click.play()
            if self.accept_btn.isOver(pos):
                self.save_options()
                self.is_animation_up = True
                self.save_type_menu = 1
            elif self.back_btn.isOver(pos):
                self.is_animation_up = True
                self.save_type_menu = 1
            elif self.next_btn_box_view.isOver(pos):
                self.next_btn_box_view.change_image(constants.BTN_NEXT_ON_IMG)
                self.type_box += 1
                self.change_box_image(self.type_box)
                self.update_view(self.box_view, self.box_img)
            elif self.prev_btn_box_view.isOver(pos):
                self.prev_btn_box_view.change_image(constants.BTN_PREV_ON_IMG)
                self.type_box -= 1
                self.change_box_image(self.type_box)
                self.update_view(self.box_view, self.box_img)
            elif self.next_btn_card_view.isOver(pos):
                self.next_btn_card_view.change_image(constants.BTN_NEXT_ON_IMG)
                self.type_card += 1
                self.change_card_image(self.type_card)
                self.update_view(self.card_view, self.card_img)
            elif self.prev_btn_card_view.isOver(pos):
                self.prev_btn_card_view.change_image(constants.BTN_PREV_ON_IMG)
                self.type_card -= 1
                self.change_card_image(self.type_card)
                self.update_view(self.card_view, self.card_img)
            elif self.next_btn_background_view.isOver(pos):
                self.next_btn_background_view.change_image(constants.BTN_NEXT_ON_IMG)
                self.type_bg += 1
                self.change_bg_image(self.type_bg)
                self.update_view(self.background_view, self.bg_img)
            elif self.prev_btn_background_view.isOver(pos):
                self.prev_btn_background_view.change_image(constants.BTN_PREV_ON_IMG)
                self.type_bg -= 1
                self.change_bg_image(self.type_bg)
                self.update_view(self.background_view, self.bg_img)
            elif self.next_btn_cp_view.isOver(pos):
                self.next_btn_cp_view.change_image(constants.BTN_NEXT_ON_IMG)
                self.type_cp += 1
                self.change_cp_image(self.type_cp)
                self.update_view(self.cp_view, self.cp_img)
            elif self.prev_btn_cp_view.isOver(pos):
                self.prev_btn_cp_view.change_image(constants.BTN_PREV_ON_IMG)
                self.type_cp -= 1
                self.change_cp_image(self.type_cp)
                self.update_view(self.cp_view, self.cp_img)
        if event.type == pygame.MOUSEMOTION:
            self.guidance(self.options_menu_buttons, pos)

    def load_options(self):
        self.type_card = settings.type_card
        self.type_bg = settings.type_bg
        self.type_cp = settings.type_cp
        self.card_view.change_image(settings.card_view_img)
        self.background_view.change_image(settings.bg_view_img)
        self.cp_view.change_image(settings.cp_view_img)

    def save_options(self):
        settings.type_box = self.type_box
        settings.type_bg = self.type_bg
        settings.type_card = self.type_card
        settings.type_cp = self.type_cp
        settings.box_view_img = self.box_img
        settings.card_view_img = self.card_img
        settings.bg_view_img = self.bg_img
        settings.cp_view_img = self.cp_img

    def change_box_image(self, type):
        if type % 3 == 0:
            self.box_img = constants.BOX_VIEW_IMG_1
        elif type % 3 == 1:
            self.box_img = constants.BOX_VIEW_IMG_2
        elif type % 3 == 2:
            self.box_img = constants.BOX_VIEW_IMG_3

    def change_card_image(self, type):
        if type % 2 == 0:
            self.card_img = constants.CARD_VIEW_IMG_1
        elif type % 2 == 1:
            self.card_img = constants.CARD_VIEW_IMG_2

    def change_bg_image(self, type):
        if type % 3 == 0:
            self.bg_img = constants.BG_VIEW_IMG_1
        elif type % 3 == 1:
            self.bg_img = constants.BG_VIEW_IMG_2
        elif type % 3 == 2:
            self.bg_img = constants.BG_VIEW_IMG_3

    def change_cp_image(self, type):
        if type % 3 == 0:
            self.cp_img = constants.CP_VIEW_IMG_1
        elif type % 3 == 1:
            self.cp_img = constants.CP_VIEW_IMG_2
        elif type % 3 == 2:
            self.cp_img = constants.CP_VIEW_IMG_3

    def update_view(self, view, img_way):
        view.change_image(img_way)


    def info_menu(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYUP and event.key == 27:
            self.is_animation_up = True
            self.save_type_menu = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_btn.isOver(pos):
                self.is_draw_info_text = False
                self.is_animation_up = True
                self.save_type_menu = 1
            elif self.about_cards_btn.isOver(pos):
                if self.type_info_menu == 1:
                    self.about_cards_btn.change_image(constants.PAPER_INFO_OFF_IMG)
                    self.type_info_menu = 0
                    pass
                else:
                    self.type_info_menu = 1
                    self.about_cards_btn.change_image(constants.PAPER_INFO_ON_IMG)
                    self.rules_game_btn.change_image(constants.PAPER_INFO_OFF_IMG)
                    self.control_btn.change_image(constants.PAPER_INFO_OFF_IMG)
            elif self.rules_game_btn.isOver(pos):
                if self.type_info_menu == 2:
                    self.rules_game_btn.change_image(constants.PAPER_INFO_OFF_IMG)
                    self.type_info_menu = 0
                    pass
                else:
                    self.type_info_menu = 2
                    self.about_cards_btn.change_image(constants.PAPER_INFO_OFF_IMG)
                    self.rules_game_btn.change_image(constants.PAPER_INFO_ON_IMG)
                    self.control_btn.change_image(constants.PAPER_INFO_OFF_IMG)
            elif self.control_btn.isOver(pos):
                if self.type_info_menu == 3:
                    self.control_btn.change_image(constants.PAPER_INFO_OFF_IMG)
                    self.type_info_menu = 0
                    pass
                else:
                    self.type_info_menu = 3
                    self.about_cards_btn.change_image(constants.PAPER_INFO_OFF_IMG)
                    self.rules_game_btn.change_image(constants.PAPER_INFO_OFF_IMG)
                    self.control_btn.change_image(constants.PAPER_INFO_ON_IMG)
        if event.type == pygame.MOUSEMOTION:
            self.guidance(self.info_menu_buttons, pos)

    def draw_info_text(self):
        if self.type_info_menu == 0:
            for i in range(len(strings_ru.array_about_author)):
                self.menuSurface.blit(self.myfont.render(self.about_author_text[i], True, constants.BLACK),
                                      (300, 150 + i * 40))
        if self.type_info_menu == 1:
            for i in range(len(strings_ru.array_about_cards)):
                self.menuSurface.blit(self.myfont.render(self.about_cards_text[i], True, constants.BLACK),
                                  (150, 130 + i * 40))
        elif self.type_info_menu == 2:
            for i in range(len(strings_ru.array_rules_game)):
                self.menuSurface.blit(self.myfont.render(self.rules_game_text[i], True, constants.BLACK),
                                  (150, 100 + i * 40))
        elif self.type_info_menu == 3:
            for i in range(len(strings_ru.array_control)):
                self.menuSurface.blit(self.myfont.render(self.control_text[i], True, constants.BLACK),
                                      (150, 150 + i * 40))

    def guidance(self, list, pos):
        for btn in list:
            if btn.with_guidance:
                if btn.isOver(pos):
                    btn.image = pygame.image.load(constants.BUTTON_ON_IMG)
                    self.guidance_button = btn
                    self.guidance_number += 1
                else:
                    btn.image = pygame.image.load(constants.BUTTON_OFF_IMG)

        if not self.guidance_button.isOver(pos):
            self.guidance_number = 0
        if self.guidance_number == 1:
            self.sound_click.play()


    def change_language(self):
        if settings.language == constants.RU:
            settings.language = constants.EN
            self.set_language(constants.EN)
        elif settings.language == constants.EN:
            settings.language = constants.RU
            self.set_language(constants.RU)

    def set_language(self, language):
        if language == constants.RU:
            self.language_btn.change_image(constants.BTN_RU_IMG)
            self.set_info_text(strings_ru)
            for item in enumerate(self.array_items):
                item[1].text = strings_ru.array_menu_strings[item[0]]
        elif language == constants.EN:
            self.language_btn.change_image(constants.BTN_EN_IMG)
            self.set_info_text(strings_en)
            for item in enumerate(self.array_items):
                item[1].text = strings_en.array_menu_strings[item[0]]

    def set_info_text(self, strings):
        self.about_author_text = strings.array_about_author
        self.about_cards_text = strings.array_about_cards
        self.rules_game_text = strings.array_rules_game
        self.control_text = strings.array_control

    def turn_volume(self, sound, volume):
        sound.set_volume(volume)
        if volume != 0:
            self.btn_music.change_image(constants.BTN_MUSIC_ON_IMG)
        else:
            self.btn_music.change_image(constants.BTN_MUSIC_OFF_IMG)