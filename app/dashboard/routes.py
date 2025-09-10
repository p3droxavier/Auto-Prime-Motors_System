from flask import Blueprint, render_template
from app.utils.auth_decorators import login_required
from flask_login import login_required

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')


# Rota para a dashboard
@dashboard_bp.route('/')
@login_required
def dashboard():
  return render_template('dashboard/dashboard.html')