from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__, template_folder='template')


# Rota para o formulário de login
@auth_bp.route('/login')
def login():
  return render_template('login.html')


# Rota para o formulário de cadastro (register)
@auth_bp.route('/register')
def register():
  return render_template('register.html')