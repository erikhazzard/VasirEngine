"""=============================================================================
    Action.py 
    ------------
    Contains a list of actions.  Each goal has persona values associated with it.
    This file is imported from Entity.py
============================================================================="""
"""=============================================================================

IMPORTS

============================================================================="""
"""=============================================================================

Actions

============================================================================="""
class Action(Object):
    '''Action:
    --------------------------------------------------------------------------
    This class' purpose is to provide a base set of attributes for other actions
    which inheirt this Action class, along with keeping track of all Action
    objects which have been instantiated
    -------------------------------------
    Actions are events that entities perform to help them accomplish goals.

    The data structure is set up like:

    #Source is the the entity (or possibly object) that is the source of
    #   this action
    SOURCE: Entity,

    #Target describes the target of this action - be it an Entity or Object
    TARGET: {} 

    #Requirements specify the conditions needs to perform this action, if
    #   any.  These are applied to the SOURCE described above
    REQUIREMENTS: [{
        'persona': {},
        'stats': {},
        etc.
    }]

    #Effects describes what will happen if the entity successfully performs
    #   this action.
    #   Each effect has a target (could be the source entity), and the 
    #   attributes that get affected if the action is successfully performed
    EFFECTS: [{'target': ____,
            'persona': {},
            'stats': {},
            'money': X,
            'restedness': X},
            {} ]
'''

    ACTIONS: {
        #Actions is a dict containing all action classes        
    }

    '''ACTIONS_BY_GOALS
    --------------------
    Contains a dictionary of 'goal IDs', each goal containing a list of
        actions which may satisfy that goal
    '''
    ACTIONS_BY_GOALS: {
        #Example:
        #'goal': [ action_object1, action_object2 ]
    }

    def __init__(self,
        #--------------------------------
        #Source
        #--------------------------------
        #Source can be an Entity, object, or place
        source=None,

        #--------------------------------
        #Target
        #--------------------------------
        #Target can be an Entity, object, or place
        target=None,

        #--------------------------------
        #Requirements
        #--------------------------------
        requirements=None,
        #EXAMPLE:
        #requirements={
        #   'persona': {
        #   'opennes': 20,
        #   'agreeableness': 20,
        #   remaning traits...
        #   },
        ##States is a dict of stats required
        #    'stats': None,
        # #Money is an integer
        #    'money': None,
        ##Restedness is an integer
        #   'restedness': None
        #},

        #--------------------------------
        #Effects
        #--------------------------------
        #effects is an array of dictionary objects containing the effects
        #   this action has.  Each effect contains a target, which can be
        #   an entity / object / location, etc., along with persona (if
        #   Entity) and other effects
        effects=None,
        #EXAMPLE:
        #effects = [
        #   {'target': Entity_A,
        #   'persona': { ... }
        #   'stats': { ... }
        #   'money': X}
        #]
            ):
        '''These are properties that every action class will receive by
        default. Sub classes can override and provide more properties.'''
        self.source = source
        self.target = target
        self.requirements = requirements
        self.effects = effects
        


class Action_Converse(Action):
    pass
