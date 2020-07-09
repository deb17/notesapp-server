from app import app, db
from app.models import Note
from functools import wraps
from flask import request, g
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy import and_


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('X-id-token')
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), app.config['CLIENT_ID'])

            if idinfo['iss'] not in ['accounts.google.com',
                                     'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            g.userid = idinfo['sub']
            return func(*args, **kwargs)

        except ValueError as e:
            return {'msg': e.args[0]}

    return wrapper


@app.route('/api/notes')
@token_required
def all_notes():

    notes = Note.query.filter_by(userid=g.userid).all()

    result = []

    for note in notes:
        obj = {
            'id': note.id,
            'title': note.title,
            'folder': note.folder
        }
        result.append(obj)

    return {'notes': result}


@app.route('/api/note/<int:id>')
@token_required
def get_note(id):

    note = Note.query.filter_by(id=id).first()

    if note is None:
        return {'error': '404 Not found'}

    if note.userid != g.userid:
        return {'error': '403 Access forbidden'}

    obj = {
        'id': note.id,
        'title': note.title,
        'folder': note.folder,
        'contents': note.contents,
        'status': note.status,
        'ts': note.ts
    }

    return obj


@app.route('/api/save', methods=['POST', 'PUT'])
@token_required
def save_note():

    note = request.get_json()

    note['userid'] = g.userid

    if note['id'] == 0:
        del note['id']
        n = Note(**note)
        db.session.add(n)
        db.session.commit()
    else:
        n = Note.query.filter_by(id=note['id']).first()
        n.title = note['title']
        n.folder = note['folder']
        n.contents = note['contents']
        n.status = note['status']
        n.ts = note['ts']
        db.session.commit()

    return {}


@app.route('/api/delete/<int:id>', methods=['DELETE'])
@token_required
def delnote(id):

    n = Note.query.get(id)
    db.session.delete(n)
    db.session.commit()

    return {'msg': 'Note deleted.'}


@app.route('/api/delete', methods=['DELETE'])
@token_required
def delfolder():

    data = request.get_json()

    rows = Note.query.filter(and_(Note.folder.startswith(
        data['folder']), Note.userid == g.userid)).all()

    for row in rows:
        db.session.delete(row)

    db.session.commit()

    return {'msg': 'Folder deleted.'}
