from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import abort

admin_dashboard_bp = Blueprint("admin_dashboard", __name__, template_folder="../templates")

@admin_dashboard_bp.route("/admin")
@login_required
def admin_dashboard():
  #Garante que apenas o admin acesse
  if not getattr(current_user, "is_admin", False):
    return abort(403) # Acesso negado se não for admin
  
  return render_template("dashboard/admin_dashboard.html", user=current_user)