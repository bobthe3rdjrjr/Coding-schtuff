<<<<<<< HEAD
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from flask_sqlalchemy import p
from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
import bcrypt
import jwt
import os

load_dotenv() 
jwt_secret = os.environ.get("JWT_SECRET") 
db = create_engine("sqlite:///app.db")

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "user_model"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), unique=True, nullable=False) 
    password: Mapped[str] = mapped_column(String(20), nullable=False) 
    email: Mapped[str] = mapped_column(String(50), nullable=False) 

# Create tables
Base.metadata.create_all(db)
=======
from flask import Flask, render_template, jsonify, request, session
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
    name: Mapped[str] = db.Column(db.String(15), unique=True, nullable=False)
    email: Mapped[str] = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User: {self.name}, Email: {self.email}"
>>>>>>> parent of 12dc244 (did some stuff)

# Query using a session
with Session(db) as session:
    users = session.execute(select(UserModel)).scalars().all()

user_args = reqparse.RequestParser() # type: ignore # TODO: Replace
user_args.add_argument('name', type=str, required=True, help="Name is required")
user_args.add_argument('password', type=str, required=True, help="Password is required")
user_args.add_argument('email', type=str, required=True, help="Email is required")

<<<<<<< HEAD
def get():
    users = db.session.execute(select(UserModel)).scalars().all()
    return users
    
    
def post():
    args = user_args.parse_args()
    user = UserModel(name=args["name"], email=args["email"], password=bcrypt.hashpw(args["password"].encode('utf-8'), bcrypt.gensalt()))
    db.session.add(user)
    db.session.commit()
    users = db.session.execute(select(UserModel)).scalars().all()
    return users, 201

def get(id):
    user = db.session.execute(select(UserModel).where(UserModel.id == id)).scalars().first()
    if not user:
        raise RuntimeError("user dont exist")
    return user
    
    
def patch(id):
    args = user_args.parse_args()
    user = db.session.execute(select(UserModel).where(UserModel.id == id)).scalars().first()
    if not user:
        raise RuntimeError("user dont exist")
    user.name = args["name"]
    user.password = args["password"]
    user.email = args["email"]
    db.session.commit()
    return user
    
    
def delete(id):
    user = db.session.execute(select(UserModel).where(UserModel.id == id)).scalars().first()
    if not user:
        raise RuntimeError("user dont exist")
    db.session.delete(user)
    db.session.commit()
    users = db.session.execute(select(UserModel)).scalars().all()
    return users, 204

api.add_resource(User, '/users/<int:id>') # type: ignore # TODO: Replace
api.add_resource(Users, "/users") # type: ignore # TODO: Replace

=======
user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'password': fields.String,
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
        user = UserModel(name=args["name"], email=args["email"])
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
        user.name = args["name"]
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
        token = request.args.get('token')
        if not token:
            return jsonify({"Alert!": 'Token is Missing.'})
        
        try:
            payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        except:
            return jsonify({'Alert':"Invalid Token"})
        return func(*args, **kwargs)    
    return decorated

# Define routes:
@app.route("/")
def home():
    if not session.get("logged id"):
        return render_template("login.html")
    return render_template("home.html")

# Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        pw = request.form['password']
        if name and pw:
            session['logged id'] = True
            token = jwt.encode({
                "user": request.form['name'],
                "expiration": datetime.now(timezone.utc) + timedelta(seconds=500),
            },
            jwt_secret)
            return jsonify({"token": token})
        else:
            return render_template("error.html", message="404, User Not Found")
    else: 
        return render_template("login.html")

# Public
@app.route("/register")
def register():
    return "For Public"

# Authenticated
@app.route('/auth')
@token_required
def auth():
    return "JWT is verified. Welcome to ya dashboard"

with app.app_context():
    db.create_all()  # Creates app.db and the users table if they don't exist
>>>>>>> parent of 12dc244 (did some stuff)


