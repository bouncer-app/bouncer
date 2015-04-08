bouncer
=======

Simple Declarative Authentication DSL inspired by Ryan Bates’ excellent
cancan library

.. image:: https://travis-ci.org/jtushman/bouncer.svg?branch=master
    :alt: travis-badge
    :target: https://travis-ci.org/bouncer-app/bouncer

Introduction
------------

Meet **bouncer**.

**bouncer** is your faithful servant. Big, burly, trustworthy – smarter
than he looks, but very effective in what he does. You just have to talk
simply to him. For example:

.. code:: python

    from bouncer import authorization_method
    from bouncer.constants import *

    @authorization_method
    def authorize(user, they):

        if user.is_admin:
            they.can(MANAGE, ALL)
        else:
            they.can(READ, ALL)
            they.cannot(READ, 'TopSecretDocs')

            def if_author(article):
                return article.author == user

            they.can(EDIT, 'Article', if_author)


And once you have that setup, you can ask questions like:

.. code:: python

    jonathan = User(name='jonathan',admin=False)
    marc = User(name='marc',admin=False)

    article = Article(author=jonathan)

    print can(jonathan, EDIT, article)   # True
    print can(marc, EDIT, article)       # False

    # Can Marc view articles in general?
    print can(marc, VIEW, Article)       # True

Installation
------------

``pip install bouncer``

Defining Abilities
------------------

@authorization_method
~~~~~~~~~~~~~~~~~~~~~
User permissions are defined in a method decorated with
``@authorize_method``

A simple setup looks like so …

.. code:: python

    @authorization_method
    def authorize(user, they):

        if user.is_admin:
            they.can(MANAGE, ALL)
        else:
            they.can(READ, ALL)

            def if_author(article):
                return article.author == user

            they.can(EDIT, Article, if_author)


If you do not think the “they.can” is pythonic enough you can use the ``append`` syntax

.. code:: python

    @authorization_method
    def authorize(user, abilities):

        if user.is_admin:
            abilities.append(MANAGE, ALL)
        else:
            abilities.append(READ, ALL)

            # See I am using a string here
            abilities.append(EDIT, 'Article', author=user)
            
Alternative syntax
~~~~~~~~~~~~~~~~~~

``dict`` syntax
^^^^^^^^^^^^^^^
You can also use an alternative ``dict`` syntax. The following is equivalent to above:

.. code:: python

    @authorization_method
    def authorize(user, they):

        if user.is_admin:
            they.can(MANAGE, ALL)
        else:
            they.can(READ, ALL)
            they.can(EDIT, Article, author=user)

You can add multiple conditions to the ``dict``:

.. code:: python

    they.can(READ, Article, published=True, active=True)

Strings instead of classes
^^^^^^^^^^^^^^^^^^^^^^^^^^
You can use strings instead of classes. This means you do not need to import a bunch of files you are not using in initialization

.. code:: python

    @authorization_method
    def authorize(user, they):

        if user.is_admin:
            they.can(MANAGE, ALL)
        else:
            they.can(READ, ALL)

            # Notice that I am using a string here
            they.can(EDIT, 'Article', author=user)


Combining Rules
^^^^^^^^^^^^^^^
You can (are encouraged to) combine similar rules on a single line:

.. code:: python

    they.can((EDIT,READ,DELETE),(Article,Photo))
    
Combining Abilities
^^^^^^^^^^^^^^^^^^^

It is possible to define multiple abilites for the same resource. This is
particularly useful in combination with the ``cannot`` method

.. code:: python

    they.can(MANAGE, ALL)
    then.cannot(DELETE, ('USER', 'ACCOUNT'))

Checking Abilities
------------------
There are two main ways for checking for authorization.  ``can`` (and its brother ``cannot``) and ``ensure``

* ``can`` returns a boolean
* ``ensure`` will raise an ``AccessDenied`` Exception

.. code:: python

    from bouncer import can, ensure
    from bouncer.constants import *

    jonathan = User(name='jonathan',admin=False)

    # can jonathan edit articles in general
    can(jonathan, EDIT, Article)

    # ensure jonathan edit articles in general -- otherwise we are going to throw an exception
    ensure(jonathan, EDIT, Article)

    article = Article(author=jonathan)

    # can jonathan delete this specific article
    can(jonathan, EDIT, article)
    
Decorating your User Model
~~~~~~~~~~~~~~~~~~~~~~~~~~
Optionally, you can add helper methods into your User model by using ``@authorization_target``

For example:

.. code:: python

    from bouncer import authorization_target

    @authorization_target
    class User(object):

        def __init__(self, **kwargs):
            self.id = kwargs.get('id', 1)
            self.name = kwargs.get('name', '')
            self.admin = kwargs.get('admin', False)
            pass
    
        @property
        def is_admin(self):
            return self.admin
    
    jonathan = User(name='jonathan',admin=False)
    marc = User(name='marc',admin=False)

    article = Article(author=jonathan)

    print jonathan.can(EDIT,article)   # True
    print marc.can(EDIT,article)       # False

Flask
-----

If you use Flask, I am currently working on a Flask extension – follow
its progress here: `flask-bouncer`_.

Questions / Issues
------------------

Feel free to ping me on twitter: `@tushman`_
or add issues or PRs at https://github.com/jtushman/bouncer
    
.. _flask-bouncer: https://github.com/jtushman/flask-bouncer
.. _@tushman: http://twitter.com/tushman
