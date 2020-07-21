from time import time
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), index=True, unique=True)
    guserid = db.Column(db.String(50), index=True, unique=True)
    gmail = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User: {}>'.format(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.public_id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            public_id = jwt.decode(token, app.config['SECRET_KEY'],
                                   algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return User.query.filter_by(public_id=public_id).first()


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, index=True)
    title = db.Column(db.String(100))
    folder = db.Column(db.String(100), index=True)
    contents = db.Column(db.Text)
    status = db.Column(db.String(10))
    ts = db.Column(db.BigInteger)

    def __repr__(self):
        return '<Note: {}>'.format(self.title)
