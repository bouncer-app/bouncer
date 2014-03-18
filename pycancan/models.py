from pycancan.constants import *
import inspect


def listify(list_or_single):
    if isinstance(list_or_single, (list, tuple)):
        return list_or_single
    else:
        return [list_or_single]


class Rule(object):
    def __init__(self, base_behavior, action, subject, conditions=None):
        self.base_behavior = base_behavior
        self.actions = listify(action)
        self.subjects = listify(subject)
        self.conditions = conditions

    # Matches both the subject and action, not necessarily the conditions
    def is_relavant(self, action, subject):
        # print "Maches Action: [{}]".format(self.matches_action(action))
        # print "Maches Subject: [{}]".format(self.matches_subject(subject))
        return self.matches_action(action) and self.matches_subject(subject)

    @property
    def expanded_actions(self):
        return self._expanded_actions

    @expanded_actions.setter
    def expanded_actions(self, value):
        self._expanded_actions = value

    def matches_action(self, action):
        return MANAGE in self.expanded_actions or action in self.expanded_actions

    def matches_subject(self, subject):
        return ALL in self.subjects or subject in self.subjects or self.matches_subject_class(subject)

    # Matches the conditions
    def matches_conditions(self, action, subject):
        pass

    def matches_subject_class(self, subject):
        for sub in self.subjects:
            if inspect.isclass(sub):
                if isinstance(subject, sub) or \
                                subject.__class__.name == str(sub) or \
                                inspect.isclass(subject) and issubclass(subject, sub):
                    return True
        return False


class RuleList(list):
    def append(self, *item_description_or_rule):
        # Will check it a Rule or a description of a rule
        # construct a rule if necessary then append
        if len(item_description_or_rule) == 1 and isinstance(item_description_or_rule[0], Rule):
            item = item_description_or_rule[0]
            super(RuleList, self).append(item)
        else:
            # try to construct a rule
            item = Rule(True, *item_description_or_rule)
            super(RuleList, self).append(item)


class Ability(object):

    @classmethod
    def set_authorization_method(cls, authorization_method):
        setattr(cls, 'authorize', staticmethod(authorization_method))


    def __init__(self, user):
        self.rules = RuleList()
        Ability.authorize(user, self.rules)


    def can(self, action, subject):
        self.rules.append(Rule(True, action, subject))

    def cannot(self, action, subject):
        self.rules.append(Rule(False, action, subject))

    def relevant_rules_for_match(self, action, subject):
        matching_rules = []
        for rule in self.rules:
            rule.expanded_actions = self.expand_actions(rule.actions)
            print "Expanded Actions for {} is {}".format(rule.actions,rule.expanded_actions)
            print "Testing relavancy: {} {}".format(action, subject)
            if rule.is_relavant(action, subject):
                matching_rules.append(rule)
        return matching_rules

    def expand_actions(self, actions):
        """Accepts an array of actions and returns an array of actions which match.
        This should be called before "matches?" and other checking methods since they
        rely on the actions to be expanded."""
        results = list()

        for action in actions:
            if action in self.aliased_actions:
                results.append(action)
                for item in self.expand_actions(self.aliased_actions[action]):
                    results.append(item)
            else:
                results.append(action)

        return results


    @property
    def aliased_actions(self):
        return self.default_alias_actions


    @property
    def default_alias_actions(self):
        return {
            READ: [INDEX, SHOW],
            CREATE: [NEW],
            UPDATE: [EDIT]
        }



