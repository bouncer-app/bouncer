bouncer (ALPHA)
========

Simple Declarative Authentication DSL based on Ryan Bates excellent cancan library

[![Build Status](https://travis-ci.org/jtushman/bouncer.svg)](https://travis-ci.org/jtushman/bouncer)

## Introduction

Meet **bouncer**.

**bouncer** is your faithful servant.  Big, burly, trustworthy -- not the sharpest tool in the box,
but very effective in what he does.  You just have to talk simply to him.  For example:

```python
from bouncer import authorization_method
from bouncer.constants import *
from yourproject.models import Article

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

And once you have that setup, you can ask questions like:

```
    jonathan = User(name='jonathan',admin=False)
    marc = User(name='marc',admin=False)

    article = Article(author=jonathan)

    print jonathan.can(EDIT,article)   # True
    print marc.can(EDIT,article)       # False
```


## Installation

`pip install bouncer`


# Getting Started

## 1. Defining Abilities

User permissions are defined in an `method` decorated with `@authorize_method`

A simple setup looks like so ...

```python
from bouncer import authorization_method
from bouncer.constants import *
from yourproject.models import Article

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

You can also use an alternative `dict` syntax.  The following is equivalent to above:
```python
from bouncer import authorization_method
from bouncer.constants import *
from yourproject.models import Article

@authorization_method
def authorize(user, they):

    if user.is_admin:
        they.can(MANAGE, ALL)
    else:
        they.can(READ, ALL)
        they.can(EDIT, Article, author=user)
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
            self.name = kwargs['name']
            self.admin = kwargs['admin']
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

If you use flask, I am currently working on a flask extension -- follow its progess here: [flask-bouncer](https://github.com/jtushman/flask-bouncer).


## Questions / Issues
Feel free to ping me on twitter: [@tushman](http://twitter.com/tushman) or add issues or PRs at [https://github.com/jtushman/bouncer](https://github.com/jtushman/state_machine)

