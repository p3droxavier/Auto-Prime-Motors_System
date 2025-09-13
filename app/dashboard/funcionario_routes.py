import os
from flask import Blueprint, flash, redirect, render_template, request
from app.utils.auth_decorators import login_required
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')


# Rota para a dashboard
@dashboard_bp.route('/')
@login_required
def dashboard():
  # passando variavel de pagina ativa para o tamplate, pegando a aba que deve ser exibida por query, string ou defoult
  aba = request.args.get('aba', 'meus_dados') # <- Padrão, retornara meus dados ao entrar na dashboard TESTE
  return render_template('dashboard/dashboard.html', funcionario=current_user) #<- Passa que tem um funcionario logado
