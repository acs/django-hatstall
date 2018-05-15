# Hatstall

Hatstall is a web interface for [SortingHat](http://github.com/grimoirelab/sortinghat) databases developed mainly with [Django](https://www.djangoproject.com/)

## What does it try to solve?

Dealing with contributors multi-identities in a development community is an issue in order to get the right metrics about their contributions in the whole project. For example:
* they might be using several usernames in the same data source (i.e. different emails for git commits)
* to get a whole view, you need to take into account their contribution in different data sources (git, issues, chats, etc.). You need to merge multiple usernames under a single unique identity
* they might be working for several organizations during project life

[SortingHat](http://github.com/grimoirelab/sortinghat) is the [GrimoireLab](https://grimoirelab.github.io) tool to deal with all that stuff, but it's CLI might not be very intuitive. So, the learning curve is high, and it takes a long time for a non-tech user to give the right  information to the right identity.

So, Hatstall tries to make easier to deal with multi-identities management in development communities.

## Why Hatstall as a name?

According to [Harry Potter Wiki](http://harrypotter.wikia.com/wiki/Hatstall) **Hatstall** is defined as:

> A Hatstall was an archaic term for a student of Hogwarts School of Witchcraft and Wizardry whose sorting took more than five minutes because the Sorting Hat found them to have a personality equally suited to different Hogwarts Houses. The Sorting Hat sometimes took the student's personal preference into consideration in order to break such a tie.

## Installation

Clone the repository and install, or check you already have, the requirements defined in the [requirements.txt](requirements.txt) file. They are mostly:

* Django
* grimoire-elk
* grimoirelab-toolkit
* sortinghat

## Usage

Once you have the requirements installed (I recommend using a Python virtual environment) you can launch the web app using the command line:

```
django-hatstall/django_hatstall $ python3 manage.py migrate
django-hatstall/django_hatstall $ python3 manage.py runserver
```

There is more documentation [under development](docs/README.md).

## Docker
This image is designed to be run next to a sortinghat database.

## Configuration
They are two ways to configure and use this image, either by bind mounting a configuration files or by 
using environment variables, the second option is the easiest one.

### Environment
#### HATSTALL_ADMIN_USER
Admin user used to access the default interface. Default set to 'admin'

#### HATSTALL_ADMIN_MAIL
Admin email used by admin user. Default set to admin@example.com

#### HATSTALL_ADMIN_PASS admin
Admin password used by admin user. Default set to admin

#### HATSTALL_ALLOWED_HOST
Allowed host to access the user interface. Default set to [*]

Example: '[localhost,127.0.0.1]

#### HATSTALL_DATABASE
Sqlite3 database used by hatstall
! This is not the sortinghat database.

#### HATSTALL_DEBUG
Hatstall debug mode enable. Default set to false

#### SHDB_USER
Sortinghat database username. Default set to sortinghat

__! This setting is not taken into account if shdb.cfg is present__

#### SHDB_PASSWORD
Sortinghat database password. Default set to password

__! This setting is not taken into account if shdb.cfg is present__

#### SHDB_NAME
Sortinghat database name. Default set to sortinghat

__! This setting is not taken into account if shdb.cfg is present__

#### SHDB_HOST
Sortinghat database hostname. default set to sortinghatdb

__! This setting is not taken into account if shdb.cfg is present__


### File
#### Shdb
Mount shdb.cfg at /var/www/django-hatstall/shdb.cfg with following content
```
[SHDB_Settings]
use=root
password=password
name=hatstall_sh
host=localhost
```

#### HTTP/HTTPS
By default this image only listen on port 80.
In order to use HTTPS, you must handle it by yourself with following informations:
* Mount ssl files at the place defined in you apache conf file
* Override '/etc/apache2/sites-available/000-default.conf'
* Override '/etc/apache2/sites-enabled/000-default.conf'

#### Sqlite3
The sqlite3 database is located at /var/www/hatstall.sqlite3

### Demo

```
docker run \
  -i -t --rm \
  -p 80:80 \
  --name hatstall \
  -e "HATSTALL_DEBUG=True" \
  -e "HATSTALL_ALLOWED_HOST=['*']" \
  -e "SHDB_USER=sortinghat" \
  -e "SHDB_PASSWORD=password" \
  -e "SHDB_NAME=sortinghat" \
  -e "SHDB_HOST=sortinghatdb" \
  grimoirelab/hatstall:latest \

```

# Contributing

We are sure it is full of issues, so don't hesitate on blaming us and submitting the ones you find!

Feel free to fork it and submit merge requests. We are sure it can be improved in many ways.

Thre is more information in the [CONTRIBUTING](CONTRIBUTING.md) file

# License

[GPL v3](LICENSE)

## Logo

Logo is based in a combination of [Bitergia](http://bitergia.com)'s owl logo and [Wizard's white hat](https://openclipart.org/detail/245968/wizards-white-hat) from [Thewizardplusplus](https://openclipart.org/user-detail/thewizardplusplus), but we are working on a new one
