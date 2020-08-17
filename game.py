import pygame

import settings
from gibbet_client import Client
from game_objects import Heart
from gibbet_server import Server


class Game:
    def __init__(self, mainSurface):
        self.FPS = 30
        self.mainSurface = mainSurface
        self.fpsClock = pygame.time.Clock()
        self.all_cards = pygame.sprite.Group()
        self.all_background = pygame.sprite.Group()
        self.run = False
        self.myfont = pygame.font.SysFont('serif', 48)

    def open_client_server(self):
        if settings.is_server:
            self.server = Server()
            self.client = Client()
        else:
            self.client = Client()

    def close_clien_server(self):
        if settings.is_server:
            self.client.close_sock()
            self.server.stop()
        else:
            self.client.close_sock()

    def retry_settings(self, type_game, count_rounds):
        if type_game == "E":
            type_game = "S"
        elif type_game == "S":
            type_game = "E"
        else:
            type_game = "ES"
        settings.type_game = type_game
        settings.count_round = count_rounds

    def play(self):
        try:
            self.open_client_server()
        except:
            return True

        array_settings = self.client.read().split('_')
        if array_settings[0] == "connected":
            is_client = not settings.is_server
            if is_client:
                self.retry_settings(array_settings[1], int(array_settings[2]))
            heart = Heart(self.mainSurface, settings.is_server)
            self.run = True

        while self.run:
            self.fpsClock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYUP and event.key == 27:
                    self.close_clien_server()
                    self.run = False
                self.all_cards, self.all_background = heart.start(event, self.client)
            self.all_background.draw(self.mainSurface)
            self.mainSurface.blit(self.myfont.render('Игра: ' + str(heart.num_game), 1, (210, 120, 200)), (100, 50))
            self.mainSurface.blit(
                self.myfont.render('Счёт: {}:{}'.format(heart.my_score, heart.opp_score), 1, (210, 120, 200)),
                (600, 50))
            self.all_cards.draw(self.mainSurface)
            pygame.display.flip()
        return True
