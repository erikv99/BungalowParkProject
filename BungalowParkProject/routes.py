from flask import render_template, session
from sqlalchemy import func
from __main__ import app, db
from enums.messageType import MessageType

# View model imports.
from models.viewModels.indexVM import IndexVM
from models.viewModels.loginVM import LoginVM
from models.viewModels.registerVM import RegisterVM
from models.viewModels.reserveVM import ReserveVM
from models.viewModels.adminVM import AdminVM
from models.viewModels.bungalowsVM import BungalowsVM
from models.viewModels.viewModelBase import ViewModelBase

# Database model imports.
from models.databaseModels.bungalow import Bungalow
from models.databaseModels.bungalowType import BungalowType
from models.databaseModels.reservation import Reservation

# Form imports
from forms.reservationForm import ReservationForm
from forms.loginForm import LoginForm
from forms.registerForm import RegisterForm

from models.databaseModels.user import User
from helpers.authHelper import AuthHelper
from helpers.reservationHelper import ReservationHelper


def _render_template(template_name, model = None, form = None):
    """
        Renders a template with a specific model (or None)
        contains logic to add the data which every model needs
    """

    # If no model is given we still need to give at least the base so the header knows if user is logged in or not.
    if model is None:
        model = ViewModelBase()

    # Checking if user is logged in and if user is an admin
    model.is_logged_in = session.get("is_logged_in")
    model.is_admin = session.get("is_admin")
    model.user_id = session.get("user_id")

    if form is not None:
        return render_template(template_name, model=model, form=form)
    else:
        return render_template(template_name, model=model)

def _add_message(model, message_type, error_message):
    """
        Adds message a of the given type to the given model and returns it.
        Meant to bring down the clutteryness in the file.
    """

    model.message_type = message_type
    model.message_content = error_message
    return model

@app.route("/home")
@app.route("/")
def index():

    model = IndexVM()
    return _render_template('index.html', model=model)

@app.route("/logout", methods=["POST", "GET"])
def logout():

    form = LoginForm()
    model = LoginVM()
    
    try:
        AuthHelper().Logout()
        model = _add_message(model, MessageType.SUCCESS, "You are now logged out")
    except:
        model = _add_message(model, MessageType.ERROR, "Error while trying to log out")

    return _render_template('login.html', model=model, form=form)

@app.route("/login", methods=["POST", "GET"])
def login():

    form = LoginForm()
    model = LoginVM()
    return _render_template('login.html', model=model, form=form)
    

@app.route("/login/submit", methods=["POST", "GET"])
def login_submit():

    form = LoginForm()
    model = LoginVM()

    if form.validate_on_submit(): 

        username = form.data.get("user_name")
        password = form.data.get("password")
        model = AuthHelper().Login(username, password)
    else:

        model = _add_message(model, MessageType.ERROR, "Error submitting form")

    return _render_template('login.html', model=model, form=form)

@app.route("/register", methods=["POST", "GET"])
def register():

    form = RegisterForm()
    model = RegisterVM()
    return _render_template('register.html', model=model, form=form)

@app.route("/login/register_submit", methods=["POST", "GET"])
def register_submit():

    form = RegisterForm()
    model = RegisterVM()

    if form.validate_on_submit():

        username = form.data.get("user_name")
        password = form.data.get("password")
        confirm_password = form.data.get("confirm_password")

        if (password == confirm_password):
            
            AuthHelper().Register(username, password)
            model = _add_message(model, MessageType.SUCCESS, "Registration completed")

        else:
             model = _add_message(model, MessageType.ERROR, "Passwords do not match")
    else:
        model = _add_message(model, MessageType.ERROR, "Error registering user")

    return _render_template('register.html', model=model, form=form)

@app.route("/bungalows")
def bungalows():
    model = BungalowsVM()
    model.grouped_bungalows = ReservationHelper().GetGroupedBungalows()
    return _render_template('bungalows.html', model=model)

@app.route("/reserve/<bungalow_id>", methods=["POST", "GET"])
def reserve(bungalow_id):

    bungalow = Bungalow.query.filter(Bungalow.id == bungalow_id).first()
    model = ReserveVM()
    form = ReservationForm()

    if bungalow == None:

        model = _add_message(model, MessageType.ERROR, "Error retrieving bungalow from the database with id: " + bungalow_id)
        return _render_template('reserve.html', model=model, form=form)
    
    bungalow_type = BungalowType.query.filter(BungalowType.id == bungalow.type_id).first()

    if bungalow_type == None: 

        model = _add_message(model, MessageType.ERROR, "Error retrieving bungalow_type from the database for bungalow with id: " + bungalow_id)
        return _render_template('reserve.html', model=model, form=form)

    form.bungalow_id.data = bungalow_id
    model.bungalow = bungalow
    model.bungalow_type = bungalow_type
    return _render_template('reserve.html', model=model, form=form)

@app.route("/reserve/commit", methods=["POST", "GET"])
def reserve_submit():

    model = ReserveVM()
    form = ReservationForm()
    bungalow_id = form.data.get("bungalow_id")
    date = form.data.get("date")

    # If form invalid returning a view with a error message.
    if not form.validate_on_submit():

        model = _add_message(model, MessageType.ERROR, "Error making reservation")

        # if valid bungalow_id or date was given we want to make sure those are still filled in.
        if (bungalow_id != None or bungalow_id != ""):
            form.bungalow_id.data = bungalow_id

        if (date != None or date != ""):
            form.date.data = date
        
        return _render_template('reserve.html', model=model, form=form)

    # If form valid but bungalow_id or date is not.
    if (bungalow_id == None or date == None or bungalow_id == "" or date == ""):

        model = _add_message(model, MessageType.ERROR, "Error making reservation")
        return _render_template('reserve.html', model=model, form=form)

    ##week_number = ReservationHelper().GetWeekNumber()'
    week_number = 1

    # Checking if bungalow is not already reserved
    alreadyReserved = db.session.query(func.count(Reservation.id)) \
        .where(Reservation.bungalow_id == bungalow_id and Reservation.reserveration_week_number == week_number) \
        .first()[0] > 0

    if alreadyReserved:

        model = _add_message(model, MessageType.ERROR, "Bungalow is already reserved")
        return _render_template('reserve.html', model=model, form=form)

    bungalow = Bungalow.query.filter(Bungalow.id == bungalow_id).first()

    if bungalow == None:

        model = _add_message(model, MessageType.ERROR, "Error retrieving bungalow from the database with id: " + bungalow_id + "\nReservation failed.")
        return _render_template('reserve.html', model=model, form=form)
    
    bungalow_type = BungalowType.query.filter(BungalowType.id == bungalow.type_id).first()

    if bungalow_type == None: 

        model = _add_message(model, MessageType.ERROR, "Error retrieving bungalow_type from the database for bungalow with id: " + bungalow_id + "\nReservation failed")
        return _render_template('reserve.html', model=model, form=form)

    #Creating a new Reservation object, then adding and commiting it to the db.
    reservation = Reservation(user_id=username, bungalow_id=hashed_password, reserveration_week_number=False)
    db.session.add(reservation)
    db.session.commit()

    model.message_type = MessageType.SUCCESS
    model.message_content = "Reservation succesfull"
    _add_message(model, MessageType.ERROR, "Error making reservation")
    model.bungalow = bungalow
    model.bungalow_type = bungalow_type
    form.date.data = date
    form.bungalow_id.data = bungalow_id
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

