#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random
from Modelo import Rastro
from __builtin__ import isinstance

class Agente(object):
    image = None
    raio = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tempoVida = random.randint(0, 5000)

    def manhattan(self, outro):
        return math.fabs(self.x - outro.x) + math.fabs(self.y - outro.y)
    
    def proximaPosicao(self, agentes, dimensaoTela, offset):
        raise NotImplementedError
    
    def colisao(self, outro, offset):
        if self.y + offset < outro.y: return False
        if self.y > outro.y + offset: return False
        if self.x + offset  < outro.x: return False
        if self.x > outro.x + offset: return False
        return True                        
    
    def movimentar(self, dimensaoTela, offset):
        movimentosPossiveis = []
        
        if self.x + offset < dimensaoTela: # peixe anda pra frente
            movimentosPossiveis.append((self.x + offset, self.y))
        
        if self.x - offset >= 0: # peixe anda pra tras
            movimentosPossiveis.append((self.x - offset, self.y))
            
        if self.y + offset < dimensaoTela: # peixe desce
            movimentosPossiveis.append((self.x, self.y + offset))
        
        if self.y - offset >= 0: # peixe sobe
            movimentosPossiveis.append((self.x, self.y - offset))
        
        return movimentosPossiveis


class Peixe(Agente):
    raio = 5
    grade = None
    def __init__(self, x, y, vetorRastro = []):
        super(Peixe, self).__init__(x, y)
        self.reproduziu = 0
        self.vetorRastro = vetorRastro
        
    def proximaPosicao(self, agentes, dimensaoTela, offset):
        
        if self.reproduziu > 0: self.reproduziu -= 1 
        if self.tempoVida > 0: self.tempoVida -= 1
        else: return None
        
        movimentosPossiveis = self.movimentar(dimensaoTela, offset)
        novoPeixe = None
        
        for a in agentes:
            if a is not self:
                if isinstance(a, Tubarao) and self.manhattan(a) <= offset * Peixe.raio:
                    distancias = [((x, y), math.fabs(x - a.x) + math.fabs(y - a.y)) for (x, y) in movimentosPossiveis]
                    self.x, self.y = random.choice([c[0] for c in distancias if  c[1] == max(distancias, key=lambda i: i[1])[1]])
                    self.marcarRastro(a)
                    return novoPeixe
        for a in agentes:
            if a is not self:
                if isinstance(a, Peixe) and self.colisao(a, offset) and not (self.reproduziu or a.reproduziu):
                    novoPeixe = Peixe.reproduzir(self, a, dimensaoTela, offset)
                    break
        if len(movimentosPossiveis) > 0: 
            self.x, self.y = random.choice(movimentosPossiveis)
            self.marcarRastro()
        return novoPeixe
    
    @staticmethod
    def reproduzir(p, m, dimensaoTela, offset):
        p.reproduziu = 200; m.reproduziu = 200
        x, y = 0, 0
        if random.randint(0, 1):
            x, y = random.choice(m.movimentar(dimensaoTela, offset*20))
        else:
            x, y = random.choice(p.movimentar(dimensaoTela, offset*20))
        return Peixe(x, y)
    
    def marcarRastro(self, tubarao = None):
        Peixe.grade[self.x, self.y].tempo = 0 # observe, aqui esta sendo usado o get e o set
        if tubarao: Peixe.grade[self.x, self.y].anguloPontos(tubarao)
        
        novoRastro = Rastro(self.x, self.y)
    
        if len(self.vetorRastro) >= 50:
            self.vetorRastro.pop(0) 
        
        self.vetorRastro.append(novoRastro)            

class Tubarao(Agente):
    raio = 10
    grade = None
    def __init__(self, x, y):
        super(Tubarao, self).__init__(x, y)
        self.reproduziu = 0
        self.lider = False
        
    def proximaPosicao(self, agentes, dimensaoTela, offset):
    
        if self.reproduziu > 0: self.reproduziu -= 1    
        if self.tempoVida > 0: self.tempoVida -= 1
        else: return None
        
        novoTubarao = None
        
        movimentosPossiveis = self.movimentar(dimensaoTela, offset)
        
        for a in agentes:
            if a is not self:
                if isinstance(a, Peixe) and self.colisao(a, offset):
                    a.tempoVida = 0
                    
        for a in agentes:
            if a is not self:
                if isinstance(a, Tubarao) and self.colisao(a, offset) and not (self.reproduziu or a.reproduziu):
                    novoTubarao = Tubarao.reproduzir(self, a, dimensaoTela, offset)
                    break
                
        for a in agentes:
            if a is not self:
                if isinstance(a, Tubarao) and a.lider and self.colisao(a, offset):
                    distancias = [((x, y), math.fabs(x - a.x) + math.fabs(y - a.y)) for (x, y) in movimentosPossiveis] 
                    self.x, self.y = min(distancias, key=lambda i: i[1])[0]
                    return novoTubarao
        
        for a in agentes:
            if a is not self:
                if isinstance(a, Peixe) and self.manhattan(a) <= offset * Tubarao.raio:
                    distancias = [((x, y), math.fabs(x - a.x) + math.fabs(y - a.y)) for (x, y) in movimentosPossiveis] 
                    self.x, self.y = min(distancias, key=lambda i: i[1])[0]
                    return novoTubarao
                    
        if len(movimentosPossiveis) > 0: self.x, self.y = Peixe.grade.weighted_choice(movimentosPossiveis)##random.choice(movimentosPossiveis)
        return novoTubarao
        
    @staticmethod
    def reproduzir(p, m, dimensaoTela, offset):
        p.reproduziu = 200; m.reproduziu = 200
        x, y = 0, 0
        if random.randint(0, 1):
            x, y = random.choice(m.movimentar(dimensaoTela, offset*20))
        else:
            x, y = random.choice(p.movimentar(dimensaoTela, offset*20))
        return Tubarao(x, y)
    
    @staticmethod
    def escolheLider(agentes):
        max([a for a in agentes if isinstance(a, Tubarao)], key= lambda i: i.tempoVida).lider = True
        
    @staticmethod
    def escolheNovoLider(agentes):
        if len([a for a in agentes if isinstance(a, Tubarao) and a.lider]) == 0: Tubarao.escolheLider(agentes)     
   
def novosAgentes(agentes, dimensaoTela, offset):
    lista = []
    e = None
    for a in agentes:
        e = a.proximaPosicao(agentes, dimensaoTela, offset)
        if e: 
            lista.append(e)        
    for a in agentes:
        if a.tempoVida > 0:
            lista.append(a)
    Peixe.grade.atualizaProbabilidadeGrade() # atualizando a cada iteracao
    Tubarao.escolheNovoLider(lista)
    return lista