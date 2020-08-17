from threading import Thread

import pygame
import time

import settings
from endgame_menu import Game_over
from settings import CARDS_WAY, CARDS_IMG


class Cards(pygame.sprite.Sprite):

    def __init__(self, filename, pos):
        super(Cards, self).__init__()
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.center = pos

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


class Heart:
    def __init__(self, mainSurface, is_server):
        self.my_score = 0
        self.opp_score = 0
        self.num_game = 1
        self.all_cards = pygame.sprite.Group()
        self.all_background = pygame.sprite.Group()

        self.background = Background('img/bg2.png', (450, 250))
        self.back_place = Background('img/s3.png', (450, 150))
        self.all_background.add(self.background, self.back_place)
        self.init_side()
        self.init_cards()
        self.deletion_card = None
        self.card = None
        self.is_doMove = False
        self.is_card_selected = False
        self.is_block_card = False
        self.image_selected_card = self.emperor.image

        self.mainSurface = mainSurface
        self.game_over = Game_over(self.mainSurface)
        self.over = False

    def init_side(self):
        if settings.type_game == 'E':
            self.is_game_emperor = True
        elif settings.type_game == 'S':
            self.is_game_emperor = False
        else:
            if settings.is_server:
                self.is_game_emperor = True
            else:
                self.is_game_emperor = False

    def init_cards(self):
        self.emperor = Cards('img/emperor.png', (450, 380))
        self.slave = Cards('img/slave.png', (450, 380))
        self.all_cards.empty()
        for i in range(4):
            self.all_cards.add(Cards(CARDS_WAY[i], CARDS_IMG[i]))
        if self.is_game_emperor:
            self.all_cards.add(self.emperor)
        else:
            self.all_cards.add(self.slave)

    def retry_score(self, data):
        if data == 'WIN':
            if self.is_game_emperor:
                self.my_score += 1
            else:
                self.my_score += 10
        elif data == "DEFEAT":
            if self.is_game_emperor:
                self.opp_score += 10
            else:
                self.opp_score += 1

    def return_table(self):
        if self.is_game_emperor:
            self.is_game_emperor = False
        else:
            self.is_game_emperor = True

    def next_round(self, data):
        self.retry_score(data)
        if settings.type_game == "ES" and self.num_game == settings.count_round / 2:
            self.return_table()
        self.init_cards()
        if self.num_game == settings.count_round:
            self.game_over
        self.num_game += 1


    def start(self, event, client):
        if self.over:
            if self.is_block_card:
                self.next_round("WIN")
                #self.game_over.show_menu()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for one_card in enumerate(self.all_cards):
                one_card[1].rect.center = CARDS_IMG[one_card[0]]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.is_card_selected and not self.is_block_card:
            def ass():
                self.is_block_card = True
                time.sleep(1)
                try:
                    data = client.read()
                    if data != 'DRAW':
                        self.next_round(data)
                except:
                    pass
                self.deletion_card.kill()
                self.is_card_selected = False
                self.is_block_card = False


            Thread(target=ass).start()
            self.deletion_card.image = self.image_selected_card

            if self.deletion_card == self.emperor:
                client.write_sock('EMPEROR')
            elif self.deletion_card == self.slave:
                client.write_sock('SLAVE')
            else:
                client.write_sock('SITIZER')
            self.card = None


        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

            if self.card != None and self.back_place.rect.colliderect(self.card.rect) and not self.is_card_selected and not self.is_block_card:

                if self.card.image != self.image_selected_card:
                    self.image_selected_card = self.card.image

                self.card.rect.center = (450, 150)
                self.deletion_card = self.card
                self.deletion_card.image = pygame.image.load('img/card_back.png')
                self.is_card_selected = True

            elif self.deletion_card != None and self.card != None and not self.back_place.rect.colliderect(self.deletion_card.rect):

                self.deletion_card.image = self.image_selected_card
                self.is_card_selected = False

            self.is_doMove = False
            self.card = None
        elif event.type == pygame.MOUSEMOTION and event.buttons[0] and self.is_doMove:
            self.card.rect.center = event.pos
        else:
            for one_card in self.all_cards:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and one_card.rect.collidepoint(event.pos):
                    self.is_doMove = True
                    self.card = one_card
        return self.all_cards, self.all_background
