import json
from typing import List

from fastapi import FastAPI, status, Body, Form, Path, HTTPException
from pydantic import EmailStr

from models.tweet import Tweet
from models.user import User, UserRegister, UserLoginOut

app = FastAPI()

USERS_FILE = 'users.json'
TWEETS_FILE = 'tweets.json'
USER_NOT_FOUND = 'User not found'
TWEET_NOT_FOUND = 'Tweet not found'


## Users
@app.post(
    '/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary='Register a User',
    tags=['Users'],
)
def signup(user: UserRegister = Body(...)):
    """
    # Signup

    This path operation register a user in the app


    Parameters:

    - RequestBody parameter:
        - user: UserRegister


    Returns a json with the basic user information

    - Response model:
        - user: User:
            - user_id: UUID
            - email: EmailStr
            - first_name: str
            - last_name: str
            - birth_date: date
    """
    with open(USERS_FILE, 'r+', encoding='utf-8') as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['birthday'] = str(user_dict['birthday'])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user


@app.post(
    '/login',
    response_model=UserLoginOut,
    status_code=status.HTTP_200_OK,
    summary='Login a User',
    tags=['Users'],
)
def login(email: EmailStr = Form(...), password: str = Form(...)):
    """
    # Login

    This path operation able to user login in the app

    Parameters:

    - RequestBody parameters:
        - email: EmailStr
        - password: str

    Return a messages with login status

    - Response Model:
        - user: UserLoginOut
            - email: EmailStr
            - user_id: UUID
            - message: str
    """
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        users = json.loads(f.read())
        valid_user = next(
            (
                user
                for user in users
                if user['email'] == email and user['password'] == password
            ),
            None,
        )
        response = UserLoginOut(email=email, message='Login Failed')
        if valid_user:
            response = UserLoginOut(email=email, user_id=valid_user['user_id'])

        return response


@app.get(
    '/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary='Show all Users',
    tags=['Users'],
)
def show_all_users():
    """
    # Show all users

    This path operation list all users registered


    Parameters:

    -


    Returns a json list with the all users registered

    - Response model:
        - user: User:
            - user_id: UUID
            - email: EmailStr
            - first_name: str
            - last_name: str
            - birth_date: date
    """
    with open(USERS_FILE, 'r+', encoding='utf-8') as f:
        results = json.loads(f.read())
        return results


@app.get(
    '/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Show a User data',
    tags=['Users'],
)
def show_user_detail(user_id: str = Path(...)):
    """
    # Show user detail

    This path operation return a user detail by id

    Parameters:

    - user_id: str

    Return a json with user detail data:

    - Response model
        - user: User
            - user_id: UUID
            - email: EmailStr
            - first_name: str
            - last_name: str
            - birth_date: date

    """
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        users = json.loads(f.read())

        valid_user = next(
            (user for user in users if user['user_id'] == user_id),
            None,
        )
        if not valid_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
            )

        return valid_user


@app.delete(
    '/users/{user_id}/delete',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete a User',
    tags=['Users'],
)
def delete_user(user_id: str = Path(...)):
    """
    # Delete a user

    This path operation delete a user by id

    Parameters:

    - user_id: str

    Not return
    """
    with open(USERS_FILE, 'r+', encoding='utf-8') as f:
        users = json.loads(f.read())

        valid_user = next(
            (user for user in users if user['user_id'] == user_id),
            None,
        )
        if not valid_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
            )

        f.close()
        users.remove(valid_user)
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            f.seek(0)
            f.write(json.dumps(users))


@app.patch(
    '/users/{user_id}/update',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='update a User',
    tags=['Users'],
)
def update_user(user_id: str = Path(...), user: User = Body(...)):
    """
    # Update a user

    This path operation update a user data by id

    Parameters:

    - user_id: str
    - user: User

    Return a json with user detail data:

    - Response model
        - user: User
            - user_id: UUID
            - email: EmailStr
            - first_name: str
            - last_name: str
            - birth_date: date
    """
    with open(USERS_FILE, 'r+', encoding='utf-8') as f:
        users = json.loads(f.read())

        valid_user = next(
            (user for user in users if user['user_id'] == user_id),
            None,
        )
        if not valid_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
            )

        f.close()
        new_user_data = user.dict(exclude_unset=True)
        original_data = User(**valid_user)
        original_data = original_data.copy(update=new_user_data).dict()
        original_data['user_id'] = str(original_data['user_id'])
        original_data['birthday'] = str(original_data['birthday'])
        users[users.index(valid_user)] = original_data
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            f.seek(0)
            f.write(json.dumps(users))
        return original_data


## Tweets


@app.get(
    '/',
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary='Show all tweets',
    tags=['Tweets'],
)
def home():
    """
    # Show all Post

    This path operation show all tweets in the app


    Parameters:

    -


    Returns a json with the tweets list

    - Response model:
        - tweet: Tweet:
            - tweet_id: UUID
            - content: str
            - created_at: datetime
            - updated_at: datetime
            - author: User
    """
    with open('tweets.json', 'r+', encoding='utf-8') as f:
        results = json.loads(f.read())
        return results


@app.post(
    '/post',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary='Create a tweet',
    tags=['Tweets'],
)
def post(tweet: Tweet = Body(...)):
    """
    # Create a Post

    This path operation create a tweet


    Parameters:

    - RequestBody parameter:
        - tweet: Tweet


    Returns a json with the tweet information

    - Response model:
        - tweet: Tweet:
            - tweet_id: UUID
            - content: str
            - created_at: datetime
            - updated_at: datetime
            - author: User
    """
    with open(TWEETS_FILE, 'r+', encoding='utf-8') as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict['tweet_id'] = str(tweet_dict['tweet_id'])
        tweet_dict['created_at'] = str(tweet_dict['created_at'])
        if tweet_dict.get('updated_at'):
            tweet_dict['updated_at'] = str(tweet_dict['updated_at'])
        tweet_dict['author']['user_id'] = str(tweet_dict['author']['user_id'])
        tweet_dict['author']['birthday'] = str(
            tweet_dict['author']['birthday']
        )
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet


@app.get(
    '/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Show a Tweet data',
    tags=['Tweets'],
)
def show_tweet_detail(tweet_id: str = Path(...)):
    """
    # Show tweet detail

    This path operation return a tweet detail by id

    Parameters:

    - tweet_id: str

    Return a json with user detail data:

    - Response model
        - user: Tweet
            - tweet_id: UUID
            - content: str
            - created_at: datetime
            - updated_at: datetime
            - author: User

    """
    with open(TWEETS_FILE, 'r', encoding='utf-8') as f:
        tweets = json.loads(f.read())

        valid_tweet = next(
            (tweet for tweet in tweets if tweet['tweet_id'] == tweet_id),
            None,
        )
        if not valid_tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=TWEET_NOT_FOUND
            )

        return valid_tweet


@app.delete(
    '/tweets/{tweet_id}/delete',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete a Tweet',
    tags=['Tweets'],
)
def delete_tweet(tweet_id: str = Path(...)):
    """
    # Delete a tweet

    This path operation delete a tweet by id

    Parameters:

    - tweet_id: str

    Not return
    """
    with open(TWEETS_FILE, 'r+', encoding='utf-8') as f:
        tweets = json.loads(f.read())

        valid_tweet = next(
            (tweet for tweet in tweets if tweet['tweet_id'] == tweet_id),
            None,
        )
        if not valid_tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=TWEET_NOT_FOUND
            )

        f.close()
        tweets.remove(valid_tweet)
        with open(TWEETS_FILE, 'w', encoding='utf-8') as f:
            f.seek(0)
            f.write(json.dumps(tweets))


@app.patch(
    '/tweets/{tweet_id}/update',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='update a Tweet',
    tags=['Tweets'],
)
def update_tweet(tweet_id: str = Path(...), tweet: Tweet = Body(...)):
    """
    # Update a tweet

    This path operation update a tweet data by id

    Parameters:

    - tweet_id: str
    - tweet: Tweet

    Return a json with tweet detail data:

    - Response model
        - user: Tweet
            - tweet_id: UUID
            - content: str
            - created_at: datetime
            - updated_at: datetime
            - author: User
    """
    with open(TWEETS_FILE, 'r+', encoding='utf-8') as f:
        tweets = json.loads(f.read())

        valid_tweet = next(
            (tweet for tweet in tweets if tweet['tweet_id'] == tweet_id),
            None,
        )
        if not valid_tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=TWEET_NOT_FOUND
            )

        f.close()
        new_tweet_data = tweet.dict(exclude_unset=True)
        original_data = Tweet(**valid_tweet)
        original_data = original_data.copy(update=new_tweet_data).dict()
        original_data['tweet_id'] = str(original_data['tweet_id'])
        original_data['created_at'] = str(original_data['created_at'])
        original_data['updated_at'] = str(original_data['updated_at'])
        original_data['author']['user_id'] = str(
            original_data['author']['user_id']
        )
        original_data['author']['birthday'] = str(
            original_data['author']['birthday']
        )
        tweets[tweets.index(valid_tweet)] = original_data
        with open(TWEETS_FILE, 'w', encoding='utf-8') as f:
            f.seek(0)
            f.write(json.dumps(tweets))

        return original_data
