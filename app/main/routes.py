from app import app, db
from . import main
from app.models import User, Note
from functools import wraps
from flask import request, g
from sqlalchemy import and_
import jwt


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('X-access-token')
        if token:
            try:
                payload = jwt.decode(
                    token, app.config['SECRET_KEY'], algorithms=['HS256'])
            except Exception:
                return {'error': 'Invalid token'}
            else:
                user = User.query.filter_by(
                    public_id=payload['public_id']).first()
                g.userid = user.id
                return func(*args, **kwargs)
        else:
            return {'error': 'Token is missing'}

    return wrapper


@main.route('/api/notes')
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


@main.route('/api/note/<int:id>')
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


@main.route('/api/save', methods=['POST', 'PUT'])
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


@main.route('/api/delete/<int:id>', methods=['DELETE'])
@token_required
def delnote(id):

    n = Note.query.get(id)
    db.session.delete(n)
    db.session.commit()

    return {'msg': 'Note deleted.'}


@main.route('/api/delete', methods=['DELETE'])
@token_required
def delfolder():

    data = request.get_json()

    rows = Note.query.filter(and_(Note.folder.startswith(
        data['folder']), Note.userid == g.userid)).all()

    for row in rows:
        db.session.delete(row)

    db.session.commit()

    return {'msg': 'Folder deleted.'}
