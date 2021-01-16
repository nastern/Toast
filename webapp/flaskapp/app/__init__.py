from flask import Flask

app = Flask(__name__)
app.secret_key = 'THIS 8mBEvwrng4P!c8nUsyVgJY-jL2mNX6iTIS SUPER SEC!!!8mBEvwrng4P!c8nUsyVgJY-jL2mNX6iTuHmywK!6RHNHkpUfuxCGwW.TYxxo_Yfx'

from app import routes
