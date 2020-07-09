from app import db


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(50), index=True)
    title = db.Column(db.String(100))
    folder = db.Column(db.String(100), index=True)
    contents = db.Column(db.Text)
    status = db.Column(db.String(10))
    ts = db.Column(db.BigInteger)

    def __repr__(self):
        return '<Note: {}>'.format(self.title)
