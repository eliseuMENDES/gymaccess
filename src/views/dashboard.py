from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PySide6.QtCore import Qt

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GymAccess Pro | Painel de Controle")
        self.resize(1200, 800)
        
        # Aplicando estilo global profissional (QSS)
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QFrame#Card { 
                background-color: #1E1E1E; 
                border-radius: 12px; 
                border: 1px solid #333; 
            }
            QLabel { color: #E0E0E0; font-family: 'Segoe UI'; }
            QPushButton { 
                background-color: #8A2BE2; 
                color: white; 
                border-radius: 6px; 
                padding: 8px; 
            }
            QPushButton:hover { background-color: #A45EFF; }
        """)

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Header Área
        header = QLabel("DASHBOARD")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #8A2BE2;")
        layout.addWidget(header)

        # Dashboard Grid
        grid = QHBoxLayout()
        grid.addWidget(self.create_card("Alunos Ativos", "324"))
        grid.addWidget(self.create_card("Check-ins Hoje", "87"))
        layout.addLayout(grid)

    def create_card(self, title, value):
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedSize(250, 120)
        
        layout = QVBoxLayout(card)
        layout.addWidget(QLabel(title))
        
        val_lbl = QLabel(value)
        val_lbl.setStyleSheet("font-size: 32px; font-weight: bold;")
        layout.addWidget(val_lbl)
        
        return card