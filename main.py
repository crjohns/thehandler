#!/usr/bin/env python
import pygame
import thehandler


game = thehandler.createGame()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            exit(0)

    clock.tick(60)
