from flask import render_template, request, session, redirect, url_for
from app import app
from functools import wraps
import app.api as api

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

@app.route("/login", methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')

    res = api.loginUser(email, password)

    # If they FAIL to authenticate, return the error message
    if not res['success']:
      err = res['message']
      return render_template('login.html', err=err)

    session['userId'] = res['userId']

    return redirect(url_for('todos'))

  return render_template('login.html')

@LoginRequired
@app.route("/logout", methods=['GET', 'POST'])
def logout():
  session.clear()
  return redirect(url_for('index'))

@LoginRequired
@app.route("/todos", methods=['GET', 'POST'])
def todos():
  return render_template('todos.html')

@LoginRequired
@app.route("/create_todo", methods=['GET', 'POST'])
def create_todos():
  return render_template('create_todo.html')



