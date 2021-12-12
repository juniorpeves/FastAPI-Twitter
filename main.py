# Python
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel # Permite crear los modelos
from pydantic import EmailStr # Valida emails
from pydantic import Field # Validar los atributos de un modelo

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body

app = FastAPI()

#Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64        
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User):
        password: str = Field(
        ...,
        min_length=8,
        max_length=64        
    )
        
class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: UserBase = Field(...)

# Path Operations

## Users

### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def singup(user: UserRegister = Body(...)):
    """
    # [Register a User]

    This path operation register a user in the app

    ### Parameters
    - Request body parameter: 
        - **user: userRegister** -> A person model with first name, last name, etc

    ### Returns a json with the basic user information:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: datetime        
    """  
    with open("users.json", "r+", encoding="utf-8") as f:
        # Abriendo el archivo en modo de lectura & escritura
        results = json.loads(f.read()) # Convertirlo a simil de json
        user_dict = user.dict() # De json a diccionario
        user_dict["user_id"] = str(user_dict["user_id"]) #Acomodando a variable a str
        user_dict["birth_date"] = str(user_dict["birth_date"]) #Acomodando a variable a str
        results.append(user_dict) #Añadiendo nuevo usuario al archivo
        f.seek(0) # Moverte al inicio del archivo
        f.write(json.dumps(results)) # Convirtiendo de una list_dic a un json
        return user
        

### Login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login():
    pass

### Show all User
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all User",
    tags=["Users"]
)
def show_all_users():
    """
    # [Show all users]

    This path operation shows all user in the app

    ### Parameters
    - 

    ### Returns a json with the all users in the app, with the following keys:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: datetime        
    """ 
    with open("user.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read()) 
        return results

### Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user():
    pass

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user():
    pass

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user():
    pass

## Tweets

### Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all Tweets",
    tags=["Tweets"]
)
def home():
    """
    # [Show all tweets]

    This path operation shows all tweets in the app

    ### Parameters
    - 

    ### Returns a json with the all tweets in the app, with the following keys:
    - tweet_id: UUID
    - content: str
    - create_at: datetime
    - update_at: Optional[datetime]
    - by: User      
    """ 
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read()) 
        return results

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)):
    """
    # [Post a tweet]

    This path operation register a tweet in the app

    ### Parameters
    - Request body parameter: 
        - **tweet: Tweet** 

    ### Returns a json with the basic tweet information:
    - tweet_id: UUID
    - content: str
    - create_at: datetime
    - update_at: Optional[datetime]
    - by: User
    """  
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read()) 
        tweet_dict =tweet.dict() 
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"]) 
        tweet_dict["created_at"] = str(tweet_dict["created_at"]) 
        if tweet_dict["updated_at"]:
            tweet_dict["updated_at"] = str(tweet_dict["updated_at"]) 
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        results.append(tweet_dict)
        f.seek(0) 
        f.write(json.dumps(results))
        return tweet

### Show a tweet
@app.get(
    path="/tweet/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet():
    pass

### Delete a tweet
@app.delete(
    path="/tweet/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet():
    pass

### Update a tweet
@app.put(
    path="/tweet/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet():
    pass