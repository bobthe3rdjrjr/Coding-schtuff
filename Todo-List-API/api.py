from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from flask import request, jsonify, Flask
from flask_sqlalchemy import SQLAlchemy, session
from flask_restful import reqparse, marshal_with, fields, abort, Resource, Api
from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from functools import wraps
import bcrypt
import jwt
import os

load_dotenv() 
jwt_secret = os.environ.get("JWT_SECRET") 
engine = create_engine("sqlite:///app.db")
app = Flask(__name__)
api = Api(app)

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "user_model"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), unique=True, nullable=False) 
    password: Mapped[str] = mapped_column(String(50), nullable=False) 
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False) 

    def __repr__(self):
        return f"Name: {self.name}, Email: {self.email}"

Base.metadata.create_all(engine)

load_dotenv()
jwt_secret = os.environ.get("JWT_SECRET")

user_args = reqparse.RequestParser() # TODO: Replace
user_args.add_argument('name', type=str, required=True, help="Name is required")
user_args.add_argument('password', type=str, required=True, help="Password is required")
user_args.add_argument('email', type=str, required=True, help="Email is required")

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'password': fields.String,
    'email': fields.String
}

class Users(Resource):
    @marshal_with(user_fields)  
    def get(self):
        with Session(engine) as session:
            users = session.execute(select(UserModel)).scalars().all()
        return users
    
    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"], password=bcrypt.hashpw(args["password"].encode('utf-8'), bcrypt.gensalt()))
        with Session(engine) as session:
            session.add(user)
            session.commit()
            users = session.execute(select(UserModel)).scalars().all()
        return users, 201

class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        with Session(engine) as session:
            user = session.execute(select(UserModel).where(UserModel.id == id)).scalars().first()
        if not user:
            abort(404)
        return user
    
    @marshal_with(user_fields)
    def patch(self, id):
        args = user_args.parse_args()
        with Session(engine) as session:
            user = session.execute(select(UserModel).where(UserModel.id == id)).scalars().first()     
        if not user:
            abort(404)
        user.name = args["name"]
        user.email = args["email"]
        with Session(engine) as session:
            session.commit()
        return user
    
    @marshal_with(user_fields)
    def delete(self, id):
        with Session(engine) as session:
            user = session.execute(select(UserModel).where(UserModel.id == id)).scalars().first()
        if not user:
            abort(404)
        
        with Session(engine) as session:
            session.delete(user)
            session.commit()
            users = session.execute(select(UserModel)).scalars().all()
        return users, 204

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs): 
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"Alert!": 'Token is Missing. Go to /login to login or /users and then post your login. Remmeber to put the token into the Authorization header.'}), 401

        token = auth_header.split(' ')[1]
        
        try:
            payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"Alert":"Expired token. Please login again and use that token."})
        except jwt.InvalidTokenError:
            return jsonify({'Alert':"Invalid Token"})
        return func(*args, **kwargs)    
    return decorated

api.add_resource(User, '/users/<int:id>')
api.add_resource(Users, "/users")

# Define routes:
@app.route("/")
def home():
    return "yo"

# Login
@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']

    with Session(engine) as session:
        user = session.execute(select(UserModel).where(email == email)).scalars().first()
    if not user:
        return jsonify("404, User not found")

    if bcrypt.checkpw(bytes(data['password'], "utf-8"), user.password):
        token = jwt.encode({
            "user": user.name,
            "email": data['email'],
            "exp": datetime.now(timezone.utc) + timedelta(seconds=500),
        },
        jwt_secret)
        return jsonify({"token": token})
    else:
        return jsonify(404)

# Authenticated
@app.route('/home')
@token_required
def nothome():
    return "JWT is verified. Welcome to ya dashboard"

if __name__ == "__main__":
    app.run(debug=True)

