[![Build Status](https://travis-ci.org/andela-andrewmakenzi/flask-bucketlist.svg?branch=develop&u=1)](https://travis-ci.org/andela-andrewmakenzi/flask-bucketlist)
[![Code Climate](https://codeclimate.com/github/andela-andrewmakenzi/flask-bucketlist/badges/gpa.svg)](https://codeclimate.com/github/andela-andrewmakenzi/flask-bucketlist)
[![license](https://img.shields.io/github/license/andela-andrewmakenzi/flask-bucketlist.svg)]()
## Introduction
Flask API

#### URL endpoints

| URL Endpoint | HTTP Methods | Summary |
| -------- | ------------- | --------- |
| `/api/v1/auth/register/` | `POST`  | Register a new user|
|  `/api/v1/auth/login/` | `POST` | Login and retrieve token|
| `/api/v1/bucketlists/` | `POST` | Create a new Bucketlist |
| `/api/v1/bucketlists/` | `GET` | Retrieve all bucketlists for user |
| `/api/v1/bucketlists/?limit=2&page=1` | `GET` | Retrieve one bucketlist per page |
| `/api/v1/bucketlists/<id>/` | `GET` |  Retrieve bucket list details |
| `/api/v1/bucketlists/<id>/` | `PUT` | Update bucket list details |
| `/api/v1/bucketlists/<id>/` | `DELETE` | Delete a bucket list |
| `/api/v1/bucketlists/<id>/items/` | `POST` |  Create items in a bucket list |
| `/api/v1/bucketlists/<id>/items/<item_id>/` | `DELETE`| Delete a item in a bucket list|
| `/api/v1/bucketlists/<id>/items/<item_id>/` | `PUT`| update a bucket list item details|

## Installation

Flask API has been developed and tested on Python 3. The recommended
version is Python 3.5.2. Using your package manager or binaries from the
official [Python language website](https://www.python.org/downloads/),
install Python 3 first.

Follow the following steps to have the system running:

* ####Clone this repo:
 - Using HTTPS:
 ```
 git clone https://github.com/andela-andrewmakenzi/flaskbucketlist.git
 ```
 - Using SSH:
 ```
 git clone git@github.com:andela-andrewmakenzi/flaskbucketlist.git
 ```

* Navigate to the application directory:

```
cd flaskbucketlist
```

* Create a virtual environment to install the
application in. You could install virtualenv and virtualenvwrapper.
Within your virtual environment, install the application package dependencies with:

```
pip install -r requirements.txt
```

* Run the application with:

```
python run.py
```

## Using the API
