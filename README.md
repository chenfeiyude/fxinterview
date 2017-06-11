# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
MAC-OS
1. install python3.6 official release.
2. install django by pip for coding:
pip3.6 install Django
3. create a project with django:
python3.6 -m django startproject fxinterview
4. create virtual environment:
python3.6 -m venv /path/to/fxinterview/venv
5. start venv:
source venv/bin/activate
6. install django in evnv:
pip3.6 install django
7. install mysqlclient
(brew unlink mysql)
brew install mysql-connector-c
(brew unlink mysql-connector-c)
(brew link mysql)
pip3.6 install mysqlclient
8. migrate db
(create database fxinterview in your mysql)
python3.6 manage.py migrate
6. start server:
python3.6 manage.py runserver



* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact