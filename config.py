import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLIENT_ID = (
        '691323965407-j0d8hin5iv5jpphq22nkg098a60l0e2g.apps.'
        'googleusercontent.com')
