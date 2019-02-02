# Fortnite API


**Track your Fortnite stats, compare with your friends and see the charts**


# Live Preview
https://investir-xp.herokuapp.com/


# Overview

* Celery
* RabbitMQ
* Redis
* Whitenoise
* PostgreSQL
* Heroku


# Features
* Track your stats by searching for the username at the main form
* All requests are stored in the database as a `Communication` instance
* You can see at Django Admin all the requests history and contents
* When a user is searched, instances of Player and PlayerStatus are created
* All requests are made asynchronously for a better performance
* The project is ready to deploy at Heroku with WhiteNoise


# Installation

Postgres
--------

Install Postgres (if you already have Postgres, go to next step)

    $ sudo su -
    $ apt-get install postgresql postgresql-contrib
    $ update-rc.d postgresql enable
    $ service postgresql start
    

Create a Postgres Database

    $ sudo su postgres
    $ psql
    $ create database investir;
    

Redis
-----
Install Redis: [tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04)



Environment
--------

Install pipenv

    $ pip3 install pipenv
    
Create virtual environment and install dependencies

    $ pipenv install

Activate the environment

    $ pipenv shell
    
Copy the `env.sample` file to `.env` and change it with your data*

    $ cp env.sample .env

* You may request your TRN Api Key at: https://fortnitetracker.com/site-api

Automatically export all variables

    $ set -a
    $ source .env
    $ set +a

RabbitMQ
--------

    $ sudo apt-get install -y erlang
    $ sudo apt-get install rabbitmq-server


Project
-------
    
Clone this repository


    $ git clone https://github.com/Guilehm/investir-nao-da-xp.git
    

Enter project directory

    $ cd investir-nao-da-xp
    

Migrate the database

    $ python3 manage.py migrate

Load the fixtures

    $ python3 manage.py loaddata staging-fixtures.json

Install RabbitMQ

    $ sudo apt-get install rabbitmq-server
    
Start Celery

    $ celery -A xp worker -l info


    
And start the server

    $ python3 manage.py runserver

Enjoy :D
