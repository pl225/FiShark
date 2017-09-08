#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random

class Agente(object):
    image = None
    raio = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tempoVida = 5000000000

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
        
        if self.x + offset <= dimensaoTela: # peixe anda pra frente
            movimentosPossiveis.append((self.x + offset, self.y))
        
        if self.x - offset >= 0: # peixe anda pra tras
            movimentosPossiveis.append((self.x - offset, self.y))
            
        if self.y + offset <= dimensaoTela: # peixe desce
            movimentosPossiveis.append((self.x, self.y + offset))
        
        if self.y - offset >= 0: # peixe sobe
            movimentosPossiveis.append((self.x, self.y - offset))
            
        if self.x + offset <= dimensaoTela and self.y - offset >= 0: # avanca e sobe
            movimentosPossiveis.append((self.x + offset, self.y - offset))
        
        if self.x - offset >= 0 and self.y - offset >= 0: # recua e sobe
            movimentosPossiveis.append((self.x - offset, self.y - offset))
        
        if self.y + offset <= dimensaoTela and self.x + offset <= dimensaoTela: # avanca e desce
            movimentosPossiveis.append((self.x + offset, self.y + offset))
        
        if self.y + offset <= dimensaoTela and self.x - offset >= 0: # desce e recua
            movimentosPossiveis.append((self.x - offset, self.y + offset))        
        
        return movimentosPossiveis


class Peixe(Agente):
    raio = 5
    def __init__(self, x, y):
        super(Peixe, self).__init__(x, y)
        self.reproduziu = 0
        
    def proximaPosicao(self, agentes, dimensaoTela, offset):
        movimentosPossiveis = self.movimentar(dimensaoTela, offset)
        novoPeixe = None
        
        if self.reproduziu > 0: self.reproduziu -= 1 
        if self.tempoVida > 0: self.tempoVida -= 1
        else: return None
        
        for a in agentes:
            if a is not self:
                if isinstance(a, Tubarao) and self.manhattan(a) <= offset * Peixe.raio:
                    distancias = [((x, y), math.fabs(x - a.x) + math.fabs(y - a.y)) for (x, y) in movimentosPossiveis] 
                    self.x, self.y = max(distancias, key=lambda i: i[1])[0]
                    return None
        for a in agentes:
            if a is not self:
                if isinstance(a, Peixe) and self.colisao(a, offset) and not (self.reproduziu or a.reproduziu):
                    novoPeixe = Peixe.reproduzir(self, a, dimensaoTela, offset)
                    break
        if len(movimentosPossiveis) > 0: self.x, self.y = random.choice(movimentosPossiveis)
        return novoPeixe
    
    @staticmethod
    def reproduzir(p, m, dimensaoTela, offset):
        p.reproduziu = 10000; m.reproduziu = 10000
        x, y = 0, 0
        if random.randint(0, 1):
            x, y = random.choice(m.movimentar(dimensaoTela, offset*20))
        else:
            x, y = random.choice(p.movimentar(dimensaoTela, offset*20))
        return Peixe(x, y)            

class Tubarao(Agente):
    raio = 10
    def __init__(self, x, y):
        super(Tubarao, self).__init__(x, y)
        
    def proximaPosicao(self, agentes, dimensaoTela, offset):
        movimentosPossiveis = self.movimentar(dimensaoTela, offset)
        
        for a in agentes:
            if a is not self:
                if isinstance(a, Peixe) and self.colisao(a, offset):
                    a.tempoVida = 0
        
        for a in agentes:
            if a is not self:
                if isinstance(a, Peixe) and self.manhattan(a) <= offset * Tubarao.raio:
                    distancias = [((x, y), math.fabs(x - a.x) + math.fabs(y - a.y)) for (x, y) in movimentosPossiveis] 
                    self.x, self.y = min(distancias, key=lambda i: i[1])[0]
                    return None
                    
        if len(movimentosPossiveis) > 0: self.x, self.y = random.choice(movimentosPossiveis)                
        
        
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
        
    return lista

def decrescimoProbabilidade (tempo, C = 1, p = 0.07):
    return C * math.exp(-p * tempo)