# Blobber Buddy Chat

by Gigi, Joying, Megan and Reem :)

## Introduction

final project for mlh; in collaboration with other members of my pod 

## Description



## Visuals



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

## Technologies Used

- Python-Flask
- SocketIO
- HTML/CSS
- Postgres


## Usage
Start flask
```bash
$ flask run

```
- Setup ENV file: - Under app directory create a .env file - Include the following information for configuring your database and fill in with your information:

  -POSTGRES_USER=
  -POSTGRES_PASSWORD=
  -POSTGRES_HOST=
  -POSTGRES_DB=
  
Start a web browser and type in localhost:5000, page will render and can be intereact like any other webpage.

