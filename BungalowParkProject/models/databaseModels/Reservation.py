from __main__ import db
from sqlalchemy.orm import relationship

class Reservation(db.Model):

    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    bungalow_id = db.Column(db.Integer, db.ForeignKey("bungalow.id"), nullable=False)
    reserveration_week_number = db.Column(db.Integer, nullable=False)

    # omni directional relations.
    user = relationship("User", backref="reservations")
    bungalow = relationship("Bungalow", backref="reservations")

    # TODO
    def __repr__(self):
        return ""