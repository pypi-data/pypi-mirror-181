Django Group Extend
===================

Django group is a Django package to extend default django group.

Installable App
---------------

This app can be installed and used in your django project by:

.. code-block:: bash

    $ pip install django_group_extend


Edit your `settings.py` file to include `'django_group'` in the `INSTALLED_APPS`
listing.

.. code-block:: python

    INSTALLED_APPS = [
        ...

        "django_group",
    ]


Edit your project `urls.py` file to import the URLs:


.. code-block:: python

    url_patterns = [
        ...

        path('django_group/', include('django_group.urls')),
    ]


Finally, add the models to your database:


.. code-block:: bash

    $ ./manage.py makemigrations django_group


The "project" Branch
--------------------

The `master branch <https://github.com/riso-tech/django_group_extend/tree/master>`_ contains the final code for the PyPI package.


Docs & Source
-------------

* Source: https://github.com/riso-tech/django_group_extend
* PyPI: https://pypi.org/project/django_group_extend/


Publishing to PyPI
------------------

The following code builds the packages and invokes Twine:


.. code-block:: bash

    $ python -m pip install -U wheel twine setuptools
    $ python setup.py sdist
    $ python setup.py bdist_wheel
    $ twine upload dist/*
