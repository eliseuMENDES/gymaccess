import customtkinter as ctk
from tkinter import filedialog
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
import shutil
import os
import sys

# ==================== CONFIGURAÇÕES INICIAIS ====================
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "assets", "fotos"), exist_ok=True)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Identidade Visual (GymAccess Bahia)
BG_COLOR = "#121212"
SIDEBAR_COLOR = "#18181B"
CARD_COLOR = "#242427"
PURPLE_ACCENT = "#8A2BE2"
GOLD_ACCENT = "#D4AF37" 
TEXT_MAIN = "#FFFFFF"
TEXT_MUTED = "#A1A1AA"

# ==================== BANCO DE DADOS ====================
Base = declarative_base()

class Aluno(Base):
    __tablename__ = 'alunos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    matricula = Column(String(20), unique=True, nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    idade = Column(Integer, nullable=False)
    foto_path = Column(String(200), nullable=True)
    ativo = Column(Boolean, default=True)
    data_cadastro = Column(DateTime, default=lambda: datetime.now(timezone.utc))

db_path = os.path.join(BASE_DIR, "database", "academia.db")
engine = create_engine(f'sqlite:///{db_path}', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# ==================== APLICAÇÃO PRINCIPAL ====================
class GymApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GymAccess Bahia - Sistema de Gestão")
        self.geometry("1280x800")
        self.resizable(True, True)
        self.configure(fg_color=BG_COLOR)
        
        self.session = Session()
        self.foto_selecionada = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_sidebar()
        self.create_main_area()

    # --- BARRA LATERAL (SIDEBAR) ---
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color=SIDEBAR_COLOR)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)

        # Logo / Marca
        self.logo_label = ctk.CTkLabel(self.sidebar, text="GymAccess\nBahia", 
                                       font=ctk.CTkFont(size=26, weight="bold"), text_color=GOLD_ACCENT)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(40, 40))

        # Botões do Menu
        self.btn_nav_dash = self.create_nav_button("📊 Dashboard", "dashboard", 1)
        self.btn_nav_checkin = self.create_nav_button("🔓 Check-in", "checkin", 2)
        self.btn_nav_cad = self.create_nav_button("➕ Novo Aluno", "cadastro", 3)
        self.btn_nav_list = self.create_nav_button("📋 Base de Dados", "lista", 4)

        # Rodapé da Sidebar (Corrigido o parâmetro sticky)
        rodape = ctk.CTkLabel(self.sidebar, text="v2.0 • Admin", font=ctk.CTkFont(size=12), text_color=TEXT_MUTED)
        rodape.grid(row=5, column=0, sticky="s", pady=20)

    def create_nav_button(self, texto, frame_name, row):
        btn = ctk.CTkButton(self.sidebar, text=texto, fg_color="transparent", text_color=TEXT_MAIN, 
                            hover_color=CARD_COLOR, anchor="w", height=50, font=ctk.CTkFont(size=16),
                            command=lambda: self.select_frame(frame_name))
        btn.grid(row=row, column=0, padx=15, pady=5, sticky="ew")
        return btn

    # --- GERENCIADOR DE TELAS ---
    def create_main_area(self):
        self.frames = {}
        
        self.frames["dashboard"] = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.frames["checkin"] = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.frames["cadastro"] = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.frames["lista"] = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)

        self.build_dashboard(self.frames["dashboard"])
        self.build_checkin(self.frames["checkin"])
        self.build_cadastro(self.frames["cadastro"])
        self.build_lista(self.frames["lista"])

        self.select_frame("dashboard") # Inicia no Dashboard

    def select_frame(self, name):
        for frame in self.frames.values():
            frame.grid_forget()
            
        for btn in [self.btn_nav_dash, self.btn_nav_checkin, self.btn_nav_cad, self.btn_nav_list]:
            btn.configure(fg_color="transparent")

        self.frames[name].grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        
        # Destaca o botão ativo e atualiza dados da tela
        if name == "dashboard":
            self.btn_nav_dash.configure(fg_color=CARD_COLOR)
            self.atualizar_dados_dashboard()
        elif name == "checkin":
            self.btn_nav_checkin.configure(fg_color=CARD_COLOR)
        elif name == "cadastro":
            self.btn_nav_cad.configure(fg_color=CARD_COLOR)
        elif name == "lista":
            self.btn_nav_list.configure(fg_color=CARD_COLOR)
            self.atualizar_lista()

    # --- TELA 1: DASHBOARD ---
    def build_dashboard(self, frame):
        ctk.CTkLabel(frame, text="Visão Geral", font=ctk.CTkFont(size=32, weight="bold")).pack(anchor="w", pady=(0, 20))
        
        self.cards_frame = ctk.CTkFrame(frame, fg_color="transparent")
        self.cards_frame.pack(fill="x", pady=10)
        
        # Variáveis dinâmicas para os cards
        self.lbl_total_alunos = self.create_dash_card(self.cards_frame, "👥 Alunos Registrados", "0", PURPLE_ACCENT, 0)
        self.lbl_alunos_ativos = self.create_dash_card(self.cards_frame, "🟢 Alunos Ativos", "0", "#10B981", 1)
        self.lbl_alunos_inativos = self.create_dash_card(self.cards_frame, "🔴 Inativos", "0", "#EF4444", 2)

    def create_dash_card(self, parent, title, value, color, column):
        card = ctk.CTkFrame(parent, height=130, fg_color=CARD_COLOR, corner_radius=12)
        card.grid(row=0, column=column, padx=(0, 20), sticky="ew")
        parent.grid_columnconfigure(column, weight=1)
        
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16), text_color=TEXT_MUTED).pack(pady=(20, 5))
        lbl_valor = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=38, weight="bold"), text_color=color)
        lbl_valor.pack(pady=(0, 20))
        return lbl_valor

    def atualizar_dados_dashboard(self):
        # Consultas reais ao banco de dados SQLite
        total = self.session.query(Aluno).count()
        ativos = self.session.query(Aluno).filter_by(ativo=True).count()
        inativos = total - ativos
        
        self.lbl_total_alunos.configure(text=str(total))
        self.lbl_alunos_ativos.configure(text=str(ativos))
        self.lbl_alunos_inativos.configure(text=str(inativos))

    # --- TELA 2: CHECK-IN ---
    def build_checkin(self, frame):
        ctk.CTkLabel(frame, text="Ponto de Acesso", font=ctk.CTkFont(size=32, weight="bold")).pack(anchor="w", pady=(0, 30))
        
        card = ctk.CTkFrame(frame, fg_color=CARD_COLOR, corner_radius=15)
        card.pack(fill="x", padx=100, pady=20)

        self.matricula_entry = ctk.CTkEntry(card, placeholder_text="Digite a matrícula", 
                                           width=400, height=55, font=ctk.CTkFont(size=20), justify="center")
        self.matricula_entry.pack(pady=(40, 20))

        ctk.CTkButton(card, text="VALIDAR ACESSO", command=self.fazer_checkin, width=400, height=60, 
                      font=ctk.CTkFont(size=18, weight="bold"), fg_color=PURPLE_ACCENT).pack(pady=(10, 30))

        self.status = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=22, weight="bold"))
        self.status.pack(pady=(0, 40))

    # --- TELA 3: CADASTRO COMPLETO ---
    def build_cadastro(self, frame):
        ctk.CTkLabel(frame, text="Registrar Novo Aluno", font=ctk.CTkFont(size=32, weight="bold")).pack(anchor="w", pady=(0, 20))
        
        card = ctk.CTkFrame(frame, fg_color=CARD_COLOR, corner_radius=12)
        card.pack(fill="both", expand=True, pady=10)

        form_frame = ctk.CTkFrame(card, fg_color="transparent")
        form_frame.pack(pady=20, padx=40, fill="x")

        labels = ["Nome Completo", "Matrícula", "CPF", "Idade"]
        attrs = ["nome_entry", "matricula_cad_entry", "cpf_entry", "idade_entry"]
        
        for i, (label_text, attr) in enumerate(zip(labels, attrs)):
            col = i % 2
            row = i // 2
            box = ctk.CTkFrame(form_frame, fg_color="transparent")
            box.grid(row=row, column=col, padx=20, pady=10, sticky="ew")
            form_frame.grid_columnconfigure(col, weight=1)

            ctk.CTkLabel(box, text=label_text, font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0,5))
            entry = ctk.CTkEntry(box, height=45, font=ctk.CTkFont(size=16))
            entry.pack(fill="x")
            setattr(self, attr, entry)

        action_frame = ctk.CTkFrame(card, fg_color="transparent")
        action_frame.pack(fill="x", padx=60, pady=20)

        self.btn_foto = ctk.CTkButton(action_frame, text="📸 Selecionar Foto", command=self.selecionar_foto, height=50, width=200, fg_color="#3F3F46")
        self.btn_foto.pack(side="left")

        ctk.CTkButton(action_frame, text="SALVAR CADASTRO", command=self.cadastrar_aluno, height=50, width=250, 
                      font=ctk.CTkFont(weight="bold"), fg_color=GOLD_ACCENT, text_color="black").pack(side="right")

        self.cad_status = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=16))
        self.cad_status.pack(pady=10)

    # --- TELA 4: LISTA BASICA ---
    def build_lista(self, frame):
        ctk.CTkLabel(frame, text="Base de Dados", font=ctk.CTkFont(size=32, weight="bold")).pack(anchor="w", pady=(0, 20))
        self.list_text = ctk.CTkTextbox(frame, font=ctk.CTkFont(size=14), fg_color=CARD_COLOR, corner_radius=10)
        self.list_text.pack(fill="both", expand=True)

    # --- LÓGICA DO SISTEMA ---
    def selecionar_foto(self):
        file = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png")])
        if file:
            self.foto_selecionada = file
            self.btn_foto.configure(text="✅ Foto Anexada", fg_color="#10B981")

    def cadastrar_aluno(self):
        nome = self.nome_entry.get().strip()
        matricula = self.matricula_cad_entry.get().strip()
        cpf = self.cpf_entry.get().strip()
        idade_str = self.idade_entry.get().strip()

        if not all([nome, matricula, cpf, idade_str]):
            self.cad_status.configure(text="❌ Preencha todos os campos.", text_color="#EF4444")
            return

        try:
            idade = int(idade_str)
        except:
            self.cad_status.configure(text="❌ Idade inválida.", text_color="#EF4444")
            return

        foto_path = None
        if self.foto_selecionada:
            destino = os.path.join(BASE_DIR, "assets", "fotos", f"{matricula}.jpg")
            shutil.copy(self.foto_selecionada, destino)
            foto_path = destino

        novo_aluno = Aluno(nome=nome, matricula=matricula, cpf=cpf, idade=idade, foto_path=foto_path)

        try:
            self.session.add(novo_aluno)
            self.session.commit()
            self.cad_status.configure(text="✅ Salvo com sucesso!", text_color="#10B981")
            for entry in [self.nome_entry, self.matricula_cad_entry, self.cpf_entry, self.idade_entry]:
                entry.delete(0, 'end')
            self.foto_selecionada = None
            self.btn_foto.configure(text="📸 Selecionar Foto", fg_color="#3F3F46")
            self.atualizar_dados_dashboard()
        except:
            self.session.rollback()
            self.cad_status.configure(text="❌ Matrícula ou CPF já existem.", text_color="#EF4444")

    def fazer_checkin(self):
        matricula = self.matricula_entry.get().strip()
        if not matricula:
            self.status.configure(text="❌ Informe a matrícula", text_color="#EF4444")
            return
            
        aluno = self.session.query(Aluno).filter_by(matricula=matricula, ativo=True).first()
        if aluno:
            self.status.configure(text=f"🟢 ACESSO LIBERADO: {aluno.nome}", text_color="#10B981")
        else:
            self.status.configure(text="🔴 Acesso Negado", text_color="#EF4444")

    def atualizar_lista(self):
        self.list_text.delete("0.0", "end")
        alunos = self.session.query(Aluno).all()
        if not alunos:
            self.list_text.insert("end", "Nenhum dado.")
            return
        for a in alunos:
            status = "🟢" if a.ativo else "🔴"
            self.list_text.insert("end", f"{status} {a.nome} | Matrícula: {a.matricula} | CPF: {a.cpf}\n")

if __name__ == "__main__":
    app = GymApp()
    app.mainloop()