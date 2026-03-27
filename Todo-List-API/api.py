from flask import Flask, render_template, request, jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped
from flask_restful import Resource, Api, reqparse, marshal_with, fields, abort
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from functools import wraps
import jwt
import os

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

jwt_secret = os.environ.get("JWT_SECRET")

db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    username: Mapped[str] = db.Column(db.String(15), unique=True, nullable=False)
    email: Mapped[str] = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User: {self.username}, Email: {self.email}"

user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help="Username is required")
user_args.add_argument('email', type=str, required=True, help="Email is required")

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}

class Users(Resource):
    @marshal_with(user_fields)  
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(username=args["username"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201

class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404)
        return user
    
    @marshal_with(user_fields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404)
        user.username = args["username"]
        user.email = args["email"]
        db.session.commit()
        return user
    
    @marshal_with(user_fields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 204

api.add_resource(User, '/users/<int:id>')
api.add_resource(Users, "/users")

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs): 
        token = request/args.get('token')
        if not token:
            return jsonify({"Alert!": 'Token is Missing.'})
        
        try:
            payload = jwt.decode(token, jwt_secret)
        except:
            return jsonify({'Alert':"Invalid Token"})
        return decorated

# Define routes:
@app.route("/")
def home():
    if not session.get:
        return render_template("login.html")
    return render_template("home.html")

# Login
@app.route("/login", methods=['POST'])
def login():
    if request.form['username'] and request.form['password']:
        session['logged id'] = True
        token = jwt.encode({
            "user": request.form['username'],
            "expiration": datetime.now(timezone.utc) + timedelta(seconds=500),
        },
        jwt_secret)
        return jsonify({"token": token.decode("utf-8")})
    else:
        return make_response("Unable to verify", 403, {"WWW-Authenticate" : 'Basic realm:"Authentication Failed"'})

# Public
@app.route("/public")
def public():
    return "For Public"

# Authenticated
@app.route('/auth')
@token_required
def auth():
    return "JWT is verified. Welcome to ya dashboard"

with app.app_context():
    db.create_all()  # Creates app.db and the users table if they don't exist

if __name__ == "__main__":
    app.run(debug=True)

