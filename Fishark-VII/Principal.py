'''
Created on 25 de ago de 2017

@author: matheus
'''
#! /usr/bin/env python
import pygame, random
from pygame.locals import *
from sys import exit
from Agentes import Peixe, Tubarao, novosAgentes
 
pygame.init()


dimensaoTela = 640
dimensaoGrade = 64
offset = dimensaoTela / dimensaoGrade
numPeixes = 15
numTubaroes = 5

screen = pygame.display.set_mode((dimensaoTela, dimensaoTela), 0, 32)

background_filename = 'background.png'
background = pygame.image.load(background_filename).convert()

fish_filename = 'fish.png'
fishImage = pygame.image.load(fish_filename).convert_alpha()
Peixe.image = fishImage

shark_filename = 'shark.png'
sharkImage = pygame.image.load(shark_filename).convert_alpha()
Tubarao.image = sharkImage

tubaroes = [Tubarao(offset, offset), Tubarao(dimensaoTela - offset, offset), Tubarao(offset, dimensaoTela - offset), Tubarao(dimensaoTela - offset, dimensaoTela - offset)]
#tubaroes = [Tubarao(random.randrange(0, dimensaoTela, offset), random.randrange(0, dimensaoTela, offset)) for _ in range(numTubaroes)]
agentes = [Peixe(random.randrange(0, dimensaoTela, offset), random.randrange(0, dimensaoTela, offset)) for _ in range(numPeixes)]

agentes = tubaroes + agentes

pygame.display.set_caption('FiShark')
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    
    screen.blit(background, (0, 0))
    
    agentes = novosAgentes(agentes, dimensaoTela, offset)

    for a in agentes:
        screen.blit(a.image, (a.x, a.y))

    """
    for t in tubaroes:
        for a in agentes:
            if t.colisao(a, offset) and not isinstance(a, Tubarao):
                a.tempoVida = 0
    """
    pygame.display.update()
    time_passed = clock.tick(5)