import uuid

from flask import request
from app import db
from app.models import User
from . import auth
from .helpers import google_signin, get_token
from .email import send_password_reset_email


@auth.route('/api/signup', methods=['POST'])
def signup():

    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user:
        return {'msg': 'That email is already taken.'}
    else:
        user = User.query.filter_by(gmail=data['email']).first()
        if user:
            user.email = data['email']
            user.set_password(data['password'])
            db.session.commit()
            return {'token': get_token(user.public_id)}
        else:
            new_user = User(
                email=data['email'],
                public_id=str(uuid.uuid4())
            )
            new_user.set_password(data['password'])
            db.session.add(new_user)
            db.session.commit()
            return {'token': get_token(new_user.public_id)}


@auth.route('/api/signin', methods=['POST'])
def signin():

    data = request.get_json()
    google_token = data.get('idToken')

    if google_token:
        return google_signin(google_token)
    else:
        user = User.query.filter_by(email=data['email']).first()
        if user:
            if user.check_password(data['password']):
                return {'token': get_token(user.public_id)}
            else:
                return {'msg': 'Invalid email or password'}
        else:
            return {'msg': 'Invalid email or password'}


@auth.route('/api/reset_password_request', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        send_password_reset_email(user)
    return {}


@auth.route('/api/reset_password/<token>', methods=['POST'])
def reset_password(token):
    user = User.verify_reset_password_token(token)
    if not user:
        return {'error': 'Password reset failed.'}
    data = request.get_json()
    user.set_password(data['password'])
    db.session.commit()
    return {'msg': 'Your password has been reset.'}
