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
'''Actions are events that entities perform to help them accomplish goals.
The data structure is set up like:
    #ID specifies the ID of the action
    ID: {
        #Note: Many of these values will be passed in by the calling object

        #Type describes the type of action this is, or what class of action.
        #   For example: an insult would be a 'conversation' type of action
        TYPE: "",

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
    }
'''


ACTIONS = {
    'conversation_start': {
        'type': 'consversation',
        'soruce': None,
        'target': None,
        'requirements': None,
    }  

}
