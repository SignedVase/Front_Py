from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton
from PyQt6.QtCore import Qt

app = QApplication([])

janela = QMainWindow()

label = QLabel('Oi', janela)
label.setAlignment(Qt.AlignmentFlag.AlignCenter)
label.setStyleSheet("color: black;")
label.resize(400,300)

botao = QPushButton("Clique Aqui", janela)
botao.move(150,100)
botao.resize(120,40)

janela.resize(400,300)
janela.show()
app.exec()