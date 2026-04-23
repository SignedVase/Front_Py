from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton
from PyQt6.QtCore import Qt
class SegundaJanela(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Segunda Janela")
        self.resize(300, 200)
        label2 = QLabel('Bom dia', self)
        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label2.setStyleSheet("color: black;")
        label2.resize(300, 200)

class JanelaPrin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("janela principal")
        self.resize(400, 300)
        label = QLabel('Hi', self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: black;")
        label.resize(400, 300)

        botao = QPushButton("Abrir Janela 2", self)
        botao.move(120,120)
        botao.clicked.connect(self.abrir_segunda)

    def abrir_segunda(self):
        self.segunda = SegundaJanela()
        self.segunda.show()  # não bloqueia a janela principal

app = QApplication([])
janela = JanelaPrin()
janela.show()
app.exec()