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
GOALS = {
    'self_preservation': {
        'persona': {
            'agreeableness': (-100, -80),
            'neuroticism': (80, 100), 
        },
    },
    'other_preservation': {
        'persona': {
            'agreeableness': (-79, 100),
            'neuroticism': (-100,79),
        },
    },
    'maintaing_health': {
        'persona': {
            'conscientiousness': (20, 100),
        },
    },
    'power': {
        'persona': {
            'extraversion': (60, 100),
            'conscientiousness': (40, 100),
        },
    },
    'wealth': {
        'persona': {
            'openness': (-100, 70),
            'conscientiousness': (0, 100),
        },
    },
    'profession': {
        'persona': {
            'conscientiousness': (30,100),
            'neuroticism': (-100, 50),
        },
    },
    'friendship': {
        'persona': {
            'openness': (-70, 100),
            'extraversion': (0, 100),
            'agreeableness': (-50, 100),
        },
    },
    'romance': {
        'persona': {
            'openness': (-20, 100),
            'agreeableness': (-50, 100),
        },
    },
    'respect': {
        'persona': {
            'conscientiousness': (20,100),
            'extraversion': (40,100),
        },
    },
    'creativity': {
        'persona': {
            'openness': (40,100),
        },
    },
}
