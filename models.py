from app import db
from sqlalchemy.dialects.postgresql import JSON


class Photo(db.Model):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    data = db.Column(JSON)
    predictions = db.relationship(
        "Prediction", backref="photo_predictions", lazy=True, passive_deletes=True
    )

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "data": self.data,
        }


class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    data = db.Column(JSON)
    predictions = db.relationship(
        "Prediction", backref="match_predictions", lazy=True, passive_deletes=True
    )

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "data": self.data,
        }


class Prediction(db.Model):
    __tablename__ = "predictions"
    __table_args__ = (
        # this can be db.PrimaryKeyConstraint if you want it to be a primary key
        db.UniqueConstraint("photo", "match"),
    )

    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(
        db.Integer, db.ForeignKey("photos.id", ondelete="CASCADE"), nullable=False
    )
    match = db.Column(
        db.Integer, db.ForeignKey("matches.id", ondelete="CASCADE"), nullable=False
    )
    status = db.Column(db.Boolean, default=False)
    score = db.Column(db.Numeric(10, 10))

    def __init__(self, photo, match, status, score):
        self.photo = photo
        self.match = match
        self.status = status
        self.score = score

    def __repr__(self):
        return "<id {}>".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "photo": self.photo,
            "match": self.match,
            "status": self.status,
            "score": self.score,
        }
