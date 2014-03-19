from flask import Flask, url_for
from flask_abilities import AbilityManager
from abilities.constants import *
from nose.tools import *

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


@app.route("/")
def hello():
    return "Hello World"

@app.route("/articles")
def articles_index():
    return "A bunch of articles"

@app.route("/article/<int:post_id>", methods=['POST'])
def edit_post(post_id):
    return "editing a post"


client = app.test_client()

def test_default():
    resp = client.get('/')
    eq_("Hello World", resp.data)

