# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
MAC-OS
1. install python3.6 official release
2. install django by pip for coding
3. create a project with django (Already done)
4. create virtual environment
5. start venv
6. install django in evnv
7. install mysqlclient
8. creating database fxinterview
9. migrate db
10. start server


* Configuration
1. install python3.6 official release.

2. install django by pip for coding:
pip3.6 install Django
doc at https://docs.djangoproject.com/en/1.11/intro/

3. create your own app with django (Already done):
python3.6 -m django startproject fxinterview
python3.6 manage.py startapp interviewer
python3.6 manage.py startapp interviewee

4. create virtual environment:
python3.6 -m venv /path/to/fxinterview/venv

5. start venv:
source venv/bin/activate

* Dependencies
1. install django in evnv:
pip3.6 install django

2. install mysqlclient
(brew unlink mysql)
brew install mysql-connector-c
(brew unlink mysql-connector-c)
(brew link mysql)
pip3.6 install mysqlclient


* Database configuration
1. create database fxinterview in your mysql

2. update settings.py DATABASES to configure your mysql (do not commit)

3. migrate db
python3.6 manage.py migrate
python3.6 manage.py makemigrations interviewer
python3.6 manage.py sqlmigrate interviewer 0001
python3.6 manage.py migrate (check states)  

* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact