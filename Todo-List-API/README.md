# Todo List API

This is a simple API for a todo list with pagination, filtering, password encryption, & user authentication from https://roadmap.sh/projects/todo-list-api.

## Setup 

1. **Clone the Repository** 
``` bash
git clone https://github.com/bobthe3rdjrjr/Coding-schtuff.git
cd ./Coding-schtuff/Todo-List-API
```
2. **Install Dependencies**
``` bash
pip install -r requirements.txt
```
3. **Make a .env file & put your secret key inside, as seen in .env.example**
``` .env
JWT_SECRET=super_secret_&_secure_key
```
4. **Run the application**
``` bash
python file_location
```

## API Endpoints

### /login
**Method:** `POST`  
**Description:** Logs in to an existing account using the user's email & password.   
**Request Body:** 
``` json
{
    "email": "your_email",
    "password": "your_password"
}
```
**Response:**
``` json
{
    "token": "the_token"
}
```
**Note:** Your token must be put into the Authorization header with the prefix "Bearer " (Bearer followed by a space) and then your token. (eg. "Bearer tokenthat'ssuperduperlongandcool").



### /users
**Method:** `POST`                             
**Description:** Posts a new user to the database; Registration
**Request Body:**
``` json
{
    "name": "your_name",
    "email": "your_email",
    "password": "your_password"
}
```
**Response:**
``` json
{
    "token": "the_token"
} 
```

## token_required
**Description:** The function that check's whether you're jwt token is valid.  
**Possible Error's:**
* Token is missing: **401**  
***Alert!**": 'Token is Missing. Go to /login to login or /users and then post your register data. Remember to put the token into the Authorization header.'*  

* Token is missing "Bearer " prefix, or is corrupted ig. **401**  
***"Alert!**": 'Token improper or corrupted. Missing "Bearer " initialization.'*  

* Signature is expired **401**  
***"Alert!**":"Expired token. Please login again and use that token."*

* Token is invalid **401**  
***'Alert!**':"Invalid Token"*

### *All following endpoints require a valid jwt token inside your authorization header, checked via token_required.*

### /users
**Method:** `GET`  
**Description:** Gets the name & email of all users.  
**Response:** 200
``` json
{
  {
    "name": "guy1",
    "email": "email@email.com"
  },
  {
    "name": "guy2",
    "email": "other_email@email.com"
  }
}
```

### /users/<int:id>
**Method:** `GET`                             
**Description:** Gets the name & email of the user.  
**Response:** 200
``` json
{
  {
    "name": "guy1",
    "email": "email@email.com"
  }
}
```

### /users/<int:id>
**Method:** `PATCH`                             
**Description:** Changes the name/email of a user.  
**Request Body:**
``` json
{
  {
    "name": "guy1",
    "email": "email@email.com"
  }
}
```
**Response:**
``` json
{
  {
    "name": "guy1",
    "email": "email@email.com"
  }
}
```

### /users/<int:id>
**Method:** `DELETE`                             
**Description:** Deletes a user. I realize I prob shouldn't have added this but whatever.  
**Request Body:** 204
``` json
{
  {
    "name": "guy1",
    "email": "email@email.com"
  }
}
```
**Response:**
``` json
{
  {
    "name": "guy2",
    "email": "email@email.com"
  },
  {
    "name": "guy3",
    "email": "otheremail@email.com"
  }
}
``` 
## *All following endpoints check that you are logged in as the given user.*

### /todos
**Method:** `GET`   
**Description:** Gets all todo entry's made by the person the user's logged in as, with pagination.  
**Request Body:**
``` json
{
  "limit": "5",
  "page": 2
}
```
**Response:** 200
``` json
{
  "todos:" [
    {
      "title": "cool title",
      "description": "cool description"
    },
    {
      "title": "very cool title",
      "description": "very cool description"
    },
    {
      "title": "very very cool title",
      "description": "very very cool description"
    },
    {
      "title": "very very very cool title",
      "description": "very very very cool description"
    },
    {
      "title": "very very very very cool title",
      "description": "very very very very cool description"
    }
  ],
  "pages:" 3,
  "limit:" 5
}
``` 
**Note:** This is the 2nd page of the 3 pages of todo entry's, the default limit is 10.

**Possible Error's:**
* Page number causes an IndexError due to the given page number being over the amount of pages given. **422**  
 ***"Alert!":** "Invalid page number."*

### /todos
**Method:** `POST`  
**Description:** Posts a todo entry to the api with a title & description. 
**Request Body:** 
``` json
{
    "title": "Cool & descriptive title",
    "description": "Cool & descriptive description."
}
```
**Response:** 201
``` json
{
    "title": "Cool & descriptive title",
    "description": "Cool & descriptive  description."
}
```

### /todos/<int:id> 
**Method:** `DELETE`  
**Description:** Deletes the selected todo entry.  
**Response:** 204

### /todos/<int:id>
**Method:** `PUT`  
**Description:** Replaces the todo entry associated with the id with the entry in the response body.
**Request Body:** 
``` json
{
    "title": "Cool & descriptive title",
    "description": "Cool & descriptive description."
}
```
**Response:**
``` json
{
    "title": "Cool & descriptive title",
    "description": "Cool & descriptive description."
}
```