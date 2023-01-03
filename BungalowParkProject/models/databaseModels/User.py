from __main__ import db

class User(db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)    
    admin = db.Column(db.Boolean, nullable=False, default=0)

    def __repr__(self):

        repr = "User '{}' ({})".format(self.username, self.id)
        
        if (self.admin == True):
            repr += " (admin)"

        return repr 
