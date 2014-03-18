import nose
import inspect
from nose.plugins.skip import SkipTest
from nose.tools import *
from nose.tools import assert_raises

from pycancan import authorization_target, authorization_method, Ability
from pycancan.constants import *

# try:
#     from flask import Flask
# except:
#     flask = None


def test_ability():

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

            # Alternatively

            abilities.append(EDIT, BlogPost, author_id=user.id)
            abilities.append(READ, BlogPost, visible=True, active=True)


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

    class Article(object):

        def __init__(self, **kwargs):
            self.author = kwargs['author']

    class BlogPost(object):

        def __init__(self, **kwargs):
            self.author_id = kwargs['author_id']
            self.visible = kwargs.get('visible', True)
            self.active = kwargs.get('active', True)



    # Test relevant_rules
    print "Testing Billy"
    billy = User(name='billy', admin=True)
    ability = Ability(billy)
    relevant_rules = ability.relevant_rules_for_match(MANAGE, Article)
    assert len(relevant_rules) == 1
    assert relevant_rules[0].actions == [MANAGE]
    assert relevant_rules[0].subjects == [ALL]

    print "Testing Sally"
    sally = User(name='sally', admin=False)
    ability = Ability(sally)
    relevant_rules = ability.relevant_rules_for_match(MANAGE, Article)
    assert len(relevant_rules) == 0

    relevant_rules = ability.relevant_rules_for_match(READ, Article)
    assert len(relevant_rules) == 1
    assert relevant_rules[0].actions == [READ]
    assert relevant_rules[0].subjects == [ALL]

    article = Article(author=sally)
    relevant_rules = ability.relevant_rules_for_match(EDIT, article)
    assert relevant_rules[0].actions == [EDIT]
    assert relevant_rules[0].subjects == [Article]

    # check abilities
    print
    print "Test Checking Abilities"
    print
    assert sally.can(EDIT, article)

    billys_article = Article(author=billy)

    assert sally.cannot(EDIT, billys_article)


    # sally = User(name='sally', admin=False)


    # assert billy.can(MANAGE, Article)
    # assert not sally.can(MANAGE, Article)
    # or
    # assert sally.cannot(MANAGE, Article)

    # article = Article(author=sally)

    # assert sally.can(EDIT, article)

    # autorize

# def requires_flask():
#     return True
#
# @requires_flask
# def test_flask():
#
#     @authorize_user
#     def current_user():
#         return 'current_user'
#
#     # Approach 1
#     app = Flask()
#     @app.route('/articles')
#     @requires_ability(Article, READ)
#     def articles():
#         return "Hello"
#
#
#     # Approach 2
#     @app.route('/article/<id>', method=['post'])
#     def articles(id):
#         article = Article.find(id=id)
#         authorize(EDIT,article) #raise 400 if not authorized
#         return "Hello"






















