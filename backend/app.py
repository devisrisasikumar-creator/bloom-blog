from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['JWT_SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)
CORS(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

@app.route('/')
def home():
    return jsonify({"message": "Blog API Running"})

@app.route('/register', methods=['POST'])
def register():
    data = request.json

    hashed_password = generate_password_hash(data['password'])

    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token)

    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()

    result = []

    for post in posts:
        result.append({
            "id": post.id,
            "title": post.title,
            "content": post.content
        })

    return jsonify(result)

@app.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    data = request.json

    current_user = get_jwt_identity()

    post = Post(
        title=data['title'],
        content=data['content'],
        user_id=current_user
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "Post created successfully"})

@app.route('/posts/<int:id>', methods=['PUT'])
@jwt_required()
def update_post(id):
    data = request.json

    post = Post.query.get(id)

    if not post:
        return jsonify({"message": "Post not found"}), 404

    post.title = data['title']
    post.content = data['content']

    db.session.commit()

    return jsonify({"message": "Post updated successfully"})

@app.route('/posts/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = Post.query.get(id)

    if not post:
        return jsonify({"message": "Post not found"}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post deleted successfully"})

@app.route('/comments', methods=['POST'])
@jwt_required()
def add_comment():
    data = request.json

    current_user = get_jwt_identity()

    comment = Comment(
        text=data['text'],
        user_id=current_user,
        post_id=data['post_id']
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify({"message": "Comment added successfully"})

@app.route('/comments/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()

    result = []

    for comment in comments:
        result.append({
            "id": comment.id,
            "text": comment.text
        })

    return jsonify(result)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)