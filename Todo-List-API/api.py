from flask import Flask, render_template, request, jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped
from flask_restful import Resource, Api, reqparse, marshal_with, fields, abort
from datetime import datetime, timedelta
from functools import wraps
import jwt


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    username: Mapped[str] = db.Column(db.String(15), unique=True, nullable=False)
    email: Mapped[str] = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User: {self.username}, Email: {self.email}"

# Argument names now match the model's column names
user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help="Username is required")
user_args.add_argument('email', type=str, required=True, help="Email is required")

# Tells Flask-RESTful how to serialize a UserModel into JSON
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}

class Users(Resource):
    @marshal_with(user_fields)  # Automatically converts model objects to JSON
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

# Define routes:
@app.route("/")
def home():
    return render_template("home.html")

with app.app_context():
    db.create_all()  # Creates app.db and the users table if they don't exist

if __name__ == "__main__":
    app.run(debug=True)

