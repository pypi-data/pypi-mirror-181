arnavArithmetic
=====

arnavArithmetic is a lightweight `WSGI`_ Math application. It is designed
to make getting started quick and easy, with the ability to scale up to
complex applications. It began as a simple wrapper around `Werkzeug`_
and `Jinja`_ and has become one of the most popular Python web
application frameworks.

.. _WSGI: https://wsgi.readthedocs.io/
.. _Werkzeug: https://werkzeug.palletsprojects.com/
.. _Jinja: https://jinja.palletsprojects.com/

Installing
----------
Install and update using `pip`_:

.. code-block:: text

    $ pip install arnavArithmetic

.. _pip: https://pip.pypa.io/en/stable/getting-started/

A Simple Example
----------------
.. code-block:: python

    # save this as app.py
    from arnavArithmetic import add

    app = add(1,3)
    print(app)
