from flask import Flask
import os

# Creating the Flask app and putting it in a var.
app = Flask(__name__)

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