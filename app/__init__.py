from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
CORS(app, resources={r'/*': {'origins': 'https://all-notes.netlify.app'}})
from app.main import main
from app.auth import auth
app.register_blueprint(main)
app.register_blueprint(auth)

from app import models
