import sys
from view_utils import  WidgetHelper, CaixaConfirmacao, ViewHelper
from campo_minado import CampoMinado
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
   QApplication, QMainWindow, QWidget, QLabel, QDialog,
   QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget, QSizePolicy, QPushButton
)

class MensagemVencedor(QWidget):
    def __init__(self, parent=None, mensagem="", on_reiniciar=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(parent.rect())

        self.setStyleSheet("background-color: rgba(0, 0, 0, 180);")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        container = QWidget()
        container.setStyleSheet("background-color: white; border-radius: 20px;")
        
        container.setMinimumSize(500, 160)  # menor altura mínima
        container.setMaximumHeight(300)     # limite máximo

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(20)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel(mensagem)
        self.label.setStyleSheet("color: red;")
        font = QFont()
        font.setPointSize(32)  # menor fonte
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.label.setMaximumWidth(520)
        self.label.setMaximumHeight(150)

        self.botao_reiniciar = QPushButton("Reiniciar")
        self.botao_reiniciar.setFixedSize(250, 60)  # menor botão
        self.botao_reiniciar.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-size: 28px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.botao_reiniciar.clicked.connect(lambda: on_reiniciar() if on_reiniciar else None)

        container_layout.addWidget(self.label)
        container_layout.addWidget(self.botao_reiniciar)

        layout.addWidget(container)

class CampoMinadoInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Campo Minado")
        self.setGeometry(100, 100, 1000, 600)
        self.showMaximized()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.view = ViewHelper()
        self.jogo = CampoMinado()
        self.view.abrir_tela(self.stack, self.tela_inicial)

    def closeEvent(self, event):
        dialogo = CaixaConfirmacao(self, titulo="Confirmar saída", mensagem="Você tem certeza que deseja sair?")
        resposta = dialogo.exec()

        if resposta == QDialog.DialogCode.Accepted:
            event.accept()
        else:
            event.ignore()
    
    def toggle_menu(self):
        if self.barra_lateral.isVisible():
            self.barra_lateral.hide()
        else:
            self.barra_lateral.show()

    #############  BLOCOS  #################
    def bloco(self, num, largura, altura):
        bloco = WidgetHelper.bloco(largura, altura)

        layout = QVBoxLayout(bloco)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        bloco.mousePressEvent = lambda e: self.adicionarJogada(num, layout)
        return bloco
    
    def adicionarJogada(self, num: int, layout: QVBoxLayout):
        # Verifica se já existe imagem no layout
        for i in range(layout.count()):
            item = layout.itemAt(i).widget()
            if isinstance(item, QLabel) and item.pixmap() is not None:
                return  # Já tem imagem, não adiciona de novo
        
        x = num // self.jogo.tamanho
        y = num % self.jogo.tamanho

        self.revelar_posicao(x, y, layout)

    def revelar_posicao(self, posicao1, posicao2, layout: QVBoxLayout):
        nome_image = self.jogo.retorna_imagem(posicao1, posicao2)
        if self.jogo.existe_bomba(posicao1, posicao2):
            self.revelar_bombas()
            self.mostrar_vencedor(-1)

        elif self.jogo.existe_numero(posicao1, posicao2):
            imagem = WidgetHelper.imagem(nome_image, scaled=30)
            layout.addWidget(imagem, alignment=Qt.AlignmentFlag.AlignHCenter)

            if self.jogo.jogo[posicao1][posicao2] == 0:
                # Se for zero, revelar posições adjacentes
                for x in range(max(0, posicao1-1), min(self.jogo.tamanho, posicao1+2)):
                    for y in range(max(0, posicao2-1), min(self.jogo.tamanho, posicao2+2)):
                        if (x != posicao1 or y != posicao2) and self.jogo.existe_espaco(x, y):
                            self.revelar_posicao(x, y, layout)
        return None
    
    def revelar_bombas(self):
        for i in range(self.jogo.tamanho):
            for j in range(self.jogo.tamanho):
                if self.jogo.existe_bomba(i, j):
                    nome_image = self.jogo.retorna_imagem(i, j)
                    bloco = self.grid.itemAtPosition(i, j).widget()
                    layout = bloco.layout()
                    imagem = WidgetHelper.imagem(nome_image, scaled=30)
                    layout.addWidget(imagem, alignment=Qt.AlignmentFlag.AlignHCenter)

    def mostrar_vencedor(self, vencedor):
        if vencedor == 1:
            texto = "Você venceu!"
        elif vencedor == -1:
            texto = "Você perdeu!"
        else:
            return

        self.mensagem_vencedor = MensagemVencedor(self, texto, on_reiniciar=self._reiniciar_jogo)
        self.mensagem_vencedor.show()

    def _reiniciar_jogo(self):
        self.jogo.reiniciar_jogo()

        # Limpar as imagens dos blocos (supondo que você tenha referência para eles)
        for i in range(self.grid.count()):
            bloco = self.grid.itemAt(i).widget()
            layout = bloco.layout()
            if layout is not None:
                # Remove todos os widgets (bolinha, X) do layout
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

        if hasattr(self, 'mensagem_vencedor'):
            self.mensagem_vencedor.hide()
            self.mensagem_vencedor.deleteLater()
            del self.mensagem_vencedor

        self.view.abrir_tela(self.stack, self.tela_opcao)

    ###################  TELAS  ########################
    def tela_lista_blocos(self, n, m, largura=50, altura=50):
        scroll, self.grid = WidgetHelper.lista_grid()

        for i in range(n*m):
            bloco = self.bloco(i, largura, altura)
            self.grid.addWidget(bloco, i // m, i % m)
        return scroll

    def tela_jogo(self):
        tela = QWidget()

        # Layout horizontal principal (menu + conteúdo)
        layout_h = QHBoxLayout(tela)

        # Adiciona a barra lateral ao layout principal (inicialmente oculta)
        self.barra_lateral = self.menu_lateral()
        layout_h.addWidget(self.barra_lateral)
        
        # Layout vertical para o conteúdo da tela
        layout_conteudo = QVBoxLayout()

        barra_superior = self.barra_superior()
        layout_conteudo.addLayout(barra_superior)

        tela_lista = self.tela_lista_blocos(n=self.jogo.tamanho, m=self.jogo.tamanho)
        layout_conteudo.addWidget(tela_lista)

        # Agora adiciona o conteúdo principal no layout horizontal
        layout_h.addLayout(layout_conteudo)

        return tela
    
    ##############  TELAS DE CRIAÇÃO  #################

    def tela_inicial(self):
        tela = QWidget()
        layout_vertical = QVBoxLayout(tela)
        layout_vertical.addSpacing(100)

        layout_horizontal = QHBoxLayout()

        imagem1 = WidgetHelper.imagem("Images/campo-minado.png", scaled=150)
        layout_horizontal.addWidget(imagem1, Qt.AlignmentFlag.AlignLeft)

        titulo = WidgetHelper.label_b("CAMPO MINADO", font_size=80)
        layout_horizontal.addWidget(titulo)

        imagem2 = WidgetHelper.imagem("Images/campo-minado.png", scaled=150)
        layout_horizontal.addWidget(imagem2, Qt.AlignmentFlag.AlignRight)

        layout_vertical.addLayout(layout_horizontal, Qt.AlignmentFlag.AlignCenter)

        botao_jogar = WidgetHelper.botao(
            nome="JOGAR",
            largura=400, altura= 100,
            fonte= 80,
            backcolor="#D12A2A",
            hover='#FF4C4C',
            pressed='#E04343',
            border='solid #FF4C4C',
            acao= lambda: self.view.abrir_tela(self.stack, self.tela_opcao)
        )
        layout_vertical.addWidget(botao_jogar, alignment=Qt.AlignmentFlag.AlignCenter)

        return tela
    
    def tela_opcao(self):
        tela = QWidget()
        layout_vertical = QVBoxLayout(tela)

        layout_horizontal = QHBoxLayout()
    
        imagem1 = WidgetHelper.imagem("Images/campo-minado.png", scaled=150)
        layout_horizontal.addWidget(imagem1, Qt.AlignmentFlag.AlignLeft)

        titulo = WidgetHelper.label_b("Qual tamanho do tabuleiro?", font_size=50)
        layout_horizontal.addWidget(titulo)

        imagem2 = WidgetHelper.imagem("Images/campo-minado.png", scaled=150)
        layout_horizontal.addWidget(imagem2, Qt.AlignmentFlag.AlignRight)

        layout_vertical.addLayout(layout_horizontal, Qt.AlignmentFlag.AlignCenter)

        layout_horizontal = QHBoxLayout()

        opcao_1 = WidgetHelper.botao(
            nome="10x10",
            largura=400, altura= 100,
            fonte= 80,
            backcolor="#D12A2A",
            hover='#FF4C4C',
            pressed='#E04343',
            border='solid #FF4C4C',
            acao= lambda: (self.jogo.reiniciar_jogo(10), self.view.abrir_tela(self.stack, self.tela_jogo))
        )
        layout_horizontal.addWidget(opcao_1)

        opcao_2 = WidgetHelper.botao(
            nome="15x15",
            largura=400, altura= 100,
            fonte= 80,
            backcolor="#D12A2A",
            hover='#FF4C4C',
            pressed='#E04343',
            border='solid #FF4C4C',
            acao= lambda: (self.jogo.reiniciar_jogo(15), self.view.abrir_tela(self.stack, self.tela_jogo))
        )
        layout_horizontal.addWidget(opcao_2)
        layout_vertical.addLayout(layout_horizontal, Qt.AlignmentFlag.AlignCenter)
        layout_vertical.addSpacing(100)

        return tela
    
    def reiniciar_jogo(self):
        dialogo = CaixaConfirmacao(self, titulo="Confirmar saída", mensagem="Você tem certeza que deseja reiniciar o jogo?")
        resposta = dialogo.exec()

        if resposta == QDialog.DialogCode.Accepted:
            self.jogo.reiniciar_jogo(self.jogo.tamanho)
            self._reiniciar_jogo()

    ##########  PARTES DE TELAS  #############
    def menu_lateral(self):
        # Crie o menu lateral e esconda no início
        menu_lateral = QFrame()
        menu_lateral.setFrameShape(QFrame.Shape.StyledPanel)
        menu_lateral.setFixedWidth(250)
        menu_lateral.hide()

        # Layout para a barra lateral
        menu_layout = QVBoxLayout(menu_lateral)
        menu_layout.setSpacing(0)  # Definir o espaçamento entre os botões como 0
        menu_layout.setContentsMargins(0, 0, 0, 0)  # Remove as margens

        botao_reiniciar = WidgetHelper.botao(
            nome="Reiniciar Jogo", fontcolor="gray",
            backcolor="", hover="#3a3a3a", border="", pressed='#000000',
            largura=250, altura=100,
            acao= self.reiniciar_jogo
        )

        # Adicionando os botões ao layout da barra lateral
        menu_layout.addWidget(botao_reiniciar, alignment=Qt.AlignmentFlag.AlignHCenter)
        menu_layout.addStretch()  # Adiciona um espaçador para empurrar os botões para cima

        return menu_lateral
    
    def barra_superior(self):
        # Barra superior com botões
        barra_superior = QHBoxLayout()

        botao_menu = WidgetHelper.botao(
            nome="≡", fonte=40,
            largura=50, altura=50,
            backcolor="", hover="#3a3a3a", border="",
            pressed='#000000', fontcolor="gray",
            acao= self.toggle_menu
        )
        barra_superior.addWidget(botao_menu)

        return barra_superior

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CampoMinadoInterface()
    window.show()
    sys.exit(app.exec())
