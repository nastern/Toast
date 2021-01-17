from datetime import datetime
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
      return redirect(url_for('/'))
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
    session['current_topping'] = res['current_topping']

    return redirect(url_for('todos'))

  return render_template('login.html')

@app.route("/signup", methods=['POST'])
def signup():
  name = request.form.get('name')
  email = request.form.get('email')
  password = request.form.get('password')

  user = api.createUser(email, password, name)
  if not user['error']:
    session['userId'] = user['userId']
    session['current_topping'] = user['current_topping']
    return redirect(url_for('todos'))


  # MAKE A FEW FAKE TODOS JUST SO WE HAVE THEM TO DISPLAY!!
  import datetime
  api.createTodo(session['userId'], "Todo #1", datetime.datetime.now())
  api.createTodo(session['userId'], "Todo #2", datetime.datetime.now())
  api.createTodo(session['userId'], "Todo #3", datetime.datetime.now())


  return render_template('index.html', err=user['error'])

@LoginRequired
@app.route("/logout", methods=['GET', 'POST'])
def logout():
  session.clear()
  return redirect(url_for('index'))

@LoginRequired
@app.route("/todos", methods=['GET', 'POST'])
def todos():
  todos = api.getTodosForUser(session['userId'])
  return render_template('todos.html', todos=todos)

@LoginRequired
@app.route("/create_todo", methods=['POST'])
def create_todos():
  title = request.form.get('title')
  description = request.form.get('description')
  date = request.form.get('date')

  datetime_obj = datetime.strptime(date, '%m/%d/%Y')
  print(datetime_obj)

  api.createTodo(session['userId'], title, date, description)

  return redirect(url_for('todos'))



