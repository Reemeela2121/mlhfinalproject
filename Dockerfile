FROM python:3.8-slim-buster

RUN mkdir /mlhfinalproject
COPY requirements.txt /mlhfinalproject
WORKDIR /mlhfinalproject
RUN pip3 install -r requirements.txt

COPY . /mlhfinalproject

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["sh", "./entrypoint.sh"]