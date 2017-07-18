#!/usr/bin/env python2

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    # WARNING! Debug mode means the server will accept arbitrary Python code!
    app.run('0.0.0.0', 5000 , debug=True)
