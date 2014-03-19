from flask import request
from abilities import Ability

class AuthorizationException(Exception):
    pass



class Condition(object):

    def __init__(self, action, subject):
        self.action = action
        self.subject = subject

    def get_current_user(self):
        return object()

    def test(self, current_user):
        ability = Ability(current_user)
        if ability.cannot(self.action, self.subject):
            raise AuthorizationException("User does not have access to resource")



class AbilityManager(object):
    """Thie class is used to control the Abilities Integration to one or more Flask applications"""

    def __init__(self, app):
        self.app = app
        self.init_app(app)

        self.endpoint_dict = dict()

        self.authorization_target_callback = None

        self.authorization_method_callback = None

        self._current_user_proxy = None


    def requires(self, *args):

        def decorator(f):
            print "args: ", args
            print "is this the endpoint: {}".format(f.__name__)

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

    def current_user_proxy(self, method):
        self._current_user_proxy = method
        return method

    @property
    def current_user(self):
        return self._current_user_proxy()

    def check_abilities(self):
        for condition in self.relevant_conditions_for_request():
            condition.test(self.current_user)

    def relevant_conditions_for_request(self):
        return self.endpoint_dict.get(request.endpoint, dict())
