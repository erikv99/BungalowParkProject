from __main__ import db
from sqlalchemy.orm import relationship

class Bungalow(db.Model):
    
    __tablename__ = "bungalows"

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey("bungalowType.id"), nullable=False)
    unique_name = db.Column(db.String, nullable=False)

    # omni directional relationship
    type = relationship("BungalowType", backref="bungalows")

    # TODO
    def __repr__(self):
        return ""