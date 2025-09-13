from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user

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



