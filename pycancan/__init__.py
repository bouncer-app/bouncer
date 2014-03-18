__author__ = 'jtushman'

from pycancan.models import Rule, Ability


def authorization_method(original_method):
    """The method that will be injected into the authorization target to perform authorization"""
    Ability.set_authorization_method(original_method)
    return original_method


_authorization_target = None


def authorization_target(original_class):
    """Add pycancan goodness to the model"""

    def is_authotized_to(self, action, subject, conditions=None):
        return True

    setattr(original_class, 'is_authotized_to', is_authotized_to)

    def can(self, action, subject):
        ability = Ability(self)

    setattr(original_class, 'can', can)

    def cannot(self, action, subject):
        self.runs.append(Rule(False, action, subject))

    setattr(original_class, 'cannot', cannot)

    def relevant_rules_for_match(self, action, subject):
        return [rule for rule in self.rules if rule.is_relavant(action, subject)]

    setattr(original_class, 'relevant_rules_for_match', relevant_rules_for_match)

    return original_class


def authorize():
    pass