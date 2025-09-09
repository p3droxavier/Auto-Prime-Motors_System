from app.database import db
from flask_login import UserMixin

class Funcionario(db.Model, UserMixin):
  __tablename__ = 'funcionarios'
  
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100), nullable=False)
  cpf = db.Column(db.String(11), unique=True, nullable=False)
  cargo = db.Column(db.String(50), nullable=False)
  setor = db.Column(db.String(50), nullable=False)
  data_admissao = db.Column(db.Date, nullable=False)
  salario = db.Column(db.Numeric(10, 2), nullable=False)
  endereco = db.Column(db.Text, nullable=True)
  telefone = db.Column(db.String(15), nullable=True)
  email = db.Column(db.String(100), unique=True, nullable=False)
  foto = db.Column(db.String(255), nullable=True)
  senha = db.Column(db.String(128), nullable=False)
  
  def __repr__(self):
    return f'<Funcionario {self.nome}>'