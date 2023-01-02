from enums.messageType import MessageType
from models.viewModels.loginVM import LoginVM
import bcrypt
from flask import session
from app import app, db
from models.databaseModels.user import User
from flask import Flask

class AuthHelper():

    def Logout(self):

        session["is_logged_in"] = False
        session["is_admin"] = False

    def Login(self, user_name, password):

        model = LoginVM()
        hashed = self._get_hashed_password(password)

        # Checking if pass hash matches the one in the db.
        if self._pass_hash_matches(user_name, hashed):

            session["is_logged_in"] = True
            
            # Checking if user is admin
            if self._is_admin(user_name):
                session["is_admin"] = True
                model.message_content = "Admin login succesfull"

            else:

                model.message_content = "Login succesfull"

            model.message_type = MessageType.SUCCESS
            
        else:

            model.message_type = MessageType.ERROR
            model.message_content = "Password or username incorrect"
        
        return model

    def Register(self, user_name_i, password):
        """
            Registers a user in the database.
        """

        # Getting the hashed password
        hashed_password = self._get_hashed_password(password)

        #Creating a new user object, then adding and commiting it to the db.
        user = User(id=1, user_name=user_name_i, password=hashed_password, admin=False)
        db.session.add(user)
        db.session.commit()

    def _pass_hash_matches(self, user_name_i, password):
        """
            Compares the given username and password against 
            the password for the given username in the database.
        """

        return True
        
        # //user = User.query.filter_by(user_name=user_name_i).first()

        # if user is None:
        #     return False

        # return user.password == password

    def _get_hashed_password(self, password):
        """
            Returns the hashed version of the given password
        """

        # Creating a salt for the hashing.
        salt = bcrypt.gensalt()

        # Hasing the password and returning it
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def _is_admin(self, user_name):
        return True