#!/usr/bin/env python
import pygame
from pygame.locals import *
import thehandler


game = thehandler.get_game()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            exit(0)

        if event.type == pygame.MOUSEBUTTONUP:
            game.mouse_click(event.pos, event.button)

    game.mouse_move(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])
    game.render()

    clock.tick(60)
