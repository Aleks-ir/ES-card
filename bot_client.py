import time
import random
from threading import Thread

import constants
import settings
from gibbet_client import Client


class Bot:
    def __init__(self):
        self.client = self.open_client()
        self.run = True
        self.is_send_card = True
        self.init_side()
        self.count_card = 5
        self.num_round = 1
        Thread(target=self.receiver).start()

    def init_side(self):
        if settings.type_game == constants.EMPEROR:
            self.is_for_emperor = True
        elif settings.type_game == constants.SLAVE:
            self.is_for_emperor = False

    def receiver(self):
        while self.run:
            try:
                data = self.client.read()
                if data.split('_')[0] == constants.DRAW:
                    self.is_send_card = True
                elif data.split('_')[0] == constants.WIN or data.split('_')[0] == constants.DEFEAT:
                    self.count_card = 5
                    self.num_round += 1
                    self.is_send_card = True
                    if settings.mode_game == constants.CHANGE and self.num_round == settings.count_round / 2 + 1:
                        self.is_for_emperor = False if self.is_for_emperor else True
            except:
                pass

    def start(self):
        while self.run:
            try:

                time.sleep(random.randint(1, 3))
                if self.is_send_card:
                    random_card = self.generation_card(random.randint(1, self.count_card))
                    self.client.write_sock(random_card)
                    self.is_send_card = False
                    self.count_card -= 1
                time.sleep(random.randint(1, 3))
            except:
                self.run = False

    def open_client(self):
        return Client(settings.server_ip)

    def generation_card(self, num):
        if num == 1:
            return constants.SLAVE if self.is_for_emperor else constants.EMPEROR
        else:
            return constants.CITIZER
