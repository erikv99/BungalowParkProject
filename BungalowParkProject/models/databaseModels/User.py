from __main__ import db

class User(db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)    

    def __repr__(self):
        return "User '{}' ({})".format(self.username, self.id)