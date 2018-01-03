=========================================
Stacklearn: Open Source Learning Platform
=========================================

Runs on Python 3.6 w/ dependencies listed in requirements.txt.

To run this project locally, clone the repo, download the project dependencies, and set up a superuser on your local machine via these steps:

Fork and clone the repo
~~~~~~~~~~~~~~~~~~~~~~~

Fork the project on GitHub and git clone your fork, e.g.:

SSH

    git clone <username>@github.com:<username>/stacklearn-clone.git
    
HTTPS

    git clone https://github.com/<username>/stacklearn-clone.git


Start a `virtualenv`
~~~~~~~~~~~~~~~~~~~~

	$ cd stacklearn-clone
    $ virtualenv -p /path/to/python3 oenv
    $ . oenv/bin/activate

Install dependencies
~~~~~~~~~~~~~~~~~~~~

The project dependencies listed in requirements.txt can be installed with pip:

	(oenv) $ pip install --upgrade pip
    (oenv) $ pip install -r requirements.txt

Set environment variables for testing

    $ export DJANGO_DEBUG=1
    $ export DJANGO_ENABLE_SSL=0

Setup the database and run locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run migrations:

	(oenv) $ python manage.py migrate

Create a Django admin user:

    (oenv) $ python manage.py createsuperuser

Run the server:

    (oenv) $ python manage.py runserver

View the data models from any browser:

	http://127.0.0.1:8000/admin/
