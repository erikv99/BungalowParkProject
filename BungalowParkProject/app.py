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

# Need to make sure tables get created before the first request.
# Otherwise the db stuff wont work properly.
@app.before_first_request
def create_tables():
    
    db.create_all()
    

def main():

    print("Main executed")

    # Setting the secret key
    app.config["SECRET_KEY"] = "SECRETKEY"
    app.config["SESSION_COOKIE_SECURE"] = False

    # Running the app.
    app.run(debug = True, use_reloader=False)

if __name__ == "__main__":
    main()

else:
    print("App was unable to launch since __name__ != __main__")

    