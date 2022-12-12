from flask import render_template
from viewModels.IndexVM import IndexVM

from __main__ import app

@app.route('/')
def index():

    model = IndexVM()
    model.isLoggedIn = True
    model.isAdmin = True

    return render_template('index.html', model=model)
