import pyrebase

config = {
  "apiKey": "API_KEY_HERE",
  "authDomain": "AUTH_DOMAIN",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "STORAGE_BUCKET",
  "serviceAccount": "./app/config/serviceAccount.json"
}

# firebase = pyrebase.initialize_app(config)

# def createUser(email, password):
  # auth = firebase.auth()
  # auth.create_user_with_email_and_password(email, password)
  # return True
