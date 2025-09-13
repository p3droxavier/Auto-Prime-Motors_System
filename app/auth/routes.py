from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, UserMixin, login_required, current_user, logout_user
from app.auth.schemas import RegisterSchema 
from app.auth.services import cadastrar_funcionario
from app.database.models.funcionario import Funcionario
from werkzeug.security import check_password_hash, generate_password_hash
import os


auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Necessario para salvar as fotos
UPLOAD_FOLDER = "app/static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


# Login do admim fixo.
class AdminUser(UserMixin):
  def __init__(self, id, nome, cpf, setor, cargo, senha, is_admin=False):
    self.id = id
    self.nome = nome
    self.cpf = cpf
    self.setor = setor
    self.cargo = cargo
    self.senha_hash = generate_password_hash(senha)
    self.is_admin = is_admin
    
  def verificar_senha(self, senha):
    return check_password_hash(self.senha_hash, senha)
    
#Usuário admin fixo (mock)
fake_admin = AdminUser(
  id=999, 
  nome="Admin01",
  cpf="23445634534",
  cargo="Adm",
  setor="Adm", 
  senha="admin01",
  is_admin=True
)
# ========================


# Coleta os dados da requisição e envia para a service
# Rota para o formulário de cadastro (register)
@auth_bp.route('/register', methods=["GET", "POST"])
def register():
  if request.method == "POST":
    print("Formulario recebido")
    print(request.form.to_dict())
    
    
    # Capturando a foto do funcionário
    form_data = request.form.to_dict()
    foto = request.files.get("foto") # <- Imagem recebida aqui
    
    
    form_data = request.form.to_dict()
    
    # Processando campos salário, data_admissao vindo como string
    try:
      form_data['salario'] = str(form_data['salario'])
    except:
      print("erro no primeiro try cast feito")
      pass
    
    schema = RegisterSchema()
    errors = schema.validate(form_data)
    
    if errors:
      flash(f"Erro de validação: {errors}", "danger")
      print("Erro de validação: ", errors) #Debug para ver o erro, caso ocorra  
      return render_template("auth/register.html", data=form_data)
    
    # fazer a verificação de duplicidade de dados unicos, como CPF, E-MAIL e TEFEFONE 
    try:
      validated_data = schema.load(form_data)
      
      # Passando a foto separadamente
      cadastrar_funcionario(validated_data, foto)
      
      
      flash("Funcionario cadastrado com sucesso!", "success")
      return redirect(url_for('auth.login'))
    except Exception as e:
      print("Erro segundo try cast: ", e)
      flash(f"Erro ao cadastrar: {str(e)}", "danger")
      return redirect("auth/register.html", data=form_data)
    
  return render_template('auth/register.html')



# Rota para o formulário de login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  
  # Capturando quando o usuário não logado for jogado para o login
  next_page = request.args.get('next')
  
  if request.method == 'POST':
    nome = request.form['nome']
    cpf = request.form['cpf']
    cargo = request.form['cargo']
    setor = request.form['setor']
    senha = request.form['senha']
    
    
    # 1 - Verificação do admin fixo
    if(
      nome == fake_admin.nome and
      cpf == fake_admin.cpf and
      cargo == fake_admin.cargo and
      setor == fake_admin.setor and
      fake_admin.verificar_senha(senha)
    ):
      login_user(fake_admin)
      flash("Login de administrador realiza com sucesso!", "success")
      return redirect(next_page or url_for('admin_dashboard.admin_dashboard')) # SE DER ALGUM ERRO VERIFICAR AQUI
    
    
    # 2 - Caso contrário, continua a lógica normal de funcionário
    funcionario = Funcionario.query.filter_by(cpf = cpf).first()
    
    if funcionario:
      if(
        funcionario.nome == nome and
        funcionario.cargo == cargo and
        funcionario.setor == setor and
        funcionario.verificar_senha(senha)
      ):
        # Login bem sucedido
        login_user(funcionario) # Salva o login na sessão usando o mecanismo flask-Login
        flash("Login realizado com sucesso! ", "success")
        return redirect(next_page or url_for('dashboard.dashboard'))
  
    flash('Dados Incorretos. Verifique as informações digitadas...')
    return redirect(url_for('auth.login'))
  
  return render_template('auth/login.html')



# Filtro de segurança onde o usuário so pode fazer upload de arquivos permitidos.
def allowed_file(filename):
  return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@auth_bp.route("/update", methods=["GET", "POST"])
@login_required
def update_profile():
  
  if request.method == 'POST':
    nome = request.form.get("nome")
    telefone = request.form.get("telefone")
    endereco = request.form.get("endereco")
    foto = request.files.get("foto")
    
    
    # Atualiza apenas campos permitidos
    if nome:
      current_user.nome = nome
    if telefone:
      current_user.telefone = telefone
    if endereco:
      current_user.endereco = endereco
      
      
    # Upload da foto
    if foto and allowed_file(foto.filename):#<- Verifica extensão do arquivo
      filename = f"{current_user.id}_{foto.filename}"#<-Cria um nome pro arquivo
      filepath = os.path.join(UPLOAD_FOLDER, filename)#<-Define um caminho
      foto.save(filepath)
      current_user.foto = filename
      
      
    # Persiste e salva no banco de dados as alterações 
    try:
      from app import db
      db.session.commit()
      flash("Dados atualizados com sucesso!", "sucesso")
      
    except Exception as e:
      flash(f"Erro ao atualizar: {str(e)}", "danger")
      
  return redirect(url_for("dashboard.dashboard"))



# Sera chamado na dashboard para logout
@auth_bp.route("/logout")
def logout():
  logout_user()
  return render_template('auth/login.html')