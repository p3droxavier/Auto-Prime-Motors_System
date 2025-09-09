from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.auth.schemas import RegisterSchema 
from app.auth.services import cadastrar_funcionario

auth_bp = Blueprint('auth', __name__, template_folder='template')


# Rota para o formulário de cadastro (register)
@auth_bp.route('/register', methods=["GET", "POST"])
def register():
  if request.method == "POST":
    print("Formulario recebido")
    print(request.form.to_dict())
    form_data = request.form.to_dict()
    
    # Processando campos salário, data_admissao vindo como string
    try:
      print("primeiro try cast feito")
      form_data['salario'] = str(form_data['salario'])
    except:
      print("erro no primeiro try cast feito")
      pass
    
    schema = RegisterSchema()
    errors = schema.validate(form_data)
    
    if errors:
      flash(f"Erro de validação: {errors}", "danger")
      print("Erro de validação: ", errors)
      return render_template("auth/register.html", data=form_data)
    
    try:
      print("Segundo try cast rodando")
      validated_data = schema.load(form_data)
      cadastrar_funcionario(validated_data)
      flash("Funcionario cadastrado com sucesso!", "success")
      return redirect(url_for('auth.login'))
    except Exception as e:
      print("Erro segundo try cast rodando: ", e)
      flash(f"Erro ao cadastrar: {str(e)}", "danger")
      return render_template("auth/register.html", data=form_data)
    
  return render_template('auth/register.html')



# Rota para o formulário de login
@auth_bp.route('/login')
def login():
  return render_template('auth/login.html')