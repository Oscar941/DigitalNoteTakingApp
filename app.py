from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Notebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebook.id'), nullable=False)

@app.route('/register', methods=['POST'])
def register_user():
    username = request.json['username']
    password = request.json['password']
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login_user():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/notebooks', methods=['GET', 'POST'])
def manage_notebooks():
    if request.method == 'POST':
        title = request.json['title']
        user_id = request.json['user_id']  
        new_notebook = Notebook(title=title, user_id=user_id)
        db.session.add(new_notebook)
        db.session.commit()
        return jsonify({'message': 'Notebook created successfully'}), 201
    else:
        notebooks = Notebook.query.all()
        return jsonify([{'id': notebook.id, 'title': notebook.title} for notebook in notebooks]), 200

@app.route('/notes', methods=['GET', 'POST'])
def manage_notes():
    if request.method == 'POST':
        content = request.json['content']
        notebook_id = request.json['notebook_id']  
        new_note = Note(content=content, notebook_id=notebook_id)
        db.session.add(new_note)
        db.session.commit()
        return jsonify({'message': 'Note added successfully'}), 201
    else:
        notes = Note.query.all()
        return jsonify([{'id': note.id, 'content': note.content} for note in notes]), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)