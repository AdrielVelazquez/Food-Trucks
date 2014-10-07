Food-Trucks
===========

San Francisco Food Trucks

Description
===========
This application is a website dedicated to getting a listing of San Francisco Food Trucks
https://github.com/AdrielVelazquez/Food-Trucks

System Dependencies
===================
Some Common System dependencies are the following

Python 2.7.3 (available via apt in debian "wheezy") or 2.7.5+ (in ubuntu 13.10)
wget 1.13+ (older versions could not connect to PyPi via HTTPS)
pip 1.1 (available via apt in debian wheezy as python-pip)
git
libbz2-dev
libffi-dev
libicu-dev
libjpeg-dev
libpython-dev

Includes
========
- app directory (models, Views, routes)
- ingestion script
- connection script
- MakeFile
- Requirements
- Config
- Run script


Setup
=====
After cloning the repo:
https://github.com/AdrielVelazquez/Food-Trucks
The setup is easy, from the root directory

Activates virtualenv, installs dependencies located in requirements.txt, and populates local database with data
"make install"

Tests the different unit tests
"make test"

to run the application locally,
". ./bin/activate"
"python run.py"




