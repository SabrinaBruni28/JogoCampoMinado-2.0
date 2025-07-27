import time
import random

class CampoMinado:
    def __init__(self):
        self.bomba = "Images/bomba.png"
        self.alerta = "Images/bandeira.png"

    def retorna_imagem(self, posicao1, posicao2):
        if self.existe_bomba(posicao1, posicao2):
            return self.bomba
        if self.existe_numero(posicao1, posicao2):
            return f"Images/{self.jogo[posicao1][posicao2]}.jpg" if self.jogo[posicao1][posicao2] >= 0 else self.bomba
        return ""

    def completa_matriz(self):
        # Preencher a matriz com números de 1 a 9
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.posicao_vazia(i, j):
                    # Contar bombas ao redor
                    contador = 0
                    for x in range(max(0, i-1), min(self.tamanho, i+2)):
                        for y in range(max(0, j-1), min(self.tamanho, j+2)):
                            if self.jogo[x][y] == -1:
                                contador += 1
                    self.jogo[i][j] = contador

    def coloca_bomba(self):
        num_bombas = self.tamanho
        bombas = 0

        # Inicializa o gerador de números aleatórios
        random.seed(int(time.time()))

        # Loop de colocação de bombas
        while bombas < num_bombas:
            posicao1 = random.randint(0, num_bombas - 1)
            posicao2 = random.randint(0, num_bombas - 1)

            if self.posicao_vazia(posicao1, posicao2):
                self.jogo[posicao1][posicao2] = -1  # Marca a posição com uma bomba
                bombas += 1

    def colocar_alertas(self, posicao1, posicao2):
        self.jogo[posicao1][posicao2] = -2  # Marca a posição com um alerta

    def posicao_vazia(self, posicao1, posicao2):
        # Verifica se a posição está dentro dos limites da matriz
        return self.jogo[posicao1][posicao2] == 100

    def existe_bomba(self, posicao1, posicao2):
        # Verifica se já existe uma bomba na posição
        return self.jogo[posicao1][posicao2] == -1
    
    def existe_espaco(self, posicao1, posicao2):
        # Verifica se a posição está vazia (sem bomba)
        return self.jogo[posicao1][posicao2] == 0
    
    def existe_numero(self, posicao1, posicao2):
        # Verifica se a posição contém um número (não é bomba)
        return self.jogo[posicao1][posicao2] >= 0
    
    def existe_alerta(self, posicao1, posicao2):
        # Verifica se a posição contém um alerta
        return self.jogo[posicao1][posicao2] == -2

    def reiniciar_jogo(self, tamanho=10):
        # Resetar matriz do jogo
        self.tamanho = tamanho
        self.jogo = [[100 for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.coloca_bomba()
        self.completa_matriz()

    def revelar_posicao(self, posicao1, posicao2):
        # Revela a posição na matriz
        return self.jogo[posicao1][posicao2]
        return None