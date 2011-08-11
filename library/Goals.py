"""=============================================================================
    Goal.py
    ------------
    Contains a list of goals.  Each goal has persona values associated with it.
    This file is imported from Entity.py
============================================================================="""
"""=============================================================================

IMPORTS

============================================================================="""
"""=============================================================================

Goals

============================================================================="""
'''Persona values are a tuple of (MIN, MAX), where MIN and MAX are
percentage values that indicate the range of possible persona values'''
GOALS = {
    'self_preservation': {
        'persona': {
            'agreeableness': (-1.0, -.8),
            'neuroticism': (.8, 1.0), 
        },
    },
    'other_preservation': {
        #other preservation is basically the opposite of self preservation, but
        #   there could be cases where neither goal is applied
        'persona': {
            'agreeableness': (-.79, 1.0),
            'neuroticism': (-1.0,.79),
        },
    },
    'maintaing_health': {
        'persona': {
            'conscientiousness': (.2, 1.0),
        },
    },
    'power': {
        'persona': {
            'extraversion': (.6, 1.0),
            'conscientiousness': (.4, 1.0),
            
        },
    },
    'wealth': {
        'persona': {
            'openness': (-1.0, .7),
            'conscientiousness': (0.0, 1.0),
        },
    },
    'profession': {
        'persona': {
            'conscientiousness': (.3,1.0),
            'neuroticism': (-1.0, .5),
        },
    },
    'friendship': {
        'persona': {
            'openness': (-.7, 1.0),
            'extraversion': (0.0, 1.0),
            'agreeableness': (-.5, 1.0),
        },
    },
    'romance': {
        'persona': {
            'openness': (-.2, 1.0),
            'agreeableness': (-.5, 1.0),
        },
    },
    'respect': {
        'persona': {
            'conscientiousness': (.4,1.0),
            'extraversion': (.5,1.0),
        },
    },
    'creativity': {
        'persona': {
            'openness': (.4,1.0),
        },
    },
}
