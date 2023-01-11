from enums.messageType import MessageType
from models.viewModels.baseVM import BaseVM
import bcrypt
from flask import session
from app import db
from models.databaseModels.user import User

class AuthHelper():

    def Logout(self):

        session["is_logged_in"] = False
        session["user_id"] = -1

    def Login(self, username, password):

        model = BaseVM()

        # Checking if pass hash matches the one in the db.
        if self._pass_matches(username, password):

            session["is_logged_in"] = True
            session["user_id"] = self._get_user_id(username)
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
        user = User(username=username, password=hashed_password)
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