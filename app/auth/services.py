import os
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from app.database import db
from app.database.models.funcionario import Funcionario

bcrypt = Bcrypt()

UPLOAD_FOLDER = "app/static/uploads"

 
def cadastrar_funcionario(data, foto=None):
  senha_hash = bcrypt.generate_password_hash(data['senha']).decode('utf-8')
  
 
  
  foto_filename = None
  if foto and foto.filename != "":
    foto_filename = secure_filename(foto.filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    foto.save(os.path.join(UPLOAD_FOLDER, foto_filename))
  
  
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
    foto=foto_filename # <- salva o nome do arquivo real
  )
  
  # Persistindo no banco de dados
  db.session.add(novo_funcionario)
  db.session.commit()
  return novo_funcionario