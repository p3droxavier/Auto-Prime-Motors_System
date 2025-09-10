from functools import wraps
from flask import  session, redirect, url_for, flash

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'id' not in session:
      flash("Você precisa estar logado para acessar essa página! ", "warning")
      return redirect(url_for('auth.login'))
    return f(*args, **kwargs)
  return decorated_function