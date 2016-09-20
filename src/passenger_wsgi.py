from flask import Flask
app = Flask(__name__)

@app.route('/')
def welcome():
    return 'This is a sample application using the flask framework'

application = app
