from flask import Flask, url_for
from flask_abilities import AbilityManager
from abilities.constants import *
from nose.tools import *


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
ability = AbilityManager(app)

@ability.authorization_method
def authorize(user, abilities):

    if user.is_admin:
        # self.can_manage(ALL)
        abilities.append(MANAGE, ALL)
    else:
        abilities.append(READ, ALL)

        def if_author(article):
            return article.author == user

        abilities.append(EDIT, 'Article', if_author)

@ability.current_user_proxy
def current_user():
    return User(name='jonathan', admin=False)


@app.route("/")
def hello():
    return "Hello World"

@app.route("/articles")
@ability.requires(READ, 'Article')
def articles_index():
    return "A bunch of articles"

@app.route("/article/<int:post_id>", methods=['POST'])
def edit_post(post_id):
    # article = Article.find(post_id)
    # authorize(EDIT,article) raise 400 if not authorized
    return "editing a post"


client = app.test_client()

def test_default():
    resp = client.get('/')
    eq_("Hello World", resp.data)


def test_articles():
    resp = client.get('/articles')
    eq_("A bunch of articles", resp.data)
