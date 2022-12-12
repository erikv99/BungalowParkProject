from flask import render_template, session
from viewModels.IndexVM import IndexVM

from __main__ import app

@app.route("/")
def index():


    model = IndexVM()
    return render_template('index.html', model=model)

@app.route("/login", methods=["POST", "GET"])
def index():

    model = IndexVM()
    return render_template('login.html', model=model)

@app.route("/register", methods=["POST", "GET"])
def index():

    model = IndexVM()
    return render_template('register.html', model=model)

@app.route("/reservation", methods=["POST", "GET"])
def index():

    model = IndexVM()
    return render_template('login.html', model=model)
