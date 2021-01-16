from flask import render_template, request, session, redirect, url_for
from app import app
import app.auth as auth



def LoginRequired(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    if 'userId' in session:
      return f(*args, **kwargs)
    else:
      return redirect(url_for('login'))
  return wrapper


@app.route("/", methods=['GET', 'POST'])
def index():
  return render_template('index.html')
