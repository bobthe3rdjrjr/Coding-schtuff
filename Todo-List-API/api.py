from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
import bcrypt
import jwt
import os

load_dotenv() 
jwt_secret = os.environ.get("JWT_SECRET") # get it 

db = create_engine("sqlite:///app.db")

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "user_model"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15), unique=True, nullable=False) # pyright: ignore[reportUndefinedVariable]
    password: Mapped[str] = mapped_column(String(20), nullable=False) # pyright: ignore[reportUndefinedVariable]
    email: Mapped[str] = mapped_column(String(50), nullable=False) # pyright: ignore[reportUndefinedVariable]

# Create tables
Base.metadata.create_all(db)

# Query using a session
with Session(db) as session:
    users = session.execute(select(UserModel)).scalars().all()

user_args = reqparse.RequestParser() # type: ignore # TODO: Replace
user_args.add_argument('name', type=str, required=True, help="Name is required")
user_args.add_argument('password', type=str, required=True, help="Password is required")
user_args.add_argument('email', type=str, required=True, help="Email is required")

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



