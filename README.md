bouncer
========

Simple Declarative Authentication DSL inspired by Ryan Bates' excellent cancan library

[![Build Status](https://travis-ci.org/jtushman/bouncer.svg)](https://travis-ci.org/jtushman/bouncer)

## Introduction

Meet **bouncer**.

**bouncer** is your faithful servant.  Big, burly, trustworthy -- smarter than he looks,
but very effective in what he does.  You just have to talk simply to him.  For example:

```python
from bouncer import authorization_method
from bouncer.constants import *

@authorization_method
def authorize(user, they):

    if user.is_admin:
        they.can(MANAGE, ALL)
    else:
        they.can(READ, ALL)

        def if_author(article):
            return article.author == user

        they.can(EDIT, 'Article', if_author)
```

And once you have that setup, you can ask questions like:

```python
jonathan = User(name='jonathan',admin=False)
marc = User(name='marc',admin=False)

article = Article(author=jonathan)

print jonathan.can(EDIT, article)   # True
print marc.can(EDIT, article)       # False

# Can Marc view articles in general?
print marc.can(VIEW, Article)       # True
    
```


## Installation

`pip install bouncer`

## 1. Defining Abilities

User permissions are defined in an method decorated with `@authorize_method`

A simple setup looks like so ...

```python
@authorization_method
def authorize(user, they):

    if user.is_admin:
        they.can(MANAGE, ALL)
    else:
        they.can(READ, ALL)

        def if_author(article):
            return article.author == user

        they.can(EDIT, Article, if_author)
```

### Alternative syntax

#### You can also use an alternative `dict` syntax.  The following is equivalent to above:

```python
@authorization_method
def authorize(user, they):

    if user.is_admin:
        they.can(MANAGE, ALL)
    else:
        they.can(READ, ALL)
        they.can(EDIT, Article, author=user)
```

#### You can add multiple conditions to the `dict`:

```python
they.can(READ, Article, published=True, active=True)
```

#### Use can use Strings instead of classes (so you do not need to import a bunch of files you are not using in initialization

```python
@authorization_method
def authorize(user, they):

    if user.is_admin:
        they.can(MANAGE, ALL)
    else:
        they.can(READ, ALL)

        # Notice that I am using a string here
        they.can(EDIT, 'Article', author=user)
```

#### If you do not think the "they.can" is pythonic enough you can use the append syntax

```python
@authorization_method
def authorize(user, abilities):

    if user.is_admin:
        abilities.append(MANAGE, ALL)
    else:
        abilities.append(READ, ALL)

        # See I am using a string here
        abilities.append(EDIT, 'Article', author=user)
```

#### You can (are encouraged to) combine similar rules on a single line:

```python
they.can((EDIT,READ,DELETE),(Article,Photo))
```

## 2. Check Abilities & Authorization

Helper methods are mixed into your User model (once it is decorated with the `@authorization_target`)

For example:

```python
from bouncer import authorization_target

@authorization_target
class User(object):

def __init__(self, **kwargs):
    self.id = kwargs.get('id', 1)
    self.name = kwargs.get('name', '')
    self.admin = kwargs.get('name', False)
    pass

@property
def is_admin(self):
    return self.admin
    
jonathan = User(name='jonathan',admin=False)
marc = User(name='marc',admin=False)

article = Article(author=jonathan)

print jonathan.can(EDIT,article)   # True
print marc.can(EDIT,article)       # False
```
------------

If you use Flask, I am currently working on a Flask extension -- follow its progress here: [flask-bouncer](https://github.com/jtushman/flask-bouncer).


## Questions / Issues
Feel free to ping me on twitter: [@tushman](http://twitter.com/tushman) or add issues or PRs at [https://github.com/jtushman/bouncer](https://github.com/jtushman/bouncer)

