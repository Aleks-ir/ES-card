from threading import Thread

import pygame
import time

import settings
from endgame_menu import Game_over
from game_button import Image_button


class Cards(pygame.sprite.Sprite):

    def __init__(self, filename, pos):
        super(Cards, self).__init__()
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def set_image(self, filename):
        self.image = pygame.image.load(filename)

    def update(self, event):
        keys = pygame.key.get_pressed()

        if event.type == pygame.MOUSEMOTION and event.buttons[0]:
            self.rect.center = event.pos


class Background(pygame.sprite.Sprite):
    def __init__(self, filename, pos):
        super(Background, self).__init__()
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.center = pos


class Game_objects:
    def receiver(self):
        while self.run_receiver:
            try:
                data = self.client.read()
                if data == "START":
                    self.is_pause = False
                    self.dialogue_group.clear()
                elif data == "WAIT":
                    print(data)
                    self.move_opp_card()
                else:
                    array_data = data.split('_')
                    self.open_my_card()
                    self.open_opp_card(array_data[1])
                    self.clear_field()
                    if array_data[0] != 'DRAW':
                        self.next_round(array_data[0])
            except:
                pass


    def __init__(self, mainSurface, client):
        self.client = client
        self.my_score = 0
        self.opp_score = 0
        self.count_cards = 5
        self.num_game = 1
        self.my_cards_group = pygame.sprite.Group()
        self.opp_cards_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()
        self.dialogue_group = []

        self.dialogue_connection = Image_button(False, 'img/dialogue_window.png', 255, 200, "Идет подключение...", 25)
        self.dialogue_group.append(self.dialogue_connection)

        self.background = self.init_backround()
        self.my_point_centre = Cards(settings.cp_img, settings.MY_POINT_CENTRE)
        self.opp_point_centre = Cards(settings.cp_img, settings.OPP_POINT_CENTRE)
        self.background_group.add(self.background, self.my_point_centre, self.opp_point_centre)
        self.init_side()
        self.init_my_cards()
        self.init_opp_cards(self.count_cards)

        self.my_selected_card = None
        self.card = None
        self.is_doMove = False
        self.is_card_selected = False
        self.run_receiver = True
        self.is_pause = True
        self.image_selected_card = self.emperor.image

        self.mainSurface = mainSurface
        #self.game_over = Game_over(self.mainSurface)
        self.over = False
        Thread(target=self.receiver).start()

    def clear_field(self):
        self.is_card_selected = False
        self.count_cards -= 1
        self.init_opp_cards(self.count_cards)
        time.sleep(1)
        self.my_point_centre.set_image(settings.cp_img)
        self.opp_point_centre.set_image(settings.cp_img)

    def move_opp_card(self):
        self.init_opp_cards(self.count_cards - 1)
        self.opp_point_centre.set_image(settings.OPPNENTS_CARDS_IMG)

    def open_my_card(self):
        self.my_point_centre.image = self.image_selected_card

    def open_opp_card(self, opp_card):
        if opp_card == 'EMPEROR':
            self.opp_point_centre.set_image(settings.EMPEROR_IMG)
        elif opp_card == 'SLAVE':
            self.opp_point_centre.set_image(settings.SLAVE_IMG)
        elif opp_card == 'CITIZER':
            self.opp_point_centre.set_image(settings.CITIZER_IMG)

    def init_backround(self):
        if settings.type_background == 1:
            return Background(settings.BACKGROUND_IMG_1, (400, 300))
        elif settings.type_background == 2:
            return Background(settings.BACKGROUND_IMG_2, (400, 300))
        elif settings.type_background == 3:
            return Background(settings.BACKGROUND_IMG_3, (400, 300))

    def init_side(self):
        if settings.type_game == 'Emperor':
            self.is_game_emperor = True
        elif settings.type_game == 'Slave':
            self.is_game_emperor = False
        else:
            if settings.is_server:
                self.is_game_emperor = True
            else:
                self.is_game_emperor = False

    def init_opp_cards(self, count):
        self.opp_cards_group.empty()
        for i in range(count):
            self.opp_cards_group.add(Cards(settings.OPPNENTS_CARDS_IMG, settings.OPPNENTS_CARDS_PLACE[i]))

    def init_my_cards(self):
        global emperor_img, slave_img, citizer_img
        if settings.type_card % 2 == 1:
            emperor_img = settings.EMPEROR_IMG
            slave_img = settings.SLAVE_IMG
            citizer_img = settings.CITIZER_IMG
        elif settings.type_card % 2 == 0:
            emperor_img = settings.FOX_IMG
            slave_img = settings.SNAKE_IMG
            citizer_img = settings.URCHIN_IMG

        self.emperor = Cards(emperor_img, settings.ES_PLACE)
        self.slave = Cards(slave_img, settings.ES_PLACE)
        self.my_cards_group.empty()
        for i in range(4):
            self.my_cards_group.add(Cards(citizer_img, settings.CITIZERS_PLACE[i]))
        if self.is_game_emperor:
            self.my_cards_group.add(self.emperor)
        else:
            self.my_cards_group.add(self.slave)

    def update_score(self, result):
        if result == 'WIN':
            self.my_score += 1 if self.is_game_emperor else 10
        elif result == "DEFEAT":
            self.opp_score += 10  if self.is_game_emperor else 1

    def return_table(self):
        if self.is_game_emperor:
            self.is_game_emperor = False
        else:
            self.is_game_emperor = True

    def next_round(self, result):
        self.count_cards = 5
        self.update_score(result)
        if settings.mode_game == "Change" and self.num_game == settings.count_round / 2:
            self.return_table()
        self.init_my_cards()
        self.init_opp_cards(self.count_cards)
        if self.num_game == settings.count_round:
            self.game_over
        self.num_game += 1

    def send_card_to_server(self, selected_card):
        if selected_card == self.emperor:
            self.client.write_sock('EMPEROR')
        elif selected_card == self.slave:
            self.client.write_sock('SLAVE')
        else:
            self.client.write_sock('CITIZER')

    def start(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for one_card in enumerate(self.my_cards_group):
                one_card[1].rect.center = settings.START_PLACE[one_card[0]]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.is_card_selected:
            self.my_point_centre.image = self.my_selected_card.image
            self.my_selected_card.kill()
            self.send_card_to_server(self.my_selected_card)
            self.card = None
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.card != None and self.my_point_centre.rect.colliderect(self.card.rect) and not self.is_card_selected:
                self.image_selected_card = self.card.image
                self.card.rect.center = settings.MY_POINT_CENTRE
                self.my_selected_card = self.card
                self.my_selected_card.image = pygame.image.load('img/card_back.png')
                self.is_card_selected = True
            elif self.my_selected_card != None and self.card != None and not self.my_point_centre.rect.colliderect(self.my_selected_card.rect):
                self.my_selected_card.image = self.image_selected_card
                self.is_card_selected = False
            self.is_doMove = False
            self.card = None
        elif event.type == pygame.MOUSEMOTION and event.buttons[0] and self.is_doMove:
            self.card.rect.center = event.pos
        else:
            for one_card in self.my_cards_group:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and one_card.rect.collidepoint(event.pos) and not self.is_pause:
                    self.is_doMove = True
                    self.card = one_card
        return self.my_cards_group, self.opp_cards_group, self.background_group, self.dialogue_group

