from bouncer.constants import *
import inspect


def listify(list_or_single):
    if isinstance(list_or_single, (list, tuple)):
        return list_or_single
    else:
        return [list_or_single]


class Rule(object):
    def __init__(self, base_behavior, action, subject, conditions=None, **conditions_hash):
        self.base_behavior = base_behavior
        self.actions = listify(action)
        self.subjects = listify(subject)
        self.conditions = None

        if conditions is not None and len(conditions_hash) > 0:
            raise TypeError('cannot provide both a condition method and hash -- pick one')
        elif conditions is not None:
            self.conditions = conditions
        elif len(conditions_hash) > 0:
            self.conditions = conditions_hash

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
        # print "Matching Conditions on {} for {}".format(action, subject)
        if self.conditions is None:
            return True
        elif inspect.isclass(subject):
            # IMPORTANT we only check conditions if we are testing specific instances of a class NOT of the classes
            # themselves
            return True
        elif isinstance(self.conditions, dict):
            return self.matches_dict_conditions(action, subject)
        else:
            return self.matches_function_conditions(action, subject)

    def matches_dict_conditions(self, action, subject):
        return all(self.matches_hash_condition(subject, key, self.conditions[key]) for key in self.conditions)

    def matches_hash_condition(self, subject, key, value):
        return getattr(subject, key) == value

    def matches_function_conditions(self, action, subject):
        return self.conditions(subject)

    def matches_subject_class(self, subject):
        for sub in self.subjects:
            if (inspect.isclass(sub) and isinstance(subject, sub)) or \
                subject.__class__.__name__ == str(sub) or \
                    (inspect.isclass(subject) and issubclass(subject, sub)):
                    return True
        return False


class RuleList(list):
    def append(self, *item_description_or_rule, **kwargs):
        # Will check it a Rule or a description of a rule
        # construct a rule if necessary then append
        if len(item_description_or_rule) == 1 and isinstance(item_description_or_rule[0], Rule):
            item = item_description_or_rule[0]
            super(RuleList, self).append(item)
        else:
            # try to construct a rule
            item = Rule(True, *item_description_or_rule, **kwargs)
            super(RuleList, self).append(item)

    # alias append
    # so you can do things like this:
    #     @authorization_method
    # def authorize(user, they):
    #
    #     if user.is_admin:
    #         # self.can_manage(ALL)
    #         they.can(MANAGE, ALL)
    #     else:
    #         they.can(READ, ALL)
    #
    #         def if_author(article):
    #             return article.author == user
    #
    #         they.can(EDIT, Article, if_author)
    can = append


class Ability(object):

    def __init__(self, user, authorization_method=None):
        from . import get_authorization_method
        self.rules = RuleList()
        self.user = user
        self._aliased_actions = self.default_alias_actions

        if authorization_method is not None:
            self.authorization_method = authorization_method
        else:
            # see if one has been set globaly
            self.authorization_method = get_authorization_method()

    @property
    def authorization_method(self):
        return self._authorization_method

    @authorization_method.setter
    def authorization_method(self, value):
        self._authorization_method = value
        # Now that we have it run use it to set the rules
        if self._authorization_method is not None:
            self._authorization_method(self.user, self.rules)


    def can(self, action, subject):
        # print "Can {} {} on {}".format(self.user, action, subject)
        return any(rule.matches_conditions(action, subject) for rule in self.relevant_rules_for_match(action, subject))

    def cannot(self, action, subject):
        return not self.can(action, subject)

    def relevant_rules_for_match(self, action, subject):
        matching_rules = []
        for rule in self.rules:
            rule.expanded_actions = self.expand_actions(rule.actions)
            # print "Expanded Actions for {} is {}".format(rule.actions,rule.expanded_actions)
            # print "Testing relavancy: {} {}".format(action, subject)
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
        return self._aliased_actions

    @aliased_actions.setter
    def aliased_actions(self, value):
        self._aliased_actions = value


    @property
    def default_alias_actions(self):
        return {
            READ: [INDEX, SHOW],
            CREATE: [NEW],
            UPDATE: [EDIT]
        }




