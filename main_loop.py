import pygame

import settings
from gibbet_client import Client
from game_objects import Game_objects
from gibbet_server import Server


class Main_loop:
    def __init__(self, mainSurface):
        self.FPS = 30
        self.mainSurface = mainSurface
        self.fpsClock = pygame.time.Clock()
        self.my_cards = pygame.sprite.Group()
        self.opp_cards = pygame.sprite.Group()
        self.all_background = pygame.sprite.Group()
        self.is_draw_dialogue_connected = True
        self.dialogue = ()
        self.run = False
        self.myfont = pygame.font.SysFont('serif', 48)

    def open_client_or_server(self):
        if settings.is_server:
            self.server = Server()
            self.client = Client()
        else:
            self.client = Client()

    def close_clien_or_server(self):
        if settings.is_server:
            self.client.close_sock()
            self.server.stop()
        else:
            self.client.close_sock()

    def retry_settings(self, type_game, count_rounds, mode_game):
        settings.type_game = type_game
        settings.count_round = count_rounds
        settings.mode_game = mode_game

    def start(self):
        try:
            self.open_client_or_server()
        except:
            return True

        array_settings = self.client.read().split('_')
        if array_settings[0] == "connected":
            self.retry_settings(array_settings[1], int(array_settings[2]), array_settings[3])
            game_object = Game_objects(self.mainSurface, self.client)
            self.run = True

        while self.run:
            self.fpsClock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close_clien_or_server()
                    game_object.run_receiver = False
                    return False
                elif event.type == pygame.KEYUP and event.key == 27:
                    self.close_clien_or_server()
                    game_object.run_receiver = False

                self.my_cards, self.opp_cards, self.all_background, self.dialogue = game_object.start(event)
            self.all_background.draw(self.mainSurface)
            self.mainSurface.blit(self.myfont.render('Игра: ' + str(game_object.num_game), 1, (210, 120, 200)), (100, 50))
            self.mainSurface.blit(self.myfont.render('Счёт: {}:{}'.format(game_object.my_score, game_object.opp_score), 1, (210, 120, 200)),(600, 50))
            self.opp_cards.draw(self.mainSurface)
            self.my_cards.draw(self.mainSurface)
            if len(self.dialogue) != 0:
                for item in self.dialogue:
                    item.draw(self.mainSurface)

            pygame.display.flip()
        return True
