import nose
from nose.tools import assert_raises

from bouncer import authorization_target, authorization_method, Ability
from bouncer.constants import *


def test_basic_usage():

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

    sally = User(name='sally', admin=False)
    billy = User(name='billy', admin=True)

    article = Article(author=sally)

    # check abilities
    assert sally.can(EDIT, article)

    billys_article = Article(author=billy)

    assert sally.cannot(EDIT, billys_article)
    assert billy.can(EDIT, billys_article)


def test_dictionary_defination_usage():

    @authorization_method
    def authorize(user, abilities):

        if user.is_admin:
            # self.can_manage(ALL)
            abilities.append(MANAGE, ALL)
        else:
            abilities.append(READ, ALL)
            abilities.append(EDIT, Article, author=user)


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

    sally = User(name='sally', admin=False)
    billy = User(name='billy', admin=True)

    article = Article(author=sally)

    # check abilities
    assert sally.can(EDIT, article)

    billys_article = Article(author=billy)

    assert sally.cannot(EDIT, billys_article)
    assert billy.can(EDIT, billys_article)


def test_finding_relivant_rules():

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
    billy = User(name='billy', admin=True)

    ability = Ability(billy)
    relevant_rules = ability.relevant_rules_for_match(MANAGE, Article)
    assert len(relevant_rules) == 1
    assert relevant_rules[0].actions == [MANAGE]
    assert relevant_rules[0].subjects == [ALL]

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


def test_using_class_strings():

    @authorization_method
    def authorize(user, abilities):

        if user.is_admin:
            # self.can_manage(ALL)
            abilities.append(MANAGE, ALL)
        else:
            abilities.append(READ, ALL)

            def if_author(article):
                return article.author == user

            abilities.append(EDIT, 'Article', if_author)


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

    sally = User(name='sally', admin=False)
    billy = User(name='billy', admin=True)

    article = Article(author=sally)

    # check abilities
    assert sally.can(EDIT, article)

    billys_article = Article(author=billy)

    assert sally.cannot(EDIT, billys_article)
    assert billy.can(EDIT, billys_article)


if __name__ == "__main__":
    nose.run()