__author__ = 'jtushman'

def can(user,action,target):
    # need to make sure that the Ability class has been loaded -- expect it in a certain path??
    return _ability_class.authorize(user,action,target)


def is_authorized_to(action,item,condition=None):
    pass

_ability_class = None

def acts_as_ability(original_class):

    assert hasattr(original_class,'authorize'), 'Your Ability Class should implement authorize'
    # check that authorize has the right signiture


    global _ability_class
    _ability_class = original_class
    return original_class