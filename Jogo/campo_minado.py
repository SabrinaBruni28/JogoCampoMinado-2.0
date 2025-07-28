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
        # Definindo um número de bombas proporcional ao tamanho do campo
        self.num_bombas = (self.tamanho * self.tamanho) // 4
        bombas = 0

        # Inicializa o gerador de números aleatórios
        random.seed(int(time.time()))

        # Loop de colocação de bombas
        while bombas < self.num_bombas:
            posicao1 = random.randint(0, self.num_bombas - 1)
            posicao2 = random.randint(0, self.num_bombas - 1)

            if self.posicao_vazia(posicao1, posicao2):
                self.jogo[posicao1][posicao2] = -1  # Marca a posição com uma bomba
                bombas += 1

    def posicao_vazia(self, posicao1, posicao2):
        return 0 <= posicao1 < self.tamanho and 0 <= posicao2 < self.tamanho and self.jogo[posicao1][posicao2] == 100

    def existe_bomba(self, posicao1, posicao2):
        # Verifica se já existe uma bomba na posição
        return self.jogo[posicao1][posicao2] == -1
    
    def existe_espaco(self, posicao1, posicao2):
        # Verifica se a posição está vazia (sem bomba)
        return self.jogo[posicao1][posicao2] == 0
    
    def revelada(self, posicao1, posicao2):
        return self.reveladas[posicao1][posicao2]

    def marcar_posicao_revelada(self, x, y):
        self.reveladas[x][y] = True

    def marcar_posicao_alerta(self, x, y):
        self.alertas[x][y] = True

    def tirar_alerta(self, posicao1, posicao2):
        self.alertas[posicao1][posicao2] = False

    def existe_alerta(self, posicao1, posicao2):
        # Verifica se já existe um alerta (bandeira) na posição
        return self.alertas[posicao1][posicao2]

    def existe_numero(self, posicao1, posicao2):
        # Verifica se a posição contém um número (não é bomba)
        return self.jogo[posicao1][posicao2] >= 0

    def reiniciar_jogo(self, tamanho=10):
        # Resetar matriz do jogo
        self.tamanho = tamanho
        self.reveladas = [[False for _ in range(tamanho)] for _ in range(tamanho)]
        self.alertas = [[False for _ in range(tamanho)] for _ in range(tamanho)]
        self.jogo = [[100 for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.coloca_bomba()
        self.completa_matriz()

    def revelar_posicao(self, posicao1, posicao2):
        # Revela a posição na matriz
        return self.jogo[posicao1][posicao2]
    
    def venceu(self):
        total_casas = self.tamanho * self.tamanho
        total_bombas = self.num_bombas
        total_reveladas = sum(sum(1 for cell in row if cell) for row in self.reveladas)

        return total_reveladas == total_casas - total_bombas
