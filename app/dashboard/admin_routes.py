from flask import Blueprint, flash, redirect, render_template, request, abort, url_for
from flask_login import login_required, current_user

from app.database import db
from app.database.models.funcionario import Funcionario

admin_dashboard_bp = Blueprint("admin_dashboard", __name__, template_folder="../templates")

@admin_dashboard_bp.route("/admin")
@login_required
def admin_dashboard():
  
  # Gerenciamento de rotas admin
  aba = request.args.get('aba', 'todos_os_funcionarios')
  
  #Garante que apenas o admin acesse
  if not getattr(current_user, "is_admin", False):
    return abort(403) # Acesso negado se não for admin
  
  funcionarios = Funcionario.query.all()
  return render_template("dashboard/admin_dashboard.html", user=current_user, funcionarios=funcionarios)



# Função de deletar funcionários
@admin_dashboard_bp.route("/delete_funcionario/<int:id>", methods=["POST"])
@login_required
def delete_funcionario(id):
  if not getattr(current_user, "is_admin", False):
    return abort(403) # Acesso negado se não for admin
  
  funcionario = Funcionario.query.get_or_404(id) # Se não achar no banco, volta erro ao inves de none
  
  # removendo o funcionario do banco
  
  db.session.delete(funcionario)  
  db.session.commit()
  
  flash(f"Funcionario {funcionario.nome} deletado com sucesso!", "success")
  return redirect(url_for("admin_dashboard.admin_dashboard", user=current_user, id=funcionario))

