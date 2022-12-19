from flask import render_template, session, url_for
from __main__ import app

# View model imports.
from models.viewModels.indexVM import IndexVM
from models.viewModels.loginVM import LoginVM
from models.viewModels.registerVM import RegisterVM
from models.viewModels.reserveVM import ReserveVM
from models.viewModels.adminVM import AdminVM
from models.viewModels.viewModelBase import ViewModelBase

# Form imports
from forms.reservationForm import ReservationForm
from forms.loginForm import LoginForm
from forms.registerForm import RegisterForm

from models.databaseModels.user import User

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

    x = User.query.all()
    y = 4
    model = IndexVM()
    return _render_template('index.html', model=model)

@app.route("/login", methods=["POST", "GET"])
def login():

    form = LoginForm()
    model = LoginVM()
    return _render_template('login.html', model=model, form=form)

@app.route("/register", methods=["POST", "GET"])
def register():

    form = RegisterForm()
    model = RegisterVM()
    return _render_template('register.html', model=model, form=form)

@app.route("/reserve", methods=["POST", "GET"])
def reserve():

    form = ReservationForm()
    model = ReserveVM()
    return _render_template('reserve.html', model=model, form=form)

@app.route("/admin", methods=["POST", "GET"])
def admin():

    model = AdminVM()
    return _render_template('admin.html', model=model)

# Error routes

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return _render_template('error.html')

