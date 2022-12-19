from flask import render_template, session, url_for
from models.viewModels.IndexVM import IndexVM
from models.viewModels.ViewModelBase import ViewModelBase
from __main__ import app

# Form inputs
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm

def _render_template(template_name, model = None, form = None):
    """
        Renders a template with a specific model (or None)
        contains logic to add the data which every model needs
    """

    # If no model is given we still need to give at least the base so the header knows if user is logged in or not.
    if model is None:
        model = ViewModelBase()

    # Checking if user is logged in and if user is an admin
    model.is_logged_in = session.get("is_logged_in") == True
    model.is_admin = session.get("is_admin") == True

    if form is not None:
        return render_template(template_name, model=model, form=form)
    else:
        return render_template(template_name, model=model)

@app.route("/")
def index():
    model = IndexVM()
    return _render_template('index.html', model=model)

@app.route("/login", methods=["POST", "GET"])
def login():

    form = LoginForm()
    model = IndexVM()
    return _render_template('login.html', model=model, form=form)

@app.route("/register", methods=["POST", "GET"])
def register():

    form = RegisterForm()
    model = IndexVM()
    return _render_template('register.html', model=model, form=form)

@app.route("/reservation", methods=["POST", "GET"])
def reservation():

    model = IndexVM()
    return _render_template('login.html', model=model)

@app.route("/admin", methods=["POST", "GET"])
def admin():

    model = IndexVM()
    return _render_template('adminFunctions.html', model=model)
