from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
import sys
from datetime import datetime

db = SQLAlchemy()

class UserAccount(db.Model):
    __tablename__ = 'user_accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_notes = db.relationship('UserNote', backref='author', lazy=True)
    user_notebooks = db.relationship('UserNotebook', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<UserAccount {self.username}>'

class UserNote(db.Model):
    __tablename__ = 'user_notes'
    id = db.Column(db.Integer, primary_key=True)
    note_title = db.Column(db.String(100), nullable=False)
    note_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user_accounts.id'), nullable=False)
    notebook_id = db.Column(db.Integer, db.ForeignKey('user_notebooks.id'), nullable=True)

    def __repr__(self):
        return f'<UserNote {self.note_title}>'

class UserNotebook(db.Model):
    __tablename__ = 'user_notebooks'
    id = db.Column(db.Integer, primary_key=True)
    notebook_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user_accounts.id'), nullable=False)
    notebook_notes = db.relationship('UserNote', backref='notebook', lazy=True)

    def __repr__(self):
        return f'<UserNotebook {self.notebook_name}>'

def initialize_database(application):
    try:
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_database.db'
        application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(application)
        with application.app_context():
            db.create_all()
        print("Database initialized successfully!")
    except SQLAlchemyError as error:
        print("Failed to initialize database:", str(error))
        sys.exit(1)