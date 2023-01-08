from enums.messageType import MessageType
from models.viewModels.loginVM import LoginVM
import bcrypt
from flask import session
from app import db
from models.databaseModels.user import User

class AuthHelper():

    def Logout(self):

        session["is_logged_in"] = False
        session["is_admin"] = False
        session["user_id"] = -1

    def Login(self, username, password):

        model = LoginVM()

        # Checking if pass hash matches the one in the db.
        if self._pass_matches(username, password):

            session["is_logged_in"] = True
            session["user_id"] = self._get_user_id(username)
            
            # Checking if user is admin
            if self._is_admin(username):

                session["is_admin"] = True
                model.message_content = "Admin login succesfull"

            else:

                model.message_content = "Login succesfull"

            model.message_type = MessageType.SUCCESS
            
        else:

            model.message_type = MessageType.ERROR
            model.message_content = "Password or username incorrect"
        
        return model

    def Register(self, username, password):
        """
            Registers a user in the database.
        """

        # Getting the hashed password
        hashed_password = self._get_hashed_password(password)

        #Creating a new user object, then adding and commiting it to the db.
        user = User(username=username, password=hashed_password, admin=False)
        db.session.add(user)
        db.session.commit()

    def _get_user_id(self, username):

        user = User.query.where(User.username == username).first()
        return user.id

    def _pass_matches(self, username, password):
        """
            Compares the given username and password against 
            the password for the given username in the database.
        """

        # Getting the first user with the given username
        user = User.query.where(User.username == username).first()

        # output is false if user is none
        if user is None:
            return False

        # returning the outcome of the password check. We check the given text password against
        # the stored hashed pw using a bcrypt function.
        return bcrypt.hashpw(password.encode('utf-8'), user.password)

    def _get_hashed_password(self, password):
        """
            Returns the hashed version of the given password
        """

        # Creating a salt for the hashing.
        salt = bcrypt.gensalt()

        # Hasing the password and returning it
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def _is_admin(self, username):
        """
            Checks and returns wheter or not the user is an admin
        """

        # Getting the first user with the given username
        user = User.query.filter_by(username=username).first()

        # output is false if user is none
        if user is None:
            return False

        # output is the outcome of if the user.admin == true
        return user.admin == True
