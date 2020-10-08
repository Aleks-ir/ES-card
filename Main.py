import queue
from threading import Thread

import pygame

import constants
import settings
from gibbet_client import Client
from gibbet_server import Server
from main_loop import Main_loop
from main_menu import Menu
from constants import SIZE





def server_connection(q):
    try:
        q.put(Client(settings.server_ip))
    except:
        q.put(None)

def creature_server():
    Server()


def creature_connection():
    if settings.is_server:
        try:
            creature_server()
        except:
            return False
    q = queue.Queue()
    Thread(target=server_connection, args=(q,)).start()
    while True:
        pygame.time.Clock().tick(30)
        try:
            return q.get(timeout=1)
        except queue.Empty:
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False



if __name__ == '__main__':
    pygame.init()
    mainSurface = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(constants.CAPTION)
    run = True
    while run:
        run = Menu(mainSurface).show_menu()
        if run:
            client = creature_connection()
            if client:
                run = Main_loop(mainSurface, client).start()
    pygame.quit()
