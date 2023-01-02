from app import db

class User(db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)    
    admin = db.Column(db.Boolean, nullable=False, default=0)

    def __repr__(self):

        repr = "User '{}' ({})".format(self.user_name, self.id)
        
        if (self.admin == True):
            repr += " (admin)"

        return repr 
