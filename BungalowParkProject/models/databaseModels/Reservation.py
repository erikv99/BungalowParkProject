from __main__ import db
from sqlalchemy.orm import relationship

class Reservation(db.Model):

    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bungalow_id = db.Column(db.Integer, db.ForeignKey("bungalows.id"), nullable=False)
    reserveration_week_number = db.Column(db.Integer, nullable=False)

    # omni directional relations.
    user = relationship("User", backref="reservations")
    bungalow = relationship("Bungalow", backref="reservations")

    def __repr__(self):
        return "Reservation\nid: {}\nuser_id: {}\nbungalow_id: {}\nreservation_week_number: {}" \
            .format(self.id, self.user_id, self.bungalow_id, self.reserveration_week_number)