"""
    bouncer
    -------

    Simple Declarative Authentication DSL inspired by Ryan Bates excellent cancan library

    :copyright:  (c) 2014 by Jonathan Tushman.
    :license:    MIT, see LICENSE for more details.
"""

__author__ = 'jtushman'

from bouncer.models import Rule, Ability
from bouncer.exceptions import AccessDenied

def can(user, action, subject):
    """Checks if a given user has the ability to perform the action on a subject

    :param user: A user object
    :param action: an action string, typically 'read', 'edit', 'manage'.  Use bouncer.constants for readability
    :param subject: the resource in question.  Either a Class or an instance of a class.  Pass the class if you
                    want to know if the user has general access to perform the action on that type of object.  Or
                    pass a specific object, if you want to know if the user has the ability to that specific instance

    :returns: Boolean
    """
    ability = Ability(user, get_authorization_method())
    return ability.can(action, subject)


def cannot(user, action, subject):
    """inverse of ``can``"""
    ability = Ability(user, get_authorization_method())
    return ability.cannot(action, subject)


def ensure(user, action, subject):
    """ Similar to ``can`` but will raise a AccessDenied Exception if does not have access"""
    ability = Ability(user, get_authorization_method())
    if ability.cannot(action, subject):
        raise AccessDenied()

_authorization_method = None

def authorization_method(original_method):
    """The method that will be injected into the authorization target to perform authorization"""
    global _authorization_method
    _authorization_method = original_method
    return original_method


def get_authorization_method():
    return _authorization_method

_authorization_target = None


def authorization_target(original_class):
    """ Add bouncer goodness to the model.  This is a class decorator, when added to your User model if will add
        ``can`` and ``cannot`` methods to the class
    :param original_class:  the User class to be decorated
    """

    def can(self, action, subject):
        ability = Ability(self, get_authorization_method())
        return ability.can(action, subject)

    def cannot(self, action, subject):
        return not can(self, action, subject)

    setattr(original_class, 'can', can)
    setattr(original_class, 'cannot', cannot)

    return original_class