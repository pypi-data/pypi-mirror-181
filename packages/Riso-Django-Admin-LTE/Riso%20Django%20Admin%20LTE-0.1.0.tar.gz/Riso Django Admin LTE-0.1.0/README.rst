Django Admin LTE
================

Behold My Awesome Package!

Installable App
---------------

This app can be installed and used in your django project by:

.. code-block:: bash

    $ pip install django_admin_lte


Edit your `settings.py` file to include `'django_admin'` in the `INSTALLED_APPS`
listing.

.. code-block:: python

    INSTALLED_APPS = [
        ...

        "django_admin",
    ]


Edit your project `urls.py` file to import the URLs:


.. code-block:: python

    url_patterns = [
        ...

        path('django_admin/', include('django_admin.urls')),
    ]


Finally, add the models to your database:


.. code-block:: bash

    $ ./manage.py makemigrations django_admin


The "project" Branch
--------------------

The `master branch <https://github.com/riso-tech/django_admin_lte/tree/master>`_ contains the final code for the PyPI package.


Docs & Source
-------------

* Source: https://github.com/riso-tech/django_admin_lte
* PyPI: https://pypi.org/project/django_admin_lte/


Publishing to PyPI
------------------

The following code builds the packages and invokes Twine:


.. code-block:: bash

    $ python -m pip install -U wheel twine setuptools
    $ python setup.py sdist
    $ python setup.py bdist_wheel
    $ twine upload dist/*
