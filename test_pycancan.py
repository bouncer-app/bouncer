import nose
from nose.plugins.skip import SkipTest
from nose.tools import *
from nose.tools import assert_raises

from pycancan import acts_as_ability, can, is_authorized_to
from pycancan.constants import *


def test_ability():
    @acts_as_ability
    class Ability(object):

        def authorize(self, current_user):

            if current_user.is_admin:
                is_authorized_to(MANAGE, ALL)
            else:
                is_authorized_to(READ, ALL)

                def if_author(article):
                    return article.author == current_user

                is_authorized_to(EDIT, Article, if_author)


    class Article(object):

        def __init__(self, **kwargs):
            self.author = kwargs['author']

    class User(object):

        def __init__(self, **kwargs):
            self.name = kwargs['name']
            self.admin = kwargs['admin']
            pass

        @property
        def is_admin(self):
            return self.admin


    # check abilities
    billy = User(name='billy', admin=True)
    sally = User(name='sally', admin=False)

    assert can(billy, MANAGE, Article)
    assert not can(sally, MANAGE, Article)

    article = Article(author=sally)

    assert can(sally, EDIT, article)


    # autorize
