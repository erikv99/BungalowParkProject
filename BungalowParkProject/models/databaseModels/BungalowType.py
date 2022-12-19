from __main__ import db

class BungalowType(db.Model):
    
    __tablename__ = "bungalowtypes"

    id = db.Column(db.Integer, primary_key=True)
    week_price = db.Column(db.Float, nullable=False)
    size = db.Column(db.Integer, nullable=False)

    # TODO
    def __repr__(self):
        return ""
