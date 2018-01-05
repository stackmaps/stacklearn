=========================================
Stacklearn: Open Source Learning Platform
=========================================

Runs on Python 3.6 w/ dependencies listed in requirements.txt.

To run this project locally, clone the repo, download the project dependencies, and set up a superuser on your local machine via these steps:

Fork and clone the repo
~~~~~~~~~~~~~~~~~~~~~~~

Fork the project on GitHub and git clone your fork, e.g.:

SSH::

    git clone <username>@github.com:<username>/stacklearn-clone.git

HTTPS::

    git clone https://github.com/<username>/stacklearn-clone.git


Start a `virtualenv`
~~~~~~~~~~~~~~~~~~~~

Replace `/path/to/python3` with the appropriate filepath::

    $ cd stacklearn-clone
    $ virtualenv -p /path/to/python3 oenv
    $ . oenv/bin/activate

Install dependencies
~~~~~~~~~~~~~~~~~~~~

The project dependencies listed in requirements.txt can be installed with pip::

    (oenv) $ pip install --upgrade pip
    (oenv) $ pip install -r requirements.txt

Set environment variables for testing::

    $ export DJANGO_DEBUG=1
    $ export DJANGO_ENABLE_SSL=0

Setup the database and run locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run migrations::

    (oenv) $ python manage.py migrate

Create a Django admin user::

    (oenv) $ python manage.py createsuperuser

Run the server::

    (oenv) $ python manage.py runserver

View the data models from any browser::

..    http://127.0.0.1:8000/admin/

Make changes and run tests
~~~~~~~~~~~~~~~~~~~~~~~~~~

To run the test suite::

    (oenv) $ python manage.py test --keepdb

Add your own feature and submit a Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Keep your commit history clean and merge process simple by following these steps before starting on any new feature::

Once time only, add this repo as a remote to your fork, e.g.::

SSH::
    git remote add upstream git@github.com:stackmaps/stacklearn.git

HTTPS::
    git remote add upstream https://github.com/stackmaps/stacklearn.git

Anytime a PR is merged or changes are pushed (or you're starting this process for the first time), you should run::

    git checkout dev
    git pull upstream dev

in order to make sure you are working with an up-to-date copy of the `dev` branch.

Once you have the most recent `dev` code, create a new branch (off of `dev`) for your new feature.

    git checkout -b my-feature

Now you can run `git branch` and should see an output like this:

    $ git branch
      dev
      master
    * my-feature


Pick an issue (or create a new one) which your new feature will address.

Proceed with writing code.  Commit frequently!  Focus on writing very clear, concise commit statements and plentiful comments.  If you have poor comments or zero tests, your PR will not be merged.

If you are aware of changes in the branch you forked from, rebase your branch from that changing branch (in our case that is `dev`) By running:

    git rebase dev

Then resolve all merge conflicts and update dependencies like this:

    pip install -r requirements
    python manage.py migrate
    python manage.py test

When your branch is ready (e.g., has comments and tests), submit a Pull Request!

IMPORTANT: WHEN YOUR PR IS ACCEPTED, stop using your branch right away (or delete it altogether).  New features (or enhanced versions of your existing feature) should be created on brand new branches (after pulling in all the fresh changes from `dev`).
