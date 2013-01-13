import thehandler.pygcurse
import pygame
import thehandler
from thehandler.scene import Scene
from thehandler.game import Game
from thehandler.menu import StartMenu


gamewindow = thehandler.createGame()

g_game = thehandler.g_game

mainscene = Scene()
menu = StartMenu()
mainscene.addWindow(menu)

g_game.pushScene(mainscene)


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key in range(pygame.K_SPACE, pygame.K_DELETE):
                key = ord(event.unicode)
            else:
                key = event.key
            g_game.inchar(key = key, char = event.unicode)

    g_game.display(gamewindow)
    gamewindow.update()

    clock.tick(60)
