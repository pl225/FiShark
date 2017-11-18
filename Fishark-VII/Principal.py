'''
Created on 25 de ago de 2017

@author: matheus
'''
#! /usr/bin/env python
import pygame, random
from pygame.locals import *
from sys import exit
from Agentes import Peixe, Tubarao, novosAgentes
from Modelo import Grade, Rastro
 
pygame.init()

dimensaoTelaAltura = 640
dimensaoTelaLargura = 640
dimensaoGradeAltura = 64
dimensaoGradeLargura = 64
offsetY = dimensaoTelaAltura / dimensaoGradeAltura
offsetX = dimensaoGradeLargura / dimensaoGradeLargura

numPeixes = 15
numTubaroes = 5

#Tubarao.grade = Grade(dimensaoTela, offset)
Peixe.grade = Grade(dimensaoTelaAltura, dimensaoGradeLargura, offsetY, offsetX)

screen = pygame.display.set_mode((dimensaoTelaLargura, dimensaoTelaAltura), 0, 32)

background_filename = 'background.png'
background = pygame.image.load(background_filename).convert()

fish_filename = 'ghost.png'
fishImage = pygame.image.load(fish_filename).convert_alpha()
Peixe.image = fishImage

shark_filename = 'shark.png'
sharkImage = pygame.image.load(shark_filename).convert_alpha()
Tubarao.image = sharkImage

rastro_filename = 'rastro.png'
rastroImage = pygame.image.load(rastro_filename).convert_alpha()
Rastro.imagem = rastroImage

shark_leader_filename = 'shark2.png'
sharkLeaderImage = pygame.image.load(shark_leader_filename).convert_alpha()

fish_leader_filename = 'fish2.png'
fishLeaderImage = pygame.image.load(fish_leader_filename).convert_alpha()

#tubaroes = [Tubarao(offset, offset), Tubarao(dimensaoTela - offset, offset), Tubarao(offset, dimensaoTela - offset), Tubarao(dimensaoTela - offset, dimensaoTela - offset)]
tubaroes = [Tubarao(random.randrange(0, dimensaoTela, offset), random.randrange(0, dimensaoTela, offset)) for _ in range(numTubaroes)]
agentes = [Peixe(random.randrange(0, dimensaoTela, offset), random.randrange(0, dimensaoTela, offset)) for _ in range(numPeixes)]

agentes = tubaroes + agentes

Tubarao.escolheNovoLider(agentes)
Peixe.escolheNovoLider(agentes)

pygame.display.set_caption('FiShark')
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    
    screen.blit(background, (0, 0))
    
    agentes = novosAgentes(agentes, dimensaoTelaAltura, dimensaoGradeLargura, offsetY, offsetX)
    
    for a in agentes:
        if isinstance(a ,Peixe):
            for r in a.vetorRastro:
                screen.blit(Rastro.imagem, (r.x, r.y))
                
    for a in agentes:
        if isinstance(a, Tubarao) and a.lider:
            screen.blit(sharkLeaderImage, (a.x, a.y))
        elif isinstance(a, Peixe) and a.lider:
            screen.blit(fishLeaderImage, (a.x, a.y))    
        else:
            screen.blit(a.image, (a.x, a.y))

    pygame.display.update()
    time_passed = clock.tick(5)