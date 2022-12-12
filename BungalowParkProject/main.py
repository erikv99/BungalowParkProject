app = Flask(__name__)

def main():

    app.config["SECRET_KEY"] = "SECRETKEY"
    app.run(debug = True)

if __name__ == "__main__":
    main()