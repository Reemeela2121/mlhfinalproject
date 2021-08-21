
# Blobber Buddy Chat

by Gigi, Joying, Megan and Reem :)
Pod 335

## Introduction

We live in a pandemic world where social distancing and germaphobia is the new social norm. 
Finding friends is becoming more difficult and strangers are becoming stranger! Fear not! Blobber's got your
back. Blobber will find friends for you so you'll have a friend to talk to anywhere, anytime online.

## Description

Our group worked on a webapp that would allow people to meetup and chat. A user 
would register to our service, and then sign-in, and join an exciting room. 

 - We used socketio for the chatroom
 - HTML / CSS for front-end design
 - Postgres for our backend database
 - Flask for our web framework
 - Nginx to reverse proxy to connect Flask
 - Created a blobber.tech domain
 - Contained our webapp, nginx and database for security and efficiency 
 - Use cAdvisor, Prometheus and grafana for monitoring containers in real time
 - Created a custom CI/CD pipeline with Github Actions for testing, linting
 - Deployed on AWS with domain name and ip blocking
 - Use google reCaptcha to help with replay attempts

## Visuals 
**updated 8/17/2021
Home Page
![image](https://user-images.githubusercontent.com/51943194/129788201-1c9a24f1-0858-41b9-90f2-3e756d9742a4.png)

Login
![image](https://user-images.githubusercontent.com/51943194/129788442-ed820c5a-6b32-4534-8303-1caa0fa3c3fc.png)

Dashboard
![image](https://user-images.githubusercontent.com/51943194/130191874-1df00dac-3d96-4c46-8b3d-c671d891fd21.png)

Chatroom
![image](https://user-images.githubusercontent.com/51943194/130191949-d2607105-4fb7-4ec1-a870-1e22b7c974bd.png)

AWS Instance from t2.micro -> t2.small
![image](https://user-images.githubusercontent.com/51943194/129834519-62245360-8a78-41d4-ab93-f157b526c64a.png)

cAdvisor
![image](https://user-images.githubusercontent.com/51943194/129844313-bb41c80f-efe4-40aa-9d65-96e25883c0e8.png)

Prometheus
![image](https://user-images.githubusercontent.com/51943194/129845143-29dfd02d-ab18-4919-a76d-98f7bb9f7bb8.png)

Grafana Dashboard
![image](https://user-images.githubusercontent.com/51943194/130197840-aef1d1a3-7a4d-4646-ad5e-f7e9ea91694f.png)

Grafana Dashboard 2
![image](https://user-images.githubusercontent.com/51943194/130197947-33246c0d-9728-4969-b621-95129d360caa.png)

Containers
![image](https://user-images.githubusercontent.com/51943194/130271390-65ecb374-384c-4409-a9f0-9f442e83eb32.png)

Discord Webhook
![image](https://user-images.githubusercontent.com/51943194/130304013-a84b42fc-8934-47c3-964a-2795fe9bcf0c.png)




## Technologies Used

- Python-Flask
- HTML / CSS
- SocketIO
- Postgres
- NGINX
- cAdvisor
- Prometheus
- Docker containers
- reCaptcha
- Github Actions (CI/CD)
- AWS instance
- Hosted on .tech domain
- IP blocking, domain name only


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

