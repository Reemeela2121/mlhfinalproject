
# Blobber Buddy Chat

by Gigi, Joying, Megan and Reem :)
Pod 335

## Introduction

We live in a pandemic world where social distancing and germaphobia is the new social norm. 
Finding friends is becoming more difficult and strangers are becoming stranger! Fear not! Blobber's got your
back. Blobber will find friends for you so you'll have a friend to talk to anywhere, anytime.

## Description

Our group worked on a webapp that would allow people to meetup and chat based on 
similiar interests. A user would join our service, answer a few questions and be
paired with someone who have similiar interests. We used socketio for the chatroom; 
HTML/CSS for the design; Postgres for our backend database; Flask for our web
framework; Nginx to reverse proxy; Created a blobber.tech domain. Contained our
application and use cAdvisor for monitoring. Used google reCaptcha to help with
replay attacks. 

## Visuals



## Technologies Used

- Python-Flask
- HTML / CSS
- SocketIO
- HTML/CSS
- Postgres
- NGINX
- cAdvisor
- Docker containers
- reCaptcha
- Github Actions
- Hosted on .tech domain


## Installation

Make sure you have python3 and pip installed

Create and activate virtual environment using virtualenv

```bash
$ python -m venv python3-virtualenv
$ source python3-virtualenv/bin/activate
```

## Pre-requisites / requirements

- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies

```bash
pip install -r requirements.txt

```

- **NOTE** Due to a known [issue](https://github.com/miguelgrinberg/Flask-SocketIO/issues/801) in SocketIO, the app may only be run in **production** mode


## Usage

Start flask

```bash
$ flask run

```

- Setup ENV file: 
  - create a .env file 
  - Include the following information to configure your database and fill in with your information:

    - POSTGRES_USER=
    - POSTGRES_PASSWORD=
    - POSTGRES_HOST=
    - POSTGRES_DB=
  
Start a web browser and type in localhost:5000, page will render and can be intereact like any other webpage.

