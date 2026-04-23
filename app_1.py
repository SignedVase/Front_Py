import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QVBoxLayout
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont


class TiraObrigado(QWidget):
    """Segunda janela que sobrepõe a janela principal.

    Mesma largura da base, altura equivalente a 1/3, posicionada
    verticalmente centralizada sobre a janela pai.
    """

    def __init__(self, parent=None):
        super().__init__(
            parent,
            Qt.WindowType.Window
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint,
        )
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._setup_ui()
        self._setup_animation()

    def _setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0f0f1a;
                border: 2px solid #5b21b6;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("Muito Obrigado")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Georgia", 32, QFont.Weight.Bold))
        label.setStyleSheet("""
            color: #fbbf24;
            background: transparent;
            border: none;
            letter-spacing: 3px;
        """)
        layout.addWidget(label)

    def _setup_animation(self):
        self._anim = QPropertyAnimation(self, b"geometry")
        self._anim.setDuration(420)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def show_over(self, parent_geometry: QRect):
        """Exibe a tira centralizada sobre a janela pai, com animação de fade-in vertical."""
        w = parent_geometry.width()
        h = parent_geometry.height() // 3
        x = parent_geometry.x()
        # Centraliza verticalmente sobre a janela principal
        y = parent_geometry.y() + (parent_geometry.height() - h) // 2

        end = QRect(x, y, w, h)
        # Começa ligeiramente acima da posição final (efeito de descida suave)
        start = QRect(x, y - 40, w, h)

        self.setGeometry(start)
        self.show()
        self.raise_()

        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.start()

    def mousePressEvent(self, event):
        """Fecha a tira ao clicar nela."""
        self.close()


class PaginaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Página Principal")
        self.setMinimumSize(700, 500)
        self._tira = None
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a14;
            }
            QWidget#central {
                background-color: #0a0a14;
            }
        """)

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        # Layout principal
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        # Empurra o conteúdo levemente acima do centro
        layout.setContentsMargins(0, 0, 0, 80)

        layout.addStretch(2)   # espaço superior maior

        # ── Título ──────────────────────────────────────────────
        titulo = QLabel("Olá, Bem-vindo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setFont(QFont("Georgia", 42, QFont.Weight.Bold))
        titulo.setStyleSheet("""
            color: #9333ea;
            letter-spacing: 4px;
            background: transparent;
        """)
        layout.addWidget(titulo)

        layout.addSpacing(48)

        # ── Botão ────────────────────────────────────────────────
        btn = QPushButton("Clique Aqui")
        btn.setFont(QFont("Georgia", 18, QFont.Weight.DemiBold))
        btn.setFixedSize(200, 54)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                color: #7c3aed;
                background-color: transparent;
                border: 2px solid #7c3aed;
                border-radius: 27px;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                background-color: #1e1040;
                border-color: #a855f7;
                color: #a855f7;
            }
            QPushButton:pressed {
                background-color: #2d1565;
            }
        """)
        btn.clicked.connect(self.bemVindo)

        # Centraliza o botão num container
        btn_container = QWidget()
        btn_container.setStyleSheet("background: transparent;")
        btn_layout = QVBoxLayout(btn_container)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addWidget(btn)
        layout.addWidget(btn_container)

        layout.addStretch(3)   # espaço inferior maior

    # ── Função solicitada ────────────────────────────────────────
    def bemVindo(self):
        if self._tira and self._tira.isVisible():
            self._tira.close()
            return

        self._tira = TiraObrigado(self)
        self._tira.show_over(self.geometry())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Fecha a tira se a janela for redimensionada
        if self._tira and self._tira.isVisible():
            self._tira.close()

    def moveEvent(self, event):
        super().moveEvent(event)
        # Reposiciona a tira junto com a janela principal ao mover
        if self._tira and self._tira.isVisible():
            g = self.geometry()
            w = g.width()
            h = g.height() // 3
            x = g.x()
            y = g.y() + (g.height() - h) // 2
            self._tira.setGeometry(QRect(x, y, w, h))


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = PaginaPrincipal()
    window.resize(800, 560)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
