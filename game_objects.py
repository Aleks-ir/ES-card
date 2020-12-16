from threading import Thread

import pygame
import time

import constants
import settings
from game_button import Image_button


class Cards(pygame.sprite.Sprite):

    def __init__(self, filename, pos):
        super(Cards, self).__init__()
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def set_image(self, filename):
        self.image = pygame.image.load(filename)



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
                if data == constants.SHUTDOWN:
                    self.is_other_one_disconnected = True
                    self.run_receiver = False
                if data == constants.START:
                    self.is_other_one_connected = True
                elif data == constants.WAIT:
                    self.move_opp_card()
                else:
                    array_data = data.split('_')
                    Thread(target=self.update_field, args=(array_data[0], array_data[1])).start()
            except:
                pass


    def __init__(self, mainSurface, client):
        self.client = client
        self.my_score = 0
        self.opp_score = 0
        self.count_cards = 5
        self.num_round = 1
        self.my_cards_group = pygame.sprite.Group()
        self.opp_cards_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()

        self.init_side()
        self.init_card_back()
        self.init_box_group()
        self.init_background_group()
        self.init_my_cards_group()
        self.init_opp_cards_group(self.count_cards)

        self.my_selected_card = None
        self.card = None
        self.is_doMove = False
        self.is_card_selected = False
        self.run_receiver = True
        self.is_pause = False
        self.is_other_one_connected = False
        self.is_other_one_disconnected = False
        self.is_change_sound = False
        self.is_game_over = False
        self.is_last_round = False
        self.image_selected_card = self.emperor.image

        self.mainSurface = mainSurface
        Thread(target=self.receiver).start()

    def update_field(self, data_0, data_1):
        self.open_my_card()
        self.open_opp_card(data_1)
        self.clear_field()
        if data_0 != constants.DRAW:
            self.next_round(data_0)


    def clear_field(self):
        self.count_cards -= 1
        self.init_opp_cards_group(self.count_cards)
        time.sleep(1)
        self.is_card_selected = False
        self.my_point_centre.set_image(self.load_cp_img())
        self.opp_point_centre.set_image(self.load_cp_img())

    def move_opp_card(self):
        self.init_opp_cards_group(self.count_cards - 1)
        self.opp_point_centre.set_image(self.card_back_img)

    def open_my_card(self):
        self.my_point_centre.image = self.image_selected_card

    def open_opp_card(self, opp_card):
        if opp_card == constants.EMPEROR:
            self.opp_point_centre.set_image(self.emperor_img)
        elif opp_card == constants.SLAVE:
            self.opp_point_centre.set_image(self.slave_img)
        elif opp_card == constants.CITIZER:
            self.opp_point_centre.set_image(self.citizer_img)

    def init_box_group(self):
        self.box_round = Image_button(False, self.load_box_img(), 20, 20, str(self.num_round), 23,
                                      constants.GRAEY, constants.ALGERIAN)
        self.box_score = Image_button(False, self.load_box_img(), 700, 20,
                                      '{}:{}'.format(self.my_score, self.opp_score), 23,
                                      constants.GRAEY, constants.ALGERIAN)
        self.box_group = (self.box_round, self.box_score)

    def load_box_img(self):
        if settings.type_box % 3 == 0:
            return constants.BOX_IMG_1
        elif settings.type_box % 3 == 1:
            return constants.BOX_IMG_2
        elif settings.type_box % 3 == 2:
            return constants.BOX_IMG_3

    def init_background_group(self):
        self.background = Background(self.load_bg_img(), constants.CENTRE)
        self.my_point_centre = Cards(self.load_cp_img(), constants.MY_CP)
        self.opp_point_centre = Cards(self.load_cp_img(), constants.OPP_CP)
        self.background_group.add(self.background, self.my_point_centre, self.opp_point_centre)

    def load_bg_img(self):
        if settings.type_bg % 3 == 0:
            return constants.BG_IMG_1
        elif settings.type_bg % 3 == 1:
            return constants.BG_IMG_2
        elif settings.type_bg % 3 == 2:
            return constants.BG_IMG_3

    def load_cp_img(self):
        if settings.type_cp % 3 == 0:
            return constants.CP_IMG_1
        elif settings.type_cp % 3 == 1:
            return constants.CP_IMG_2
        elif settings.type_cp % 3 == 2:
            return constants.CP_IMG_3

    def init_side(self):
        if settings.type_game == constants.EMPEROR:
            self.is_for_emperor = True
        elif settings.type_game == constants.SLAVE:
            self.is_for_emperor = False
        else:
            if settings.is_server:
                self.is_for_emperor = True
            else:
                self.is_for_emperor = False

    def init_card_back(self):
        if settings.type_card % 2 == 0:
            self.card_back_img = constants.CARD_BACK_IMG_1
        else:
            self.card_back_img = constants.CARD_BACK_IMG_2

    def init_opp_cards_group(self, count):
        self.opp_cards_group.empty()
        for i in range(count):
            self.opp_cards_group.add(Cards(self.card_back_img, constants.OPPNENTS_CARDS_PLACE[i]))

    def init_my_cards_group(self):
        if settings.type_card % 2 == 0:
            self.emperor_img = constants.EMPEROR_IMG
            self.slave_img = constants.SLAVE_IMG
            self.citizer_img = constants.CITIZER_IMG
        elif settings.type_card % 2 == 1:
            self.emperor_img = constants.FOX_IMG
            self.slave_img = constants.SNAKE_IMG
            self.citizer_img = constants.URCHIN_IMG

        self.emperor = Cards(self.emperor_img, constants.ES_PLACE)
        self.slave = Cards(self.slave_img, constants.ES_PLACE)
        self.my_cards_group.empty()
        for i in range(4):
            self.my_cards_group.add(Cards(self.citizer_img, constants.CITIZERS_PLACE[i]))
        if self.is_for_emperor:
            self.my_cards_group.add(self.emperor)
        else:
            self.my_cards_group.add(self.slave)

    def update_score(self, result):
        if result == constants.WIN:
            self.my_score += 1 if self.is_for_emperor else 5
        elif result == constants.DEFEAT:
            self.opp_score += 5 if self.is_for_emperor else 1

    def update_box(self):
        self.box_round.text = str(self.num_round)
        self.box_score.text = '{}:{}'.format(self.my_score, self.opp_score)

    def return_table(self):
        self.is_change_sound = True
        if self.is_for_emperor:
            self.is_for_emperor = False
        else:
            self.is_for_emperor = True

    def send_card_to_server(self, selected_card):
        if selected_card == self.emperor:
            self.client.write_sock(constants.EMPEROR)
        elif selected_card == self.slave:
            self.client.write_sock(constants.SLAVE)
        else:
            self.client.write_sock(constants.CITIZER)

    def next_round(self, result):
        self.count_cards = 5
        self.update_score(result)
        if settings.mode_game == constants.CHANGE and self.num_round == settings.count_round / 2:
            self.return_table()
        if self.num_round == settings.count_round:
            self.is_last_round = True
            self.is_game_over = True
        else:
            self.card = None
            self.init_my_cards_group()
            self.init_opp_cards_group(self.count_cards)
            self.num_round += 1
        self.update_box()

    def get(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            for one_card in enumerate(self.my_cards_group):
                one_card[1].rect.center = constants.START_PLACE[one_card[0]]
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            if self.is_card_selected and not self.is_other_one_disconnected and not self.is_doMove and not self.is_game_over:
                self.my_point_centre.image = self.my_selected_card.image
                self.my_selected_card.kill()
                self.send_card_to_server(self.my_selected_card)
                self.card = None
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.card != None and self.my_point_centre.rect.colliderect(self.card.rect) and not self.is_card_selected:
                self.image_selected_card = self.card.image
                self.card.rect.center = constants.MY_CP
                self.my_selected_card = self.card
                self.my_selected_card.image = pygame.image.load(self.card_back_img)
                self.is_card_selected = True
            elif self.my_selected_card != None and self.card != None and not self.my_point_centre.rect.colliderect(self.my_selected_card.rect):
                self.my_selected_card.image = self.image_selected_card
                self.is_card_selected = False
            self.is_doMove = False
            self.card = None
        elif self.card != None and event.type == pygame.MOUSEMOTION and event.buttons[0] and self.is_doMove:
            self.card.rect.center = event.pos
        else:
            for one_card in self.my_cards_group:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and one_card.rect.collidepoint(event.pos):
                    if not self.is_pause and self.is_other_one_connected and not self.is_other_one_disconnected and not self.is_game_over:
                        self.is_doMove = True
                        self.card = one_card
        return  self.background_group, self.box_group, self.opp_cards_group, self.my_cards_group

