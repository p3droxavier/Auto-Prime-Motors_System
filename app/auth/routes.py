from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user
from app.auth.schemas import RegisterSchema 
from app.auth.services import cadastrar_funcionario
from app.database.models.funcionario import Funcionario

auth_bp = Blueprint('auth', __name__, template_folder='templates')


# Rota para o formulário de cadastro (register)
@auth_bp.route('/register', methods=["GET", "POST"])
def register():
  if request.method == "POST":
    print("Formulario recebido")
    print(request.form.to_dict())
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
      cadastrar_funcionario(validated_data)
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