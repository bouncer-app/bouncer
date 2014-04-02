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