from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

# We want to be able to access these properties from the outside so we declare them here.
app = Flask(__name__)
db = SQLAlchemy(app)

# Have to import these after creating the app
# since they need app to function.
import Routes
import ErrorRoutes

def main():

    # Setting the secret key
    app.config["SECRET_KEY"] = "SECRETKEY"

    baseDir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Running the app.
    app.run(debug = True)

if __name__ == "__main__":
    main()