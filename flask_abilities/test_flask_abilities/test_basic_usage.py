from flask import Flask, g
from flask_abilities import AbilityManager, AuthorizationException
from abilities.constants import *
from nose.tools import *

from contextlib import contextmanager
from flask import appcontext_pushed



# http://flask.pocoo.org/docs/testing/
@contextmanager
def user_set(app, user):
    def handler(sender, **kwargs):
        g.current_user = user
    with appcontext_pushed.connected_to(handler, app):
        yield

class User(object):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 1)
        self.name = kwargs['name']
        self.admin = kwargs['admin']
        pass

    @property
    def is_admin(self):
        return self.admin

app = Flask("basic")
app.debug = True
ability = AbilityManager(app)

class Article(object):

    def __init__(self, **kwargs):
        self.author = kwargs['author']


class TopSecretFile(object):
    pass


@ability.current_user_proxy
def current_user():
    return g.current_user


@ability.authorization_method
def authorize(user, abilities):

    if user.is_admin:
        # self.can_manage(ALL)
        abilities.append(MANAGE, ALL)
    else:
        abilities.append(READ, Article)
        abilities.append(EDIT, Article, author=user)


@app.route("/")
def hello():
    return "Hello World"

@app.route("/articles")
@ability.requires(READ, Article)
def articles_index():
    return "A bunch of articles"

@app.route("/topsecret")
@ability.requires(READ, TopSecretFile)
def topsecret_index():
    return "A bunch of top secret stuff that only admins should see"


@app.route("/article/<int:post_id>", methods=['POST'])
def edit_post(post_id):
    # article = Article.find(post_id)
    # authorize(EDIT,article) raise 400 if not authorized
    return "editing a post"


client = app.test_client()

def test_default():
    jonathan = User(name='jonathan',admin=False)
    with user_set(app, jonathan):
        resp = client.get('/')
        eq_("Hello World", resp.data)


def test_allowed_index():
    jonathan = User(name='jonathan',admin=False)
    with user_set(app, jonathan):
        resp = client.get('/articles')
        eq_("A bunch of articles", resp.data)

def test_not_allowed_index():
    jonathan = User(name='doug',admin=False)
    with user_set(app, jonathan):
        with assert_raises(AuthorizationException):
            resp = client.get('/topsecret')
