pycancan (need better name)
========

Simple Declarative Authentication based on Ryan Bates excellent cancan library

## Installation

`pip install pycancan`


# Getting Started

## 1. Defining Abilities

User permissions are defined in an `method` decorated with `@authorize_method`

A simple setup looks like so ...

```python
from pycancan import authorization_method
from pycancan.constants import *
from yourproject.models import Article

@authorization_method
def authorize(user, abilities):

    if user.is_admin:
        # self.can_manage(ALL)
        abilities.append(MANAGE, ALL)
    else:
        abilities.append(READ, ALL)

        def if_author(article):
            return article.author == user

        abilities.append(EDIT, Article, if_author)
```

See [Defining Abilities](#) for details

## 2. Check Abilities & Authorization

Helper methods are mixed into your User model (once it is decorated with the `@authorization_target`)

For example:

```python
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


