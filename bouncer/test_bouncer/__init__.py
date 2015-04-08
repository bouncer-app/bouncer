import nose
from nose.tools import assert_raises, raises
from bouncer import authorization_target, authorization_method, Ability, can, cannot, ensure
from bouncer.exceptions import AccessDenied
from bouncer.constants import *
from bouncer.test_bouncer.models import User, Article, BlogPost


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

    sally = User(name='sally', admin=False)
    billy = User(name='billy', admin=True)

    article = Article(author=sally)

    # check abilities
    assert can(sally, EDIT, article)

    billys_article = Article(author=billy)

    assert cannot(sally, EDIT, billys_article)
    assert can(billy, EDIT, billys_article)

def test_user_decorator():

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

    authorization_target(User)

    sally = User(name='sally', admin=False)
    billy = User(name='billy', admin=True)

    article = Article(author=sally)

    # check abilities
    assert sally.can(EDIT, article)

    billys_article = Article(author=billy)

    assert sally.cannot(EDIT, billys_article)
    assert billy.can(EDIT, billys_article)

@raises(AccessDenied)
def test_ensure():

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


    sally = User(name='sally', admin=False)
    billy = User(name='billy', admin=True)

    article = Article(author=sally)
    billys_article = Article(author=billy)

    # This should raise and AccessDenied exception
    ensure(sally, EDIT, billys_article)

def test_dictionary_defination_usage():

    @authorization_method
    def authorize(user, abilities):

        if user.is_admin:
            # self.can_manage(ALL)
            abilities.append(MANAGE, ALL)
        else:
            abilities.append(READ, ALL)
            abilities.append(EDIT, Article, author=user)

    authorization_target(User)

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

    authorization_target(User)

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
    def authorize(user, they):
        they.can(EDIT, 'Article')

    authorization_target(User)

    sally = User(name='sally', admin=False)

    article = Article(author=sally)

    # Can edit articles in general
    assert sally.can(EDIT, Article)

    # Can edit specific article
    assert sally.can(EDIT, article)


def test_cannot_override():

    @authorization_method
    def authorize(user, they):
        they.can(MANAGE, ALL)
        they.cannot(DELETE, Article)

    authorization_target(User)

    sally = User(name='sally', admin=False)

    # test checks againsts a articles in general
    assert sally.can(READ, Article)
    assert sally.cannot(DELETE, Article)

    article = Article(author=sally)

    # test checks againsts a specific article
    assert sally.can(READ, article)
    assert sally.cannot(DELETE, article)





if __name__ == "__main__":
    nose.run()