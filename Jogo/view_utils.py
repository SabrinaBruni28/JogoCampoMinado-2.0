import sys, os, shutil

from PyQt6.QtGui import QPixmap, QMovie, QPainter
from PyQt6.QtCore import Qt, QTimer, QSize

from PyQt6.QtWidgets import (
   QPushButton, QApplication, QWidget, QLabel, QDialog,
   QVBoxLayout, QHBoxLayout, QFrame, QFileDialog, QScrollArea,
   QGridLayout
)

class WidgetHelper(QWidget):
    @staticmethod
    def caminho_absoluto(rel_path):
        try:
            base_path = sys._MEIPASS  # Quando executado como .exe com PyInstaller
        except AttributeError:
            base_path = os.path.abspath(".")  # Quando executado como script .py
        return os.path.join(base_path, rel_path)

    @staticmethod
    def lista_grid():
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        conteudo = QWidget()
        conteudo_layout = QHBoxLayout(conteudo)  # usa HBox para poder centralizar horizontalmente
        conteudo_layout.setContentsMargins(0, 0, 0, 0)
        conteudo_layout.setSpacing(0)

        grid_container = QWidget()
        vbox = QVBoxLayout(grid_container)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(5)
        vbox.addLayout(grid)
        vbox.addStretch()

        conteudo_layout.addStretch()         # Centraliza o grid_container horizontalmente
        conteudo_layout.addWidget(grid_container)
        conteudo_layout.addStretch()

        scroll.setWidget(conteudo)

        return scroll, grid

    @staticmethod
    def label_preco(preco_label, aligment=Qt.AlignmentFlag.AlignCenter, tamanho=30):
        preco_label = QLabel(f"<span style='font-size: {tamanho}px; color: green'>R$ {'{:.2f}'.format(float(preco_label))}</span>")
        preco_label.setAlignment(aligment)
        return preco_label

    @staticmethod
    def label_b(label, font_size=20, alignment=Qt.AlignmentFlag.AlignCenter, color="#E0E0E0"):
        label_b = QLabel(f"<b>{label}</b>")
        label_b.setAlignment(alignment)
        label_b.setStyleSheet(f"""
            font-size: {font_size}px;
            color: {color};
        """)
        return label_b
    
    @staticmethod
    def label_span(label, tamanho, alignment=Qt.AlignmentFlag.AlignCenter):
        label_span = QLabel(f"<span style='font-size: {tamanho}px; font-weight: bold'>{label}</span>")
        label_span.setAlignment(alignment)
        return label_span

    @staticmethod
    def bloco(largura, altura):
        bloco = QFrame()
        bloco.setFixedSize(QSize(largura, altura))
        bloco.setFrameShape(QFrame.Shape.StyledPanel)
        bloco.setStyleSheet("""
            QFrame {
                border: 1px;
                border-radius: 8px;
                background-color: #fff;
                color: #000;
                font-size: 20px;
            }
            QFrame:hover {
                background-color: #f0f0f0;
            }
        """)
        return bloco

    @staticmethod
    def imagem(imagem, scaled=200, pixmap=False):
        imagem_label = QLabel()
        caminho = WidgetHelper.caminho_absoluto(imagem)

        # Carrega a imagem original
        original_pixmap = QPixmap(caminho)

        # Redimensiona mantendo a proporção, sem ultrapassar o tamanho definido
        imagem_redimensionada = original_pixmap.scaled(
            scaled, scaled,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        # Cria um pixmap quadrado branco com o tamanho total desejado
        base_pixmap = QPixmap(scaled, scaled)
        base_pixmap.fill(Qt.GlobalColor.transparent)

        # Desenha a imagem redimensionada no centro da base
        painter = QPainter(base_pixmap)
        x = (scaled - imagem_redimensionada.width()) // 2
        y = (scaled - imagem_redimensionada.height()) // 2
        painter.drawPixmap(x, y, imagem_redimensionada)
        painter.end()

        # Define o pixmap final no label
        imagem_label.setPixmap(base_pixmap)
        imagem_label.setFixedSize(scaled, scaled)
        imagem_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if pixmap:
            return imagem_label.pixmap()
        return imagem_label

    @staticmethod
    def mostrar_alerta_temporario(
        parent_widget, mensagem, duracao_ms=3000,
        largura=400, altura=50, fonte=20,
        paddingH=20, paddingV=20,
        fontcolor='white', backcolor='#0078d7',
        border='#000000',
        posicao='inferior_direita'  # <-- novo parâmetro
    ):
        alerta = QLabel(mensagem, parent_widget)
        alerta.setFixedSize(largura, altura)
        alerta.setStyleSheet(f"""
            QLabel {{
                background-color: {backcolor};
                color: {fontcolor};
                border: 2px solid {border};
                border-radius: 2px;
                padding: 5px;
                font-weight: bold;
                font-size: {fonte}px;
            }}
        """)

        alerta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Coloca o alerta por cima de tudo
        alerta.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip)
        alerta.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        # Calcula a posição com base na string
        parent_pos = parent_widget.mapToGlobal(parent_widget.rect().topLeft())
        x = y = 0

        if 'direita' in posicao:
            x = parent_pos.x() + parent_widget.width() - largura - paddingH
        elif 'esquerda' in posicao:
            x = parent_pos.x() + paddingH

        if 'superior' in posicao:
            y = parent_pos.y() + paddingV
        elif 'inferior' in posicao:
            y = parent_pos.y() + parent_widget.height() - altura - paddingV

        alerta.move(x, y)
        alerta.show()

        QTimer.singleShot(duracao_ms, alerta.close)

    @staticmethod
    def copiar_texto(label: QLabel):
        clipboard = QApplication.clipboard()
        texto_sem_html = label.text()  # Isso ainda está com HTML
        # Se quiser extrair só o texto puro:
        from PyQt6.QtGui import QTextDocument
        doc = QTextDocument()
        doc.setHtml(texto_sem_html)
        texto_puro = doc.toPlainText()

        clipboard.setText(texto_puro)

    @staticmethod
    def botao(
        nome, fonte = 20, largura = 110, altura = 30, 
        fontcolor = 'white', backcolor='#0078d7', 
        hover='#005fa3', pressed='#003f7f',
        border = 'solid #005fa3',
        acao = None,
    ):
        botao = QPushButton(nome)
        botao.setFixedSize(largura, altura)
        botao.setStyleSheet(f"""
            QPushButton {{
                background-color: {backcolor};
                color: {fontcolor};
                border: 2px {border};
                border-radius: 10px;
                font-weight: bold;
                font-size: {fonte}px;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {pressed};
            }}
        """)
        if acao:
            botao.clicked.connect(acao)

        return botao
    
    @staticmethod
    def abrir_dialogo_arquivo(parent):
        caminho_arquivo, _ = QFileDialog.getOpenFileName(
            parent,
            "Escolher arquivo",
            "",
            "Imagens (*.png *.jpg *.jpeg  *.webp *.gif)"
        )

        if caminho_arquivo:
            # Caminho de destino onde o arquivo será salvo (pode mudar para o que quiser)
            nome_arquivo = os.path.basename(caminho_arquivo)
            destino = os.path.join("uploads", nome_arquivo)

            # Cria a pasta "uploads" se ela não existir
            os.makedirs("uploads", exist_ok=True)

            # Copia o arquivo para a pasta destino
            shutil.copy(caminho_arquivo, destino)
            return nome_arquivo

class ViewHelper(QWidget):
    funcoes_telas = []

    def __init__(self):
        pass

    def set_tela(self, stack, index):
        total = stack.count()

        # Converte índice negativo em positivo
        if index < 0:
            index = total + index

        if index < 0 or index >= total:
            return

        # Chama novamente a função para obter a tela atualizada
        funcao_criadora = self.__class__.funcoes_telas[index]
        self.sobrescrever_tela(stack, funcao_criadora, index)

    def voltar_tela(self, stack, excluir_funcao = True, atualizar_tela=True):
        index = stack.currentIndex()
        stack.setCurrentIndex(index - 1)
        self.excluir_tela(stack, index, excluir_funcao)
        if atualizar_tela:
            self.atualiza_tela(stack)

    def abrir_tela(self, stack, funcao_criadora, excluir_anterior=False, salvar_tela=True):
        tela = funcao_criadora()
        if not tela:
            return None
        
        if salvar_tela:
            self.__class__.funcoes_telas.append(funcao_criadora)

        if excluir_anterior:
            index = stack.currentIndex()
            self.excluir_tela(stack, index, excluir_funcao=False)

        stack.addWidget(tela)
        stack.setCurrentWidget(tela)

    def excluir_tela(self, stack, index, excluir_funcao = True):
        widget = stack.widget(index)
        stack.removeWidget(widget)
        widget.deleteLater()
        if excluir_funcao:
            del self.__class__.funcoes_telas[index]

    def sobrescrever_tela(self, stack, funcao_criadora: QWidget, index: int = None, atualizar_tela=True):
        if index is None:
            index = stack.currentIndex()

        total = stack.count()

        # Converte índice negativo em positivo
        if index < 0:
            index = total + index

        if index < 0 or index >= total:
            return

        if 0 <= index < stack.count():
            self.excluir_tela(stack, index, excluir_funcao=False)
            tela = funcao_criadora()
            stack.insertWidget(index, tela)
            if index < len(self.__class__.funcoes_telas):
                self.__class__.funcoes_telas[index] = funcao_criadora
            else:
                self.__class__.funcoes_telas.insert(index, funcao_criadora)
            if atualizar_tela:
                stack.setCurrentIndex(index)
                # Remove widgets e funções após o índice atual
                for i in range(len(self.__class__.funcoes_telas) - 1, index, -1):
                    if i < stack.count():
                        self.excluir_tela(stack, i, excluir_funcao=True)
                    else:
                        # Só remove da lista de funções, caso não exista mais o widget
                        del self.__class__.funcoes_telas[i]

    def atualiza_tela(self, stack):
        index = stack.currentIndex()
        funcao_criadora = self.__class__.funcoes_telas[index]
        self.sobrescrever_tela(stack, funcao_criadora, index)

    @staticmethod
    def tela_carregando_com_spinner(mensagem="Carregando...", gif_path="spinner.gif"):
        tela = QWidget()
        layout = QVBoxLayout(tela)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Spinner animado
        spinner = QLabel()
        movie = QMovie(gif_path)
        spinner.setMovie(movie)
        movie.start()

        # Mensagem opcional
        texto = QLabel(f"<span style='font-size: 20px'>{mensagem}</span>")
        texto.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(spinner)
        layout.addWidget(texto)

        return tela

    @staticmethod
    def tela_carregando(mensagem="Carregando..."):
        tela = QWidget()
        layout = QVBoxLayout(tela)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel(f"<span style='font-size: 24px'>{mensagem}</span>")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        return tela

class CaixaConfirmacao(QDialog):
    def __init__(self, parent=None, titulo=None, mensagem = None,  color="#E0E0E0", fonte=20, largura=400, altura=100):
        super().__init__(parent)
        self.setWindowTitle(titulo)
        self.setMinimumSize(largura, altura)

        layout = QVBoxLayout()
        mensagem = QLabel(f"<p style='font-size:{fonte}px; color: {color};'>{mensagem}</p>", self)
        layout.addWidget(mensagem)

        botoes = QHBoxLayout()
        btn_sim = QPushButton("Sim", self)
        btn_nao = QPushButton("Não", self)

        btn_sim.setStyleSheet(f"color: {color}; font-size: 18px;")
        btn_nao.setStyleSheet(f"color: {color}; font-size: 18px;")

        botoes.addWidget(btn_sim)
        botoes.addWidget(btn_nao)

        layout.addLayout(botoes)
        self.setLayout(layout)

        btn_sim.clicked.connect(self.accept)
        btn_nao.clicked.connect(self.reject)