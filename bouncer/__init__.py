__author__ = 'jtushman'

from bouncer.models import Rule, Ability

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
    """Add pycancan goodness to the model"""

    def can(self, action, subject):
        ability = Ability(self, get_authorization_method())
        return ability.can(action, subject)

    def cannot(self, action, subject):
        return not can(self, action, subject)

    setattr(original_class, 'can', can)
    setattr(original_class, 'cannot', cannot)

    return original_class