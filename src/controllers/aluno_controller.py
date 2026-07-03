from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.aluno_model import Base, Aluno

class AlunoController:
    def __init__(self, db_path):
        engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
    
    def get_session(self):
        return self.Session()