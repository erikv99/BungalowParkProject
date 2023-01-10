from flask import render_template, session
from sqlalchemy import func, update
from __main__ import app, db

# Enum imports
from enums.messageType import MessageType
from enums.PermissionUser import PermissionUser as PU

# View model imports.
from models.viewModels.indexVM import IndexVM
from models.viewModels.loginVM import LoginVM
from models.viewModels.registerVM import RegisterVM
from models.viewModels.reserveVM import ReserveVM
from models.viewModels.adminVM import AdminVM
from models.viewModels.bungalowsVM import BungalowsVM
from models.viewModels.myReservationsVM import MyReservationVM
from models.viewModels.changeTypeVM import ChangeTypeVM
from models.viewModels.viewModelBase import ViewModelBase

# Database model imports.
from models.databaseModels.bungalow import Bungalow
from models.databaseModels.bungalowType import BungalowType
from models.databaseModels.reservation import Reservation


from models.dataTransferObjects.reservationBungalowDto import ReservationBungalowDto

# Form imports
from forms.reservationForm import ReservationForm
from forms.loginForm import LoginForm
from forms.registerForm import RegisterForm

from models.databaseModels.user import User
from helpers.authHelper import AuthHelper
from helpers.reservationHelper import ReservationHelper

# View names with their required level of permissions in order to view it
view_permissions = {
    "admin.html": PU.ADMIN,
    "bungalows.html": PU.EVERYONE,
    "changeType.html": PU.AUTHORIZED_USER,
    "error.html": PU.EVERYONE,
    "index.html": PU.EVERYONE,
    "layout.html": PU.EVERYONE,
    "login.html": PU.EVERYONE,
    "myReservations.html": PU.AUTHORIZED_USER,
    "noPermission.html": PU.EVERYONE,
    "register.html": PU.EVERYONE,
    "reserve.html": PU.AUTHORIZED_USER,
}

def _has_permission(model, template_name): 

    # Checking if the needed permission for the view (template) exists
    needed_permission = view_permissions.get(template_name, None)

    # If needed_permission not found for current template we assume its a new template and we didn't update the view_permissions list so we deny access.
    if needed_permission == None:
        return False

    # If permission applies to auth user or admin 
    if needed_permission == PU.AUTHORIZED_USER or needed_permission == PU.ADMIN:
        
        # If user is not logged in 
        if not model.is_logged_in:
            return False
        
        # If neede perm is admin and user is not admin
        if needed_permission == PU.ADMIN:
            if not model.is_admin:
                return False

    return True

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

    # If user has no permission for the view we 'redirect' to the no perm page
    # This should make sure that typing a route in the taskbar wont bring you to this actual page if you don't have permission
    if not _has_permission(model, template_name):
        return render_template("noPermission.html", model=model)

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

    # Getting all bungalows 
    bungalows = Bungalow.query.all()
    model.grouped_bungalows = ReservationHelper().GetGroupedBungalows(bungalows)
    return _render_template('bungalows.html', model=model)

@app.route("/reserve/<bungalow_id>", methods=["POST", "GET"])
def reserve(bungalow_id):

    bungalow = Bungalow.query.filter(Bungalow.id == bungalow_id).first()
    model = ReserveVM()
    form = ReservationForm()

    # If we didnt find the bungalow returning a message
    if bungalow == None:

        model = _add_message(model, MessageType.ERROR, "Error retrieving bungalow from the database with id: " + bungalow_id)
        return _render_template('reserve.html', model=model, form=form)
    
    bungalow_type = BungalowType.query.filter(BungalowType.id == bungalow.type_id).first()

    # If we didnt find the bungalow type returning a message
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

    # Getting the weeknumber for the reservation
    week_number = ReservationHelper().GetWeekNumber(date)

    # Checking if bungalow is not already reserved
    alreadyReserved = db.session.query(func.count(Reservation.id)) \
        .where(Reservation.bungalow_id == bungalow_id) \
        .where(Reservation.reserveration_week_number == week_number) \
        .first()[0] > 0

    # If already reserved rendering the view with a error message.
    if alreadyReserved:
        
        model.bungalow = Bungalow.query.where(Bungalow.id == bungalow_id).first()
        model = _add_message(model, MessageType.ERROR, "Bungalow is already reserved")
        return _render_template('reserve.html', model=model, form=form)

    # Trying to get the bungalow of the reservation, error message if not found
    bungalow = Bungalow.query.filter(Bungalow.id == bungalow_id).first()

    if bungalow == None:
        model = _add_message(model, MessageType.ERROR, "Error retrieving bungalow from the database with id: " + bungalow_id + "\nReservation failed.")
        return _render_template('reserve.html', model=model, form=form)
    
    # Trying to get bungalow type of reservation bungalow, error message if not found
    bungalow_type = BungalowType.query.filter(BungalowType.id == bungalow.type_id).first()

    if bungalow_type == None: 
        model = _add_message(model, MessageType.ERROR, "Error retrieving bungalow_type from the database for bungalow with id: " + bungalow_id + "\nReservation failed")
        return _render_template('reserve.html', model=model, form=form)

    # Creating a new Reservation object, then adding and commiting it to the db.
    reservation = Reservation(user_id=session["user_id"], bungalow_id=bungalow_id, reserveration_week_number=week_number)
    db.session.add(reservation)
    db.session.commit()

    _add_message(model, MessageType.SUCCESS, "Reservation succesfull")
    model.bungalow = bungalow
    model.bungalow_type = bungalow_type
    form.date.data = date
    form.bungalow_id.data = bungalow_id
    return _render_template('reserve.html', model=model, form=form)


