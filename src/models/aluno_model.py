from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Aluno(Base):
    __tablename__ = 'alunos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    matricula = Column(String(20), unique=True, nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    idade = Column(Integer, nullable=False)
    foto_path = Column(String(200))
    ativo = Column(Boolean, default=True)
    data_cadastro = Column(DateTime, default=lambda: datetime.now(timezone.utc))