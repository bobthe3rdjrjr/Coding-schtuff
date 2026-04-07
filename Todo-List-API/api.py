from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from flask import request, jsonify, Flask
from flask_restful import reqparse, marshal, marshal_with, fields, abort, Resource, Api
from sqlalchemy import create_engine, select, String, ForeignKey
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

# Todo List Model
class TodoModel(Base):
    __tablename__ = "todo_model"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_model.id"), nullable=False, )
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

Base.metadata.create_all(engine)

load_dotenv()
jwt_secret = os.environ.get("JWT_SECRET")

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name is required")
user_args.add_argument('password', type=str, required=True, help="Password is required")
user_args.add_argument('email', type=str, required=True, help="Email is required")

todo_args = reqparse.RequestParser()
todo_args.add_argument("title", type=str, required=True, help="Please give a description for your todo item.")
todo_args.add_argument("description", type=str, default="No description.")

gettodo_args = reqparse.RequestParser()
gettodo_args.add_argument("limit", type=int, default=10)
gettodo_args.add_argument("filter", type=str, case_sensitive=False)
gettodo_args.add_argument("page", type=int, default=0)

user_fields = {
    'name': fields.String,
    'email': fields.String
}
todo_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String
}

# TODO: Implement verification to check whether its the right user
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs): 
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return {"Alert!": 'Token is Missing. Go to /login to login or /users and then post your register data. Remmeber to put the token into the Authorization header.'}, 401
        elif not auth_header.startswith('Bearer '):
            return {"Alert!": 'Token improper or corrupted. Missing "Bearer " initialization.'}, 401

        token = auth_header.split(' ')[1]
        
        try:
            payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return {"Alert!":"Expired token. Please login again and use that token."}, 401
        except jwt.InvalidTokenError:
            return {'Alert!':"Invalid Token"}, 401
        
        kwargs['current_user'] = payload['user']

        return func(*args, **kwargs)
    return decorated

class Users(Resource):
    @token_required
    @marshal_with(user_fields)  
    def get(self, current_user):
        with Session(engine) as session:
            users = session.execute(select(UserModel)).scalars().all()
            return users
    
    def post(self, current_user):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"], password=bcrypt.hashpw(args["password"].encode('utf-8'), bcrypt.gensalt()))
        with Session(engine) as session:
            session.add(user)
            session.commit()
      
        token = jwt.encode({
            "user": user.id,
            "email": user.email,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=2500),
        },
        jwt_secret)
        return jsonify({"token": token})

class User(Resource):
    method_decorators = [token_required]  

    @marshal_with(user_fields)
    def get(self, id, current_user):
        with Session(engine) as session:
            user = session.execute(select(UserModel).where(UserModel.id == id)).scalars().first()
            if not user:
                abort(404)
            return user
    
    @marshal_with(user_fields)
    def patch(self, id, current_user):
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
    def delete(self, id, current_user):
        with Session(engine) as session:
            user = session.execute(select(UserModel).where(UserModel.id == id)).scalars().first()
        if not user:
            abort(404)
        
        with Session(engine) as session:
            session.delete(user)
            session.commit()
            users = session.execute(select(UserModel)).scalars().all()
            return users, 204

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
        user = session.execute(select(UserModel).where(UserModel.email == email)).scalars().first()
    if not user:
        return jsonify("404, User not found")

    if bcrypt.checkpw(bytes(data['password'], "utf-8"), user.password):
        token = jwt.encode({
            "user": user.id,
            "email": user.email,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=2500),
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

# TODO: Implement Pagination
# Todo List CRUD
class Todos(Resource):
    method_decorators = [token_required] 

    def get(self, current_user):
        args = gettodo_args.parse_args()

        with Session(engine) as session:
            applicable = session.execute(select(TodoModel).where(TodoModel.user_id == current_user)).scalars().all()
            if args["filter"]:
                filter: String = args["filter"]
                titled = []
                desc = []
                for item in applicable:
                    if filter in item.title.lower():
                        titled.append(item)
                    elif filter in item.description.lower():
                        desc.append(item)
                applicable = titled + desc

        pages = []
        count = -1
        page = []
        while 1:
            count += 1
            try:
                todo = applicable[count]
            except IndexError:
                pages.append(page)
                break

            page.append(todo)
            if not len(page) % args["limit"]:
                pages.append(page)
                page = []

        try: 
            return {
            "todos": marshal(pages[args["page"] - 1], todo_fields),
            "pages": len(pages),
            "limit": args["limit"]
            }, 200
        except IndexError:
            return {"Alert!": "Invalid page number."}, 422
            

    @marshal_with(todo_fields)
    def post(self, current_user):
        args = todo_args.parse_args()
        todo = TodoModel(title=args["title"], description=args["description"], user_id=current_user)
        
        with Session(engine) as session:
            session.add(todo)
            session.commit()
            session.refresh(todo)
            session.expunge(todo)
        return todo, 201
    
class TodoEntry(Resource):
    method_decorators = [token_required] 

    def delete(self, id, current_user):
        with Session(engine) as session:
            entry = session.execute(select(TodoModel).where(TodoModel.id == id)).scalars().first()
            if not entry:
                abort(404)
            elif entry.user_id != current_user:
                return {"Alert!": "Forbidden"}, 403
            session.delete(entry)
            session.commit()
            return 204

    @marshal_with(todo_fields)
    def put(self, id, current_user):
        args = todo_args.parse_args()

        with Session(engine) as session:
            todo = session.execute(select(TodoModel).where(TodoModel.id == id)).scalars().first()
            if not todo:
                abort(404)
            elif todo.user_id != current_user:
                return {"Alert!": "Forbidden"}, 403
            todo.title = args["title"]
            todo.description = args["description"]
            session.commit()
            return todo

api.add_resource(User, '/users/<int:id>')
api.add_resource(Users, "/users")
api.add_resource(Todos, "/todos")
api.add_resource(TodoEntry, "/todos/<int:id>")

if __name__ == "__main__":
    app.run()