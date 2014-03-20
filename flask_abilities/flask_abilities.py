from flask import request, g
from werkzeug.exceptions import Unauthorized
from abilities import Ability


def authorize(action, subject):
    ability = Ability(get_current_user())
    if ability.cannot(action, subject):
        raise Unauthorized("User does not have access to resource")


def get_current_user():
    if hasattr(g, 'current_user'):
        return g.current_user
    else:
        raise Exception("Excepting current_user on flask's g")


class Condition(object):

    def __init__(self, action, subject):
        self.action = action
        self.subject = subject

    def test(self):
        ability = Ability(get_current_user())
        if ability.cannot(self.action, self.subject):
            raise Unauthorized("User does not have access to resource")



class AbilityManager(object):
    """Thie class is used to control the Abilities Integration to one or more Flask applications"""

    def __init__(self, app):
        self.app = app
        self.init_app(app)

        self.endpoint_dict = dict()

        self.authorization_target_callback = None

        self.authorization_method_callback = None


    def requires(self, *args):

        def decorator(f):
            # print "args: ", args
            # print "is this the endpoint: {}".format(f.__name__)

            self.endpoint_dict.setdefault(f.__name__, list())
            self.endpoint_dict[f.__name__].append(Condition(*args))

            return f

        return decorator

    def init_app(self, app):
        # I am sure that we will need to put something in here soon
        app.before_request(self.check_abilities)

    def authorization_target(self, callback):
        """
        the callback for finding the currentuser in the given request context.
        should return `None` if the user does not exist
        """
        self.authorization_target_callback = callback
        return callback

    def authorization_method(self, callback):
        """
        the callback for defining user abilities
        """
        self.authorization_method_callback = callback
        Ability.set_authorization_method(self.authorization_method_callback)
        return callback


    def check_abilities(self):
        for condition in self.relevant_conditions_for_request():
            condition.test()

    def relevant_conditions_for_request(self):
        return self.endpoint_dict.get(request.endpoint, dict())
