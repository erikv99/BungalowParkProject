from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# We want to be able to access these properties from the outside so we declare them here.
app = Flask(__name__)

baseDir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Have to import these after creating the app
# since they need app to function.
import routes

def main():

    print("Main executed...")

    # Setting the secret key
    app.config["SECRET_KEY"] = "SECRETKEY"
    app.config["SESSION_COOKIE_SECURE"] = False

    # We need to import these here so when creating the db
    # the db knows how to find them.
    from models.databaseModels.bungalow import Bungalow
    from models.databaseModels.bungalowType import BungalowType
    from models.databaseModels.user import User
    from models.databaseModels.reservation import Reservation
    db.create_all()

    # Populating the db if needed
    from helpers.populateHelper import PopulateHelper
    PopulateHelper().Populate()

    # Running the app.
    app.run(debug = True, use_reloader=False)

if __name__ == "__main__":
    main()
else:
    print("App was unable to launch since __name__ != __main__")

    