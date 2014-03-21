from flask import request, g
from werkzeug.exceptions import Unauthorized
from bouncer import Ability


def bounce(action, subject):
    current_user = get_current_user()
    ability = Ability(current_user)
    if ability.cannot(action, subject):
        msg = "{} does not have {} access to {}".format(current_user, action, subject)
        raise Unauthorized(msg)


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
        bounce(self.action, self.subject)


class Bouncer(object):
    """Thie class is used to control the Abilities Integration to one or more Flask applications"""

    def __init__(self, app):
        self.app = app
        self.init_app(app)

        self.endpoint_dict = dict()

        self.authorization_method_callback = None

        self.flask_classy_classes = None


    def requires(self, *args):

        def decorator(f):
            # print "args: ", args
            # print "is this the endpoint: {}".format(f.__name__)

            self.endpoint_dict.setdefault(f.__name__, list())
            self.endpoint_dict[f.__name__].append(Condition(*args))

            return f

        return decorator

    def init_app(self, app):
        app.before_request(self.check_abilities)


    def bounce(self, *classy_routes):
        if self.flask_classy_classes is None:
            self.flask_classy_classes = list()
        self.flask_classy_classes.extend(classy_routes)


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

    def classy_conditions_for_request(self):
        if ':' not in request.endpoint:
            return list()

        parts = request.endpoint.split(':')
        if not len(parts) == 2:
            return list()

        class_name = parts[0]
        action_name = parts[1]

        classy_class = next((clazz for clazz in self.flask_classy_classes if clazz.__name__ == class_name), None)

        if not classy_class:
            return list()

        target_model = None
        if hasattr(classy_class, '__target_model__'):
            target_model = classy_class.__target_model__
        else:
            raise NotImplementedError('We will get to this -- but will inspect the class name to determine which model we care about')

        return [Condition(action_name, target_model)]


    def relevant_conditions_for_request(self):
        conditions = list()
        conditions.extend(self.endpoint_dict.get(request.endpoint, dict()))
        conditions.extend(self.classy_conditions_for_request())
        return conditions
