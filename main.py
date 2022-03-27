from typing import List

from fastapi import FastAPI, status

from models.tweet import Tweet
from models.user import User

app = FastAPI()


## Users
@app.post(
    '/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary='Register a User',
    tags=['Users'],
)
def signup():
    ...


@app.post(
    '/login',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Login a User',
    tags=['Users'],
)
def login():
    ...


@app.get(
    '/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary='Show all Users',
    tags=['Users'],
)
def show_all_users():
    ...


@app.get(
    '/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Show a User data',
    tags=['Users'],
)
def show_user_detail():
    ...


@app.delete(
    '/users/{user_id}/delete',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Delete a User',
    tags=['Users'],
)
def delete_user():
    ...


@app.put(
    '/users/{user_id}/update',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='update a User',
    tags=['Users'],
)
def update_user():
    ...


## Tweets


@app.get(
    '/',
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary='Show all tweets',
    tags=['Tweets'],
)
def home():
    return {'Twitter API': 'v1'}


@app.post(
    '/post',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary='Create a tweet',
    tags=['Tweets'],
)
def post():
    ...


@app.get(
    '/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Show a Tweet data',
    tags=['Tweets'],
)
def show_tweet_detail():
    ...


@app.delete(
    '/tweets/{tweet_id}/delete',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Delete a Tweet',
    tags=['Tweets'],
)
def delete_tweet():
    ...


@app.put(
    '/tweets/{tweet_id}/update',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='update a Tweet',
    tags=['Tweets'],
)
def update_tweet():
    ...
