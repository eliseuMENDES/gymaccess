from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLineEdit, 
                               QPushButton, QLabel, QFrame, QMessageBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap
import sys
import os

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GymAccess - Login")
        self.setFixedSize(420, 580)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
        """)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)

        self.init_ui()

    def init_ui(self):
        # Logo / Título
        title = QLabel("GymAccess")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #8A2BE2;")
        self.layout.addWidget(title)

        subtitle = QLabel("Controle de Academia")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #AAAAAA;")
        self.layout.addWidget(subtitle)

        self.layout.addSpacing(30)

        # Campos
        self.username = QLineEdit()
        self.username.setPlaceholderText("Usuário ou Matrícula")
        self.username.setMinimumHeight(50)
        self.layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Senha")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMinimumHeight(50)
        self.layout.addWidget(self.password)

        self.layout.addSpacing(20)

        # Botão Login
        login_btn = QPushButton("ENTRAR")
        login_btn.setMinimumHeight(55)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #8A2BE2;
                color: white;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A45EFF;
            }
        """)
        login_btn.clicked.connect(self.handle_login)
        self.layout.addWidget(login_btn)

        # Rodapé
        footer = QLabel("© 2026 GymAccess - Todos os direitos reservados")
        footer.setFont(QFont("Arial", 9))
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #555555;")
        self.layout.addStretch()
        self.layout.addWidget(footer)

    def handle_login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Erro", "Preencha usuário e senha!")
            return

        # Por enquanto, login simples (vamos melhorar depois)
        if username == "admin" and password == "123456":
            self.close()
            from views.dashboard import DashboardWindow
            self.dashboard = DashboardWindow()
            self.dashboard.show()
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos!")

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())