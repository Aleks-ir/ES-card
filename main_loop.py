from threading import Thread

import pygame

import constants
import settings
import strings_en
import strings_ru
from bot_client import Bot
from game_button import Image_button
from game_objects import Game_objects


class Main_loop:
    def __init__(self, mainSurface, client):
        self.run = False
        array_settings = client.read().split('_')
        if array_settings[0] == constants.CONNECTED:
            settings.type_menu = 1
            self.client = client
            self.run = True
            self.FPS = 30
            self.mainSurface = mainSurface
            self.fpsClock = pygame.time.Clock()
            self.is_draw_dialogue = True
            self.retry_settings(array_settings[1], int(array_settings[2]), array_settings[3])
            self.game_object = Game_objects(self.mainSurface, client)
            self.my_cards = self.game_object.my_cards_group
            self.opp_cards = self.game_object.opp_cards_group
            self.all_background = self.game_object.background_group
            self.box = self.game_object.box_group
            self.init_dialogue_object()
            self.init_sound()
            if not settings.is_server:
                self.game_object.is_other_one_connected = True
            if not settings.is_multiplayer:
                self.bot = Bot()
                Thread(target=self.bot.start).start()


    def init_sound(self):
        self.sound_defeat = pygame.mixer.Sound(constants.DEFEAT_SOUND)
        self.sound_defeat.set_volume(0.4)
        self.sound_victory = pygame.mixer.Sound(constants.VICTORY_SOUND)
        self.sound_victory.set_volume(0.4)
        if self.game_object.is_for_emperor:
            self.sound = pygame.mixer.Sound(constants.SOUND_1).play(-1)
        else:
            self.sound = pygame.mixer.Sound(constants.SOUND_2).play(-1)
        if settings.is_music:
            self.turn_on_volume(self.sound)
        else:
            self.turn_off_volume(self.sound)


    def disconnect(self):
        self.game_object.run_receiver = False
        if not self.game_object.is_other_one_disconnected:
            self.client.write_sock(constants.SHUTDOWN)

    def retry_settings(self, type_game, count_rounds, mode_game):
        settings.type_game = type_game
        settings.count_round = count_rounds
        settings.mode_game = mode_game

    def init_dialogue_object(self):
        strings = strings_en if settings.language == constants.EN else strings_ru
        self.dialogue_connection = Image_button(False, constants.DIALOGUE_WINDOW_IMG, 200, 180, strings.info_connection + settings.server_ip, 30, constants.BLACK, constants.MONOTYPECORSIVA)
        self.dialogue_disconnection = Image_button(False, constants.DIALOGUE_WINDOW_IMG, 200, 180, strings.info_disconnection, 30, constants.BLACK, constants.MONOTYPECORSIVA)
        self.dialogue = Image_button(False, constants.DIALOGUE_WINDOW_IMG, 200, 180, "")
        self.btn_music = Image_button(False, constants.BTN_MUSIC_ON_IMG, 375, 210, "")
        self.btn_continue = Image_button(True, constants.BUTTON_ON_IMG, 250, 270, strings.continue_game, 30, constants.BLACK, constants.GABRIOLA)
        self.btn_main_menu = Image_button(True, constants.BUTTON_ON_IMG, 250, 340, strings.main_menu, 30, constants.BLACK, constants.GABRIOLA)
        self.menu_group = (self.dialogue, self.btn_main_menu, self.btn_continue, self.btn_music)
        self.text_victory = Image_button(False, constants.TEXT_IMG, 200, 180, strings.victory, 30, constants.BLACK, constants.MONOTYPECORSIVA)
        self.text_defeat = Image_button(False, constants.TEXT_IMG, 200, 180, strings.defeat, 30, constants.BLACK, constants.MONOTYPECORSIVA)
        self.game_over_group = [self.dialogue, self.btn_main_menu]


    def start(self):
        while self.run:
            self.fpsClock.tick(self.FPS)
            if self.game_object.is_last_round:
                self.supplement_game_over_group()
                self.play_game_over_sound()
                self.game_object.is_pause = True
                self.game_object.is_last_round = False
                if not settings.is_multiplayer:
                    self.bot.is_send_card = False
                    self.bot.run = False
            if self.game_object.is_change_sound:
                self.change_sound()
                self.game_object.is_change_sound = False
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self.disconnect()
                    return False
                self.lisen_events(event, pos)
                self.all_background, self.box, self.opp_cards, self.my_cards = self.game_object.get(event)

            self.draw_game_object()
            self.draw_dialogue()
            pygame.display.flip()
        return True

    def lisen_events(self, event, pos):
        if event.type == pygame.KEYUP and event.key == 27:
            if not self.game_object.is_game_over and self.game_object.is_pause:
                self.game_object.is_pause = False
            else:
                self.game_object.is_pause = True
        elif self.game_object.is_game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_main_menu.isOver(pos):
                if not settings.is_multiplayer:
                    self.bot.run = False
                self.disconnect()
                self.run = False
        elif self.game_object.is_pause and event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_main_menu.isOver(pos):
                if not settings.is_multiplayer:
                    self.bot.run = False
                self.disconnect()
                self.sound.stop()
                self.run = False
            elif self.btn_continue.isOver(pos):
                self.game_object.is_pause = False
            elif self.btn_music.isOver(pos):
                if settings.is_music:
                    settings.is_music = False
                    self.turn_off_volume(self.sound)
                else:
                    settings.is_music = True
                    self.turn_on_volume(self.sound)
        if event.type == pygame.MOUSEMOTION:
            self.guidance(self.menu_group, pos)

    def draw_game_object(self):
        self.all_background.draw(self.mainSurface)
        if len(self.box) == 2:
            self.box[0].draw(self.mainSurface)
            self.box[1].draw(self.mainSurface)
        self.opp_cards.draw(self.mainSurface)
        self.my_cards.draw(self.mainSurface)

    def draw_dialogue(self):
        if self.game_object.is_game_over:
            for item in self.game_over_group:
                item.draw(self.mainSurface)
        elif self.game_object.is_pause:
            for item in self.menu_group:
                item.draw(self.mainSurface)
        elif not self.game_object.is_other_one_connected:
            self.dialogue_connection.draw(self.mainSurface)
        elif self.game_object.is_other_one_disconnected:
            self.dialogue_disconnection.draw(self.mainSurface)

    def supplement_game_over_group(self):
        self.game_over_group.append(self.text_victory if self.game_object.my_score >= self.game_object.opp_score else self.text_defeat)

    def play_game_over_sound(self):
        if settings.is_music:
            self.sound.stop()
            self.sound_victory.play() if self.game_object.my_score >= self.game_object.opp_score else self.sound_defeat.play()

    def change_sound(self):
        self.sound.stop()
        if self.game_object.is_for_emperor:
            self.sound = pygame.mixer.Sound(constants.SOUND_1).play(-1)
        else:
            self.sound = pygame.mixer.Sound(constants.SOUND_2).play(-1)

    def turn_on_volume(self, sound):
        sound.set_volume(1)
        self.btn_music.change_image(constants.BTN_MUSIC_ON_IMG)

    def turn_off_volume(self, sound):
        sound.set_volume(0)
        self.btn_music.change_image(constants.BTN_MUSIC_OFF_IMG)

    def guidance(self, list, pos):
        for btn in list:
            if btn.with_guidance:
                if btn.isOver(pos):
                    btn.image = pygame.image.load(constants.BUTTON_ON_IMG)
                else:
                    btn.image = pygame.image.load(constants.BUTTON_OFF_IMG)