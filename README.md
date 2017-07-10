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
$ pip3.6 install Django  
doc at https://docs.djangoproject.com/en/1.11/intro/  

3. create your own app with django (Already done):  
$ python3.6 -m django startproject fxinterview  
$ python3.6 manage.py startapp main  

4. create your local_settings.py based on local_settings_template.py  

5. create virtual environment:  
$ python3.6 -m venv /path/to/fxinterview/venv  

6. start venv:  
$ source venv/bin/activate  

7. install requirement libs  
$ pip3.6 install -r ./requirements.txt

* Dependencies  
1. install django in evnv:    
$ pip3.6 install django  

2. install mysqlclient  
($ brew unlink mysql)  
$ brew install mysql-connector-c  
($ brew unlink mysql-connector-c)  
($ brew link mysql)  
$ pip3.6 install mysqlclient  


* Database configuration  
1. create database fxinterview in your mysql  

2. update settings.py DATABASES to configure your mysql (do not commit)  

3. migrate db  
$ python3.6 manage.py migrate  
$ python3.6 manage.py makemigrations main  
$ python3.6 manage.py sqlmigrate main 0001  
$ python3.6 manage.py migrate (check states)

4. insert default data  
 1). Create your own admin user, and test staff user  
 2). Load test fake data:  
     $ python3.6 manage.py loaddata main/default_insert_data.json   

* How to run tests
1. Run testing with command:  
$ coverage run manage.py test project_name  
e.g. 
$ coverage run manage.py test main  
or running full test:  
$ coverage run manage.py test

2. Build your test report  
$ coverage html  

3. View your test report  
$ open ./htmlcov/index.html   

* Deployment instructions

### Contribution guidelines ###

* Writing tests  
Every new functionality should has a related test. 

1. Add your test case class into project_name/tests/test_xxx.py 

2. Every test case should contain description for showing what are you testing

3. Test case class name should be ClassNameTestCase, and test case name should be test_function_name  
e.g. CompanyModelTestCase

* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact