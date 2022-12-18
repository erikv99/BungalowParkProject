from __main__ import db

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False) # TODO MAKE FOREIGN
    bungalow_id = db.Column(db.Integer, nullable=False) # TODO MAKE FOREIGN
    reserveration_week_number = db.Column(db.Integer, nullable=False) # TODO MAKE FOREIGN
