from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QFrame, QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GymAccess - Dashboard")
        self.setMinimumSize(1200, 700)
        self.setStyleSheet("background-color: #1E1E1E; color: white;")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #6A1B9A; border-radius: 10px;")
        header_layout = QHBoxLayout(header)
        
        title = QLabel("GymAccess")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        header_layout.addWidget(title, alignment=Qt.AlignCenter)
        
        layout.addWidget(header)

        # Cards
        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)
        
        self.create_card(cards_layout, "👥 Alunos Ativos", "348", "#22C55E", 0, 0)
        self.create_card(cards_layout, "📅 Check-ins Hoje", "124", "#3B82F6", 0, 1)
        self.create_card(cards_layout, "🔥 Treinando Agora", "41", "#F59E0B", 1, 0)
        self.create_card(cards_layout, "📊 Taxa de Ocupação", "78%", "#8B5CF6", 1, 1)

        layout.addLayout(cards_layout)

        # Botões rápidos
        btn_layout = QHBoxLayout()
        btn_checkin = QPushButton("Fazer Check-in")
        btn_checkin.setMinimumHeight(60)
        btn_checkin.clicked.connect(self.open_checkin)
        btn_layout.addWidget(btn_checkin)

        btn_cadastrar = QPushButton("Cadastrar Aluno")
        btn_cadastrar.setMinimumHeight(60)
        btn_layout.addWidget(btn_cadastrar)

        layout.addLayout(btn_layout)

    def create_card(self, layout, title, value, color, row, col):
        card = QFrame()
        card.setStyleSheet(f"""
            background-color: #2A2A2A;
            border-radius: 12px;
            padding: 20px;
        """)
        card_layout = QVBoxLayout(card)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 36, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        card_layout.addWidget(value_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14))
        card_layout.addWidget(title_label)
        
        layout.addWidget(card, row, col)

    def open_checkin(self):
        # Vamos implementar depois
        print("Check-in aberto")

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())