@app.route("/my_reservations")
def my_reservations():

    # Loading all reservations for the logged in user from the database.
    reservations = Reservation.query.filter(Reservation.user_id == session["user_id"]).all()
    model = MyReservationVM()

    # If the user has no reservation we send a message informing them
    if len(reservations) == 0:

        model = _add_message(model, MessageType.INFO, "You have no reservations")
        return _render_template('myReservations.html', model=model)

    model.grouped_bungalows = ReservationHelper().GetGroupedReservations()
    return _render_template('myReservations.html', model=model)

@app.route("/my_reservations/cancel/<reservation_id>")
def cancel(reservation_id):

    # all we have to do is delete te reservation and return the my_reservation view basically.
    Reservation.query.filter(Reservation.id == reservation_id).delete()
    db.session.commit()
    return my_reservations()

@app.route("/my_reservations/extend/<reservation_id>/<direction_forward>", )
def extend(reservation_id, direction_forward):

    model = MyReservationVM()
    reservation = Reservation.query.where(Reservation.id == reservation_id).first()

    # Getting the default grouped bungelows, this means that the 'extended' reservation is not present yet.
    # Reason we get this now is that we can just return the view with the error message when required.
    model.grouped_bungalows = ReservationHelper().GetGroupedReservations()

    if reservation == None:

        model = _add_message(model, MessageType.ERROR, "Extending reservation failed, reservation number invalid")
        return _render_template('myReservations.html', model=model)

    required_week_number = None
    
    # Getting the week number of the week which would be the extension
    if direction_forward == 'True':

        required_week_number = reservation.reserveration_week_number + 1

        # From dec to januarie we switch from 52 to 1
        if (required_week_number > 52):
            required_week_number = 1

    else:
    
        required_week_number = reservation.reserveration_week_number - 1

        # From january to december we switch from 1 to 
        if (required_week_number <= 0):
            required_week_number = 52

    # Checking if the required week for the extend is actually available
    is_available = db.session.query(func.count(Reservation.id)) \
        .where(Reservation.bungalow_id == reservation.bungalow_id) \
        .where(Reservation.reserveration_week_number == required_week_number) \
        .first()[0] == 0

    # If the selected date and bungalow is not available we return with a message saying so
    if not is_available:

        model = _add_message(model, MessageType.ERROR, "Extending reservation failed, week " + str(required_week_number) + " is not free for selected bungalow")
        return _render_template('myReservations.html', model=model)

    # Creating a new Reservation object, then adding and commiting it to the db.
    reservation = Reservation(user_id=session["user_id"], bungalow_id=reservation.bungalow_id, reserveration_week_number=required_week_number)
    db.session.add(reservation)
    db.session.commit()
    model = _add_message(model, MessageType.SUCCESS, "Reservation extended")

    # Since we were succesfull in extending the reservation we have to reload all this in order to 
    # get accurate results (remember we just added a new entry in the db)       
    model.grouped_bungalows = ReservationHelper().GetGroupedReservations()

    return _render_template('myReservations.html', model=model)

@app.route("/my_reservations/change_type/<reservation_id>")
def change_type(reservation_id):

    model = ChangeTypeVM()
    reservation = Reservation.query.where(Reservation.id == reservation_id).first()
    
    # If we cant find a reservation with that id we just go back to the my reservation page with a fitting error message
    if reservation == None:

        model.grouped_bungalows = ReservationHelper().GetGroupedReservations()
        model = _add_message(model, MessageType.ERROR, "Failed loading template, reservation not found for id " + str(reservation_id))
        return _render_template('myReservations.html', model=model)

    model.bungalow = reservation.bungalow
    model.reservation = reservation

    # Getting all bungalows already reserved for the week in question
    reserved_bungalow_ids = [ entry[0] for entry in db.session.query(Reservation.bungalow_id).where(Reservation.reserveration_week_number == reservation.reserveration_week_number).all()]

    # Getting all available bungalows for the given week which are not reserved
    available_bungalows = Bungalow.query.where(Bungalow.id.not_in(reserved_bungalow_ids)).all()
    
    # Grouping the available bungalows in groups of 3 and ofc adding them to the model
    model.grouped_available_bungalows =  ReservationHelper().GetGroupedBungalows(available_bungalows)

    return _render_template("changeType.html", model)

@app.route("/my_reservations/change_type/confirm/<reservation_id>/<bungalow_id>")
def change_type_confirm(reservation_id, bungalow_id):

    # Updating the reservation and changing its bungalow id (bungalow type) which is attached to the reservation
    reservation = Reservation.query.where(Reservation.id == reservation_id).first()
    reservation.bungalow_id = bungalow_id
    db.session.commit()

    model = MyReservationVM()

    # Rendering the my reservations view with a message saying the reservation type changed
    model.grouped_bungalows = ReservationHelper().GetGroupedReservations()
    model = _add_message(model, MessageType.SUCCESS, "Reservation type changed")
    return _render_template('myReservations.html', model=model)

@app.route("/admin", methods=["POST", "GET"])
def admin():

    model = AdminVM()
    return _render_template('admin.html', model=model)

# Error routes

@app.route("/no_permission") 
def no_permission():
    return _render_template("noPermission.html")


@app.errorhandler(404)
def page_not_found(e):
    
    # note that we set the 404 status explicitly
    return _render_template('error.html')