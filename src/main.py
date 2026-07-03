import sys
import os
from PySide6.QtWidgets import QApplication

# Adicionamos "src." antes dos imports para o Python achar as pastas
from src.views.dashboard import DashboardWindow
from src.controllers.aluno_controller import AlunoController

def main():
    app = QApplication(sys.argv)
    
    # Caminhos
    db_path = os.path.join(os.getcwd(), "database", "academia.db")
    
    # Inicia Controller e View
    controller = AlunoController(db_path)
    dashboard = DashboardWindow()
    
    dashboard.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()