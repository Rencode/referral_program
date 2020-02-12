# Referral Program
A proof of concept API to manage a referral program

![Python application](https://github.com/Rencode/referral_program/workflows/Python%20application/badge.svg)

## Overview
The service allows users to sign up for an account and once signed up they can create a referral, which is a UUID. 
A referral can then be used by a new user to sign up. If the new user signs up using the referral token their balance is 
credited with $10. For every 5 people that a user refers their account is credited with an additional $10.

## Endpoints
The endpoints provided are as follows:
* ``POST /user/`` Create new user
* ``GET /user/{id}`` Get user
* ``POST /user/{id}/referral`` Create a new referral

### Create User
Create a new user.

**URL** : `/user/`

**Method** : `POST`

**Parameters**
* email - The new user's email address
* referral(**optional**) - A referral provided by an existing user

## Success Response

**Code** : `200 OK`

**Example**

``POST /user?email=barbie@gmail.com&referral=9a299020-6ddb-4bf4-8fdd-4989337d8e82``

```json
{
    "id": 1234
}
```

### Get User
Retrieve the information for an existing user.

**URL** : `/user/{user_id}`

**Method** : `GET`

**Parameters**
* user_id - The user id

## Success Response

**Code** : `200 OK`

**Example**

``GET /user/12``

```json
{
    "id": "49",
    "email": "somerandom@email.com",
    "referral": "9a299020-6ddb-4bf4-8fdd-4989337d8e82",
    "balance": "10.0",
    "total_referrals": "0"
}
```

### Get User
Retrieve the information for an existing user.

**URL** : `/user/{user_id}`

**Method** : `GET`

**Parameters**
* user_id - The user id

## Success Response

**Code** : `200 OK`

**Example**

``GET /user/12``

```json
{
    "id": "49",
    "email": "somerandom@email.com",
    "referral": "9a299020-6ddb-4bf4-8fdd-4989337d8e82",
    "balance": "10.0",
    "total_referrals": "0"
}
```

### Create Referral
Create a referral for the given user

**URL** : `/user/{user_id}/referral`

**Method** : `POST`

**Parameters**
* user_id - The user id

## Success Response

**Code** : `200 OK`

**Example**

``POST /user/12/referral``

```json
{
    "referral": "9a299020-6ddb-4bf4-8fdd-4989337d8e82"
}
```

## Running Locally

The service requires Postgres and the ``sqlalchemy.url`` value should be set to your Postgres instance.

First off lets create a virtual environment 
```
virtualenv venv
```
And activate it
```
source ./venv/bin/activate
``` 
Now we install the dependencies
```
pip install -e .
```
Install the dev dependencies
```
pip install -e ".[dev]"
```
Run the unit tests
```
pytest tests
```
Finally we can run the web server
```
pserve development.ini --reload
```
