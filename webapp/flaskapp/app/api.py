from firebase_admin import credentials
import pyrebase
import firebase_admin
from firebase_admin import firestore
import requests
import ast
import datetime
import pytz

config = {
  "apiKey": "AIzaSyChN6zUmOTt9h6vBSHP72XXSGaOb7o2TaM",
  "authDomain": "toast-6ee26.firebaseapp.com",
  "databaseURL": "https://toast.firebaseio.com",
  "storageBucket": "toast-6ee26.appspot.com",
  "serviceAccount": "./app/config/serviceAccount.json"
}

pyrebase = pyrebase.initialize_app(config)
credentials = firebase_admin.credentials.Certificate("./app/config/serviceAccount.json")
firebase = firebase_admin.initialize_app(credential=credentials)


def createUser(email, password, name):
  '''
    args:
      email: the email associated with the new account
      password: the password associated with the new account
      name: the name of the new account

    returns:
      res: {}
  '''
  res = {
    'userId': None,
    'error': None,
    'current_topping': 'default.png'
  }
  try:
    pyrebase_auth = pyrebase.auth()
    user = pyrebase_auth.create_user_with_email_and_password(email, password)
    user = pyrebase_auth.refresh(user['refreshToken'])
  except requests.exceptions.HTTPError as err:
    # Actual error message for data
    # errorDict = ast.literal_eval(err.strerror)
    # message = errorDict["error"]["message"]
    res['error'] = "An account with that email already exists. Please log in."
    return res

  userId = user['userId']
  res['userId'] = userId

  db = firestore.client()
  doc_ref = db.collection('users').document(userId)

  doc_ref.set({
    'userId': userId,
    'todos': [],
    'email': email,
    'name': name,
    'toppings': [],
    'current_topping': 'default.png'
  })

  return res

def loginUser(email, password):
    '''
      args:
        email: email to login
        password: password to login

      returns:
        response: {"success": False, "message": None, "userId": None, "idToken": None, "refreshToken": None}}
    '''
    response = {"success": False, "message": None, "userId": None, "idToken": None, "refreshToken": None, "current_topping": None}
    pyrebase_auth = pyrebase.auth()

    try:
      user = pyrebase_auth.sign_in_with_email_and_password(email, password)
      user = pyrebase_auth.refresh(user['refreshToken'])
      userId = user['userId']
      idToken = user['idToken']
      refreshToken = user['refreshToken']

      response["success"] = True
      response["message"] = "Successfully authenticated."
      response['userId'] = userId
      response['idToken'] = idToken
      response['refreshToken'] = refreshToken
      response['current_topping'] = user['current_topping']
    except:
      response["message"] = "Failed to authenticate. Either username or password is incorrect."
    return response

def createTodo(userId, title, dueDate, description="", completed=False, isFocus=False, category="Default"):
  '''
    args:
      userId: the userId associated with the new todo item
      title: the title of the new todo
      dueDate: when this todo is due. must conform to datetime.datetime date
      description: the optional argument of the todo description
      completed: defaulted to False unless you want to create a todo that is already completed
      isFocused: defaulted to False, set to true if this is a focused todo
      category: what category does this belong to?
  '''
  new_todo = {
    'title': title,
    'description': description,
    'completed': completed,
    'isFocus': isFocus,
    'category': category,
    'dueDate': dueDate
  }

  db = firestore.client()
  # Add the todo
  (_, todo) = db.collection('todos').add(new_todo)

  # Add the todo ID to the users table
  db.collection('users').document(userId).update({
    'todos': firestore.ArrayUnion([todo.id])
  })

def getUser(userId):
  '''
    args:
      userId: the userId to get the data for
    returns:
      user: all of the data about that user
  '''
  db = firestore.client()
  user = db.collection('users').document(userId).get().to_dict()
  return user

def getTodo(todoId):
  '''
    args:
      todoId: gets the todo associated with the ID
    returns:
      user: the todo data
  '''
  db = firestore.client()
  todo = db.collection('todos').document(todoId).get().to_dict()
  return todo

def getTodosForUser(userId):
  '''
    args:
      userId: the userId to get the data for
    returns:
      todos: all of the todos associated with a specific user
  '''
  user = getUser(userId)
  user_todos = user['todos']

  utc = pytz.UTC
  current_date = datetime.datetime.now(tz=utc).date()

  todos = {
    'upcoming': {},
    'today': {},
    'previous': {}
  }

  for todoId in user_todos:
    todo = getTodo(todoId)
    localized = todo['dueDate']

    if current_date > localized.date():
      todos['upcoming'][todoId] = todo
    elif current_date < localized.date():
      todos['previous'][todoId] = todo
    else:
      todos['today'][todoId] = todo

  return todos

