# Item Catalog Project

This application provides a list of categories and items.  Users can register to be able to add, modify and delete items and categories.  Non registered users will be able to view categories and items.
Items and Categories can also be retrieved via a JSON API.

## Table of contents

- [How to run](#how-to-run)
- [Features](#features)
- [Extras](#extras)
- [References](#references)

## How to run

* Install [Vagrant](http://vagrantup.com) and [VirtualBox](https://www.virtualbox.org)
* Clone this [repository](https://github.com/younessassassi/fullstack-nanodegree-catalog)
* Launch the Vagrant VM
* login to the linux box and cd to the tournament folder

```sh
$ vagrant up
$ vagrant ssh
$ cd path/to/project/folder
```

### Google Client ID & Secret

As the app uses Google for authentication, the next step you have to obtain a client id and client secret from Google:

1. Go to the [Google Developer Console](https://console.developers.google.com/project).
2. Create a new project.
3. Get the App ID & App Secret
4. Copy the client id and client secret and replace the GOOGLE_LOGIN_CLIENT_ID and GOOGLE_LOGIN_CLIENT_SECRET in config.py file located in catalog/catolog/config.py

### Facebook Client ID & Secret

As the app uses also Facebook for authentication, the next step you have to obtain a client id and client secret from Facebook:

1. Go to the [Facebook Developer](https://developers.facebook.com/apps/).
2. Create a new app (www - website).
3. Get the App ID & App Secret
4. Copy the client id and client secret and replace the FACEBOOK_LOGIN_CLIENT_ID and FACEBOOK_LOGIN_CLIENT_SECRET in config.py file located in catalog/catolog/config.py

### Install the project dependencies

```sh
$ pip install -r requirements.txt
```

### Initialize the database

```sh
$ python manage.py db init
$ python manage.py db upgrade
```

### Run the Application

```sh
$ python manage.py runserver
```

### Shutdown Vagrant machine

```sh
$ vagrant halt
```

### Destroy the Vagrant machine

```sh
$ vagrant destroy
```

## Features

- JSON API endpoints:
        - /categories/all/json
        - /items/all/json
        - /items/<int:item_id>/json


## Extras

### Easily find and run the project within the virtul environment
1. login to the linux box

```sh
$ vagrant up
$ vagrant ssh
$ sudo pip install virtualenvwrapper
$ cd ~
$ nano .profile
```

2.  Add the following to the .profile

```sh
# Virtualenvwrapper setup
export PROJECT_HOME=$HOME/path/to/project/directory
source /usr/local/bin/virtualenvwrapper.sh
```

3. Save and close the file
4. Navigate to the project directory

```sh
$ cd path/to/project/folder
$ mkvirtualenv 'project-name'
$ setvirtualenvproject
```
5. Now from any project or directory in the linux you can jump to your project workspace by typing:

```sh
$ workon 'project-name'
```

6. when you are done deactivate the project by typing:

```sh
$ deactivate
```

### DB management and setup

```sh
$ python manage.py db init                  #initialize migration files
$ python manage.py db migrate -m "initial"  #initialize database with a title
$ python manage.py db upgrade               #create tables
$ python manage.py db migrate -m "tags"     #for sample db migration when a db change is introduced
$ python manage.py db upgrade               #to run the migration
```

### Debug the project

1. Insert these lines which act as a breakpoint in your code:

```sh
import pdb
pdb.set_trace()
```

2. Run the application until it hits the breakpoint
3. Use these commands in the python console

```sh
'l' #to list the context of breakpoint
'c' #to continue
'n' #to move forward
's' #to step into
'r' #run until the current function returns
'h' #for help
'q' #for quit
'w' #to print the call stack
'b' #filename:line number
```

### Testing
1- nosetests will detect and run the available tests within the project.  A temporary database will be created and destroyed in the process which will not impact the dev and prod databses

```sh
nosetests
```

### Environment change
1- to switch between, dev, test and prod type the following:

```sh
$ export CATALOG_ENV=dev   # for the dev environment
$ export CATALOG_ENV=test  # for the test environment
$ export CATALOG_ENV=prod  # for the prod environment
```

## References
- [Pluralsight Flask course](http://www.pluralsight.com/courses/flask-micro-framework-introduction)
- [OAuth Authentication with Flask blog](http://blog.miguelgrinberg.com/post/oauth-authentication-with-flask)