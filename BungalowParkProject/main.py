from flask import Flask

# Creating the Flask app and putting it in a var.
app = Flask(__name__)

# Have to import these after creating the app
# since they need app to function.
import routes
import errorRoutes

def main():

    # Setting the secret key
    app.config["SECRET_KEY"] = "SECRETKEY"
    


    # Running the app.
    app.run(debug = True)

if __name__ == "__main__":
    main()