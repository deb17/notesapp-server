import datetime
import uuid

from app import app, db
from app.models import User

import jwt
from google.oauth2 import id_token
from google.auth.transport import requests


def get_token(public_id):

    token_bytes = jwt.encode({
        'public_id': public_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return token_bytes.decode()


def google_signin(google_token):

    try:
        idinfo = id_token.verify_oauth2_token(
            google_token, requests.Request(), app.config['CLIENT_ID'])

        if idinfo['iss'] not in ['accounts.google.com',
                                 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        userid = idinfo['sub']
        gmail = idinfo['email']
    except ValueError as e:
        return {'msg': e.args[0]}
    else:
        user = User.query.filter_by(guserid=userid).first()
        if user:
            return {'token': get_token(user.public_id)}
        else:
            user = User.query.filter_by(email=gmail).first()
            if user:
                user.guserid = userid
                user.gmail = gmail
                db.session.commit()
                return {'token': get_token(user.public_id)}
            else:
                new_user = User(guserid=userid, gmail=gmail,
                                public_id=str(uuid.uuid4()))
                db.session.add(new_user)
                db.session.commit()
                return {'token': get_token(new_user.public_id)}
