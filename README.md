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

There is more documentation in [docs/README.md](under development).

# Contributing

We are sure it is full of issues, so don't hesitate on blaming us and submitting the ones you find!

Feel free to fork it and submit merge requests. We are sure it can be improved in many ways.

Thre is more information in the [CONTRIBUTING](CONTRIBUTING.md) file

# License

[GPL v3](LICENSE)

## Logo

Logo is based in a combination of [Bitergia](http://bitergia.com)'s owl logo and [Wizard's white hat](https://openclipart.org/detail/245968/wizards-white-hat) from [Thewizardplusplus](https://openclipart.org/user-detail/thewizardplusplus)
