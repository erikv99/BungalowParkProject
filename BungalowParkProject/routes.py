from flask import render_template, session
from sqlalchemy import func
from __main__ import app, db

# Enum imports
from enums.messageType import MessageType
from enums.PermissionUser import PermissionUser as PU

# View model imports.
from models.viewModels.reserveVM import ReserveVM
from models.viewModels.bungalowsVM import BungalowsVM
from models.viewModels.myReservationsVM import MyReservationVM
from models.viewModels.changeTypeVM import ChangeTypeVM
from models.viewModels.errorVM import ErrorVM
from models.viewModels.changeWeekVM import ChangeWeekVM
from models.viewModels.baseVM import BaseVM

# Database model imports.
from models.databaseModels.bungalow import Bungalow
from models.databaseModels.bungalowType import BungalowType
from models.databaseModels.reservation import Reservation

# Form imports
from forms.reservationForm import ReservationForm
from forms.loginForm import LoginForm
from forms.registerForm import RegisterForm
from forms.changeWeekForm import ChangeWeekForm

from models.databaseModels.user import User
from helpers.authHelper import AuthHelper
from helpers.reservationHelper import ReservationHelper

# View names with their required level of permissions in order to view it
view_permissions = {
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
    "changeWeek.html": PU.AUTHORIZED_USER
}

def _has_permission(model, template_name): 
    """
        Checks if the current user has permission to view the template.
        Returns a bool
    """

    # Checking if the needed permission for the view (template) exists
    needed_permission = view_permissions.get(template_name, None)

    # If needed_permission not found for current template we assume its a new template and we didn't update the view_permissions list so we deny access.
    if needed_permission == None:
        return False

    # If permission applies to auth user 
    if needed_permission == PU.AUTHORIZED_USER:
        
        # If user is not logged in 
        if not model.is_logged_in:
            return False

    return True

def _render_template(template_name, model = None, form = None):
    """
        Renders a template with a specific model (or None)
        contains logic to add the data which every model needs
    """

    # If no model is given we still need to give at least the base (ViewModelBase) so the template knows if user is logged in or not.
    if model is None:
        model = BaseVM()

    # Getting data for currently logged in (or not) user
    model.is_logged_in = session.get("is_logged_in")
    model.user_id = session.get("user_id")

    # If user has no permission for the view we 'redirect' to the no perm page
    # This should make sure that typing a route in the taskbar wont bring you to this actual page if you don't have permission
    if not _has_permission(model, template_name):
        return render_template("noPermission.html", model=model)

    # Rendering template 
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
    return _render_template('index.html')

@app.route("/logout", methods=["POST", "GET"])
def logout():

    form = LoginForm()
    model = BaseVM()
    
    try:

        AuthHelper().Logout()
        model = _add_message(model, MessageType.SUCCESS, "You are now logged out")

    except:
        model = _add_message(model, MessageType.ERROR, "Error while trying to log out")

    return _render_template('login.html', model=model, form=form)

@app.route("/login", methods=["POST", "GET"])
def login():

    form = LoginForm()
    model = BaseVM()
    return _render_template('login.html', model=model, form=form)
    

@app.route("/login/submit", methods=["POST", "GET"])
def login_submit():

    form = LoginForm()
    model = BaseVM()

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
    model = BaseVM()
    return _render_template('register.html', model=model, form=form)

@app.route("/login/register_submit", methods=["POST", "GET"])
def register_submit():

    form = RegisterForm()
    model = BaseVM()

    # If the form is valid we get the given data and attempt to register the user.
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

@app.route("/reserve/<bungalow_id>")
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

# USED INTERNAL ONLY
def _redirect_to_my_reservations_with_message(message_type, message):

    # Loading all reservations for the logged in user from the database.
    reservations = Reservation.query.filter(Reservation.user_id == session["user_id"]).all()
    model = MyReservationVM()

    model = _add_message(model, message_type, message)

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

@app.route("/my_reservations/extend/<reservation_id>/<direction_forward>")
def extend(reservation_id, direction_forward):
    """
        Extend a reservation
        arg reservation_id: reservation id of reservation to extend
        arg direction_forward: boolean which determines wheter or not it should be extended forward (next week)
            or backwards (week before)

        Reason this route is commented and others are not is since I realize direction_forward is a sloppy and unclean way
        to do this.
    """

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
        return _redirect_to_my_reservations_with_message(MessageType.ERROR, "Failed loading template, reservation not found for id " + str(reservation_id))

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

    return _redirect_to_my_reservations_with_message(MessageType.SUCCESS, "Reservation type changed")

@app.route("/my_reservations/change_week/<reservation_id>") 
def change_week(reservation_id):

    model = ChangeWeekVM()
    form = ChangeWeekForm()
    reservation_id_is_valid = reservation_id != None or reservation_id != ""

    if not reservation_id_is_valid:
        return _redirect_to_my_reservations_with_message(MessageType.ERROR, "Given reservation id for change_week not valid")

    reservation = Reservation.query.where(Reservation.id == reservation_id).first()

    if reservation == None:
        return _redirect_to_my_reservations_with_message(MessageType.ERROR, "Reservation not found in database")

    form.reservation_id.data = reservation_id
    model.reservation = reservation
    return _render_template("changeWeek.html", model=model, form=form)

@app.route("/my_reservations/change_week/confirm", methods=["POST", "GET"])
def change_week_submit():

    model = ChangeWeekVM()
    form = ChangeWeekForm()
    reservation_id = form.data.get("reservation_id")
    date = form.data.get("date")
    reservation_id_is_valid = reservation_id != None or reservation_id != ""
    date_is_valid = date != None or date != ""

    # if valid reservation_id or date was given we want to make sure those are still filled in.
    if reservation_id_is_valid:
        form.reservation_id.data = reservation_id

    if (date_is_valid):
        form.date.data = date

    # If form invalid, date invalid or reservation invalid returning a view with a error message.
    if not form.validate_on_submit() or not reservation_id_is_valid or not date_is_valid:

        model = _add_message(model, MessageType.ERROR, "Error changing week number for reservation")        
        return _render_template('changeWeek.html', model=model, form=form)

    # Getting the weeknumber for the reservation
    week_number = ReservationHelper().GetWeekNumber(date)
    reservation = Reservation.query.where(Reservation.id == reservation_id).first()

    if (reservation == None):

        model = _add_message(model, MessageType.ERROR, "Reservation not found in database")
        return _render_template('changeWeek.html', model=model, form=form)

    # Checking if bungalow is not already reserved on that week.
    alreadyReserved = db.session.query(func.count(Reservation.id)) \
        .where(Reservation.bungalow_id == reservation.bungalow_id) \
        .where(Reservation.reserveration_week_number == week_number) \
        .first()[0] > 0

    # If already reserved rendering the view with a error message.
    if alreadyReserved:

        model.reservation = reservation
        model = _add_message(model, MessageType.ERROR, "Selected week is already reserved by someone else.")
        return _render_template('changeWeek.html', model=model, form=form)

    # Updating week number for reservation and commiting it to the db
    reservation.reserveration_week_number = week_number
    db.session.commit()

    return _redirect_to_my_reservations_with_message(MessageType.SUCCESS, "Reservation week changed succesfully")

# Error routes
@app.route("/no_permission") 
def no_permission():
    return _render_template("noPermission.html")

@app.errorhandler(404)
def page_not_found(e):
    
    model = ErrorVM()
    model.message = "Page could not be found"
    model.error_code = 404
    return _render_template('error.html', model=model)