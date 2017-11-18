import math, random

class Posicao(object):
    def __init__(self, x, y, tempo = 100): # quando a posicao e nova, o tempo e maximo, assim a funcao de decrescimo dara um numero muito pequeno
        self.x = x
        self.y = y
        self.tempo = tempo
        self.angulo = 0
        self.marcado = False
        
    def decrescimoProbabilidade (self, C = 1, p = 0.07):
        return C * math.exp(-p * self.tempo)
    
    def anguloPontos(self, outro): # o angulo seria calculado quando precisarmos, pq no momento de criacao do ponto, podemos nao ter outro ponto pra comparacao
        x1, y1 = self.x, self.y
        x2, y2 = outro.x, outro.y
        try: # tem q ter try pq a linha abaixo pode dar divisao por zero ou um acos q nao existe :(
            self.angulo = math.acos((x1*x2 + y1*y2) / (math.sqrt(x1**2 + y1**2) * math.sqrt(x2**2 + y2**2)))
        except:
            self.angulo = 0 # ai coloquei pra retornar zero por padrao

class Grade(object):
    def __init__(self, dimensaoAltura, dimensaoLargura, offsetY, offsetX):
        self.posicoes = self.crie_matriz(dimensaoAltura, dimensaoLargura, offsetY, offsetX)
        self.dimensaoAltura = dimensaoAltura
        self.dimensaoLargura = dimensaoLargura
        self.offsetY = offsetY
        self.offsetX = offsetX
        self.direcao = 0
        
    def __getitem__ (self, index): # isso e o q achei
        return self.posicoes[index[0] / self.offsetY][index[1] / self.offsetX] # dividir pelo offset
    
    def __setitem__ (self, index, value):
        self.posicoes[index[0] / self.offsetY][index[1] / self.offsetX] = value
    
    def crie_matriz(self, dimensaoAltura, dimensaoLargura, offsetY, offsetX):    
        matriz = []
        for i in range(0, dimensaoAltura + offsetY, offsetY): # as coordenadas devem bater com as posicoes possiveis da grade
            linha = []
            for j in range(0, dimensaoLargura + offsetX, offsetX):
                linha.append(Posicao(i,j))
            matriz.append(linha)
    
        return matriz
    
    def weighted_choice(self, choices): # funcao de escolha aleatoria
        escolhas = [(c, self[c[0], c[1]].decrescimoProbabilidade()) for c in choices]
        total = sum(w for c, w in escolhas)
        r = random.uniform(0, total)
        upto = 0
        for c, w in escolhas:
            if upto + w >= r:
                return c
            upto += w
        assert False, "Shouldn't get here"
    
    def atualizaProbabilidadeGrade(self): # essa funcao e chamada a cada iteracao
        for i in range(len(self.posicoes)):
            for j in range(len(self.posicoes)):
                if self.posicoes[i][j].tempo >= 100: continue
                else: self.posicoes[i][j].tempo += 1 # temos que aumentar o tempo pra diminuir a probabilidade
                
    def decidePosicao (self, orientacao, c):
        if orientacao == 0:
            if c + self.offsetX < self.dimensaoLargura:
                return c + self.offsetX
            else :
                return 0
        elif orientacao == 1:
            if c - self.offsetY < 0:
                return self.dimensaoAltura - self.offsetY
            else :
                return c - self.offsetY

class Rastro(object):
    imagem = None
    def __init__(self, x, y, tempo = 10):
        self.x = x
        self.y = y
        self.tempo = tempo

    def descontarTempo(self):
        self.tempo = self.tempo - 1