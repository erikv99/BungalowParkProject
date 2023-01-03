from __main__ import db
from sqlalchemy.orm import relationship

class Bungalow(db.Model):
    
    __tablename__ = "bungalows"

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey("bungalowTypes.id"), nullable=False)
    unique_name = db.Column(db.String, nullable=False)
    img_file_name = db.Column(db.String, nullable=False)

    # omni directional relationship
    type = relationship("BungalowType", backref="bungalows")

    def __repr__(self):
        return "Bungalow\nid: {}\ntype_id: {}\nunique_name: {}\nimg_file_name: {}" \
            .format(self.id, self.type_id, self.unique_name, self.img_file_name)