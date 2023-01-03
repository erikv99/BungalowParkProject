from __main__ import db

class BungalowType(db.Model):
    
    __tablename__ = "bungalowTypes"

    id = db.Column(db.Integer, primary_key=True)
    week_price = db.Column(db.Float, nullable=False)
    size = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Bungalow type\nid: {}\nweek_price: {}\nsize: {}" \
            .format(self.id, self.week_price, self.week_price)
