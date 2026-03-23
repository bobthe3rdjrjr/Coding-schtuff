from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped
from flask_restful import Resource, Api, reqparse, marshal_with, fields, abort

# Make app and configure to an sqlite app database
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
    
# Add arguments using reqparser
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="gng just put this in")
user_args.add_argument('email', type=str, required=True, help="gng just put this in")

class Users(Resource):
    def get(self):
        users=UserModel.query.all()
        return users
    
api.add_resource(Users, "/users")

@app.route("/")
def home():
    return render_template("home.html")

app.run(debug=True)