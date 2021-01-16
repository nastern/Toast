from firebase_admin import credentials
import pyrebase
import firebase_admin
from firebase_admin import firestore

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
      userId: the userId of the new user to be stored in the session variable.
  '''


  pyrebase_auth = pyrebase.auth()
  user = pyrebase_auth.create_user_with_email_and_password(email, password)
  user = pyrebase_auth.refresh(user['refreshToken'])

  userId = user['userId']

  db = firestore.client()
  doc_ref = db.collection('users').document(userId)

  doc_ref.set({
    'userId': userId,
    'todos': [],
    'email': email,
    'name': name
  })

  return userId

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
  db.collection('users').document(userId).update({
    'todos': firestore.ArrayUnion([new_todo])
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

def getTodosForUser(userId):
  '''
    args:
      userId: the userId to get the data for
    returns:
      todos: all of the todos associated with a specific user
  '''
  user = getUser(userId)
  todos = user['todos']

  return todos

