# social_networking_application

# Django Project

This is a Django project containerized with Docker.

## Features

- Django 4.x
- Dockerized for easy setup and deployment
- SQLite as the database

## Prerequisites

- Docker installed on your system

## Installation

Clone the repository:

you can clone with SSH

git clone git@github.com:Rohitghule131/social_networking_application.git

or HTTPS

git clone https://github.com/Rohitghule131/social_networking_application.git

cd ./social_networking_application

## Docker Setup

1. Build Docker Image
To build the Docker image for your Django project, run the following command:

docker build -t social_networking_application .

2. Run Docker Container
To run the Docker container, use the following command:

docker run -d -p 8000:8000 social_networking_application

This will start your Django project and make it accessible at http://localhost:8000.

Here is the postman collection for endpoints.

https://dark-zodiac-787425.postman.co/workspace/social_networking~935a3972-35d5-40c0-bc61-afa861fd55c8/collection/21390973-b6b75cf6-f283-478b-a2ad-e29fa3544482?action=share&creator=21390973

Here is the DB diagram of the project.

https://www.dbdiagram.io/d/Social-Networking-665ca752b65d9338794ba112


