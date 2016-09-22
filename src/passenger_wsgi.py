from flask import Flask
app = Flask(__name__)
import platform

@app.route('/')
def welcome():
    pyver = platform.python_version()
    return 'This is a sample application using the flask framework on Python %s' % pyver

application = app
