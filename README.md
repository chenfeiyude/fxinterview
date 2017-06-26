# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
MAC-OS
1. install python3.6 official release<br />
2. install django by pip for coding<br />
3. create a project with django (Already done)<br />
4. create virtual environment<br />
5. start venv<br />
6. install django in evnv<br />
7. install mysqlclient<br />
8. creating database fxinterview<br />
9. migrate db<br />
10. start server<br />


* Configuration<br />
1. install python3.6 official release.<br />

2. install django by pip for coding:<br />
pip3.6 install Django<br />
doc at https://docs.djangoproject.com/en/1.11/intro/<br />

3. create your own app with django (Already done):<br />
python3.6 -m django startproject fxinterview<br />
python3.6 manage.py startapp interviewer<br />
python3.6 manage.py startapp interviewee<br />

4. create virtual environment:<br />
python3.6 -m venv /path/to/fxinterview/venv<br />

5. start venv:<br />
source venv/bin/activate<br />

* Dependencies
1. install django in evnv:<br />
pip3.6 install django<br />

2. install mysqlclient<br />
(brew unlink mysql)<br />
brew install mysql-connector-c<br />
(brew unlink mysql-connector-c)<br />
(brew link mysql)<br />
pip3.6 install mysqlclient<br />


* Database configuration<br />
1. create database fxinterview in your mysql<br />

2. update settings.py DATABASES to configure your mysql (do not commit)<br />

3. migrate db<br />
python3.6 manage.py migrate<br />
python3.6 manage.py makemigrations interviewer<br />
python3.6 manage.py sqlmigrate interviewer 0001<br />
python3.6 manage.py migrate (check states)<br />

* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact