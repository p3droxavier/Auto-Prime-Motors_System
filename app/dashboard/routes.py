from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__, template_folder='template')


# Rota para a dashboard
@dashboard_bp.route('/')
def dashboard():
  return render_template('dashboard.html')