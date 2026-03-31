from flask import Flask, render_template, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped
from sqlalchemy import select
from flask_restful import Resource, Api, reqparse, marshal_with, fields, abort
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from functools import wraps
import bcrypt
import jwt
import os

load_dotenv() # load jwt_secret from .env
app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db" 

jwt_secret = os.environ.get("JWT_SECRET") # get it 

db = SQLAlchemy(app) # 
api = Api(app)

class UserModel(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(16), unique=True, nullable=False)
    password: Mapped[str] = db.Column(db.String(20), nullable=False)
    email: Mapped[str] = db.Column(db.String(50), unique=True, nullable=False)

user_args = reqparse.RequestParser()
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
        users = db.session.execute(select(UserModel)).scalars().all()
        return users
    
    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"], password=bcrypt.hashpw(args["password"].encode('utf-8'), bcrypt.gensalt()))
        db.session.add(user)
        db.session.commit()
        users = db.session.execute(select(UserModel)).scalars().all()
        return users, 201

class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = db.session.execute(select(UserModel).where(UserModel.id == id)).scalars().first()
        if not user:
            abort(404)
        return user
    
    @marshal_with(user_fields)
    def patch(self, id):
        args = user_args.parse_args()
        user = db.session.execute(select(UserModel).where(UserModel.id == id)).scalars().first()
        if not user:
            abort(404)
        user.name = args["name"]
        user.password = args["password"]
        user.email = args["email"]
        db.session.commit()
        return user
    
    @marshal_with(user_fields)
    def delete(self, id):
        user = db.session.execute(select(UserModel).where(UserModel.id == id)).scalars().first()
        if not user:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        users = db.session.execute(select(UserModel)).scalars().all()
        return users, 204

api.add_resource(User, '/users/<int:id>')
api.add_resource(Users, "/users")

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs): 
        token = request.args.get('token')
        if not token:
            return render_template("error.html", message="401, Unauthorized. Please Login or Register")
        
        try:
            payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        except:
            return jsonify({'Alert':"Invalid Token"})
        return func(*args, **kwargs)    
    return decorated

@app.route("/")
def public():
    return render_template("public.html")

@app.route("/login", methods=['POST'])
def login():
    user = db.session.execute(select(UserModel).where(UserModel.email == request.form['email'])).scalars().first()
    hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
    if bcrypt.checkpw(hashed.encode('utf-8'), user.password):
        return render_template("login.html", error="401, Email or Password is incorrect.")

    session['logged id'] = True
    token = jwt.encode({
        "user": request.form['name'],
        "expiration": datetime.now(timezone.utc) + timedelta(seconds=500),
    },
    jwt_secret)
    return jsonify({"token": token})



@app.route("/register", methods=['POST'])
def register():
    if not len(request.form['email']) <= 50:
        return render_template("register.html", error=1)
    elif not len(request.form['name']) <= 16:
        return render_template("register.html", error=2)
    elif not len(request.form['password']) <= 20:
        return render_template("register.html", error=3)
    
    hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
    user = UserModel(name=request.form['name'], email=request.form['email'], password=hashed)
    db.session.add(user)
    db.session.commit()
    users = db.session.execute(select(UserModel)).scalars().all()
    
    session['logged id'] = True

    token = jwt.encode({
        "user": request.form['name'],
        "expiration": datetime.now(timezone.utc) + timedelta(seconds=500),
    },
    jwt_secret)

    return jsonify({"token": token}), users
    

@app.route('/auth')
@token_required
def auth():
    return "JWT is verified. Welcome to ya dashboard"

with app.app_context():
    db.create_all()  

if __name__ == "__main__":
    app.run(debug=True)

