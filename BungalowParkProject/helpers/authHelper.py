from enums.messageType import MessageType
from models.viewModels.loginVM import LoginVM
import bcrypt
from flask import session

class AuthHelper():

    def Logout():

        session["is_logged_in"] = False
        session["is_admin"] = False

    def Login(self, user_name, password):

        model = LoginVM()

        # Creating a salt for the hashing.
        salt = bcrypt.gensalt()

        # Hasing the password
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

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

    def _pass_hash_matches(self, user_name, pass_hash):
        return True

    def _is_admin(self, user_name):
        return True