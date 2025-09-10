from flask_bcrypt import Bcrypt
from app.database import db
from app.database.models.funcionario import Funcionario

bcrypt = Bcrypt()

def cadastrar_funcionario(data):
  senha_hash = bcrypt.generate_password_hash(data['senha']).decode('utf-8')
  
  novo_funcionario = Funcionario (
    nome=data['nome'], 
    email=data['email'],
    senha = senha_hash, 
    cpf=data['cpf'],
    cargo=data['cargo'],
    setor=data['setor'],
    telefone=data.get('telefone'),
    endereco=data.get('endereco'),
    data_admissao=data['data_admissao'],
    salario=data['salario'],
    foto=data.get('foto'),
  )
  
  # Persistindo no banco de dados
  db.session.add(novo_funcionario)
  db.session.commit()
  return novo_funcionario