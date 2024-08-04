from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

database_user = os.getenv('DB_USER')
database_password = os.getenv('DB_PASSWORD')
database_host = os.getenv('DB_HOST')
database_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{database_user}:{database_password}@{database_host}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Notebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notes_list = db.relationship('Note', backref='owner_notebook', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_content = db.Column(db.Text, nullable=False)
    parent_notebook_id = db.Column(db.Integer, db.ForeignKey('notebook.id'), nullable=False)

@app.route('/register', methods=['POST'])
def register_new_user():
    username = request.json['username']
    password = request.json['password']
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400
    new_user = User(username=username)
    new_user.hash_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def authenticate_user():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/notebooks', methods=['GET', 'POST'])
def notebook_operations():
    if request.method == 'POST':
        title = request.json['title']
        owner_id = request.json['user_id']  
        new_notebook = Notebook(title=title, user_id=owner_id)
        db.session.add(new_notebook)
        db.session.commit()
        return jsonify({'message': 'Notebook created successfully'}), 201
    else:
        all_notebooks = Notebook.query.all()
        return jsonify([{'id': notebook.id, 'title': notebook.title} for notebook in all_notebooks]), 200

@app.route('/notes', methods=['GET', 'POST'])
def note_operations():
    if request.method == 'POST':
        content = request.json['content']
        notebook_id = request.json['notebook_id']  
        new_note = Note(content=content, notebook_id=notebook_id)
        db.session.add(new_note)
        db.session.commit()
        return jsonify({'message': 'Note created successfully'}), 201
    else:
        all_notes = Note.query.all()
        return jsonify([{'id': note.id, 'content': note.text_content, 'notebook_id': note.parent_notebook_id} for note in all_notes]), 200

@app.route('/search', methods=['GET'])
def search_notes_by_keyword():
    search_keyword = request.args.get('keyword', '')  # Get keyword from query parameter
    filtered_notes = Note.query.filter(Note.content.like(f'%{search_keyword}%')).all()  # Search for notes containing the keyword
    return jsonify([{'id': note.id, 'content': note.text_content, 'notebook_id': note.parent_notebook_id} for note in filtered_notes]), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)