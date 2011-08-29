"""=============================================================================
    Action.py 
    ------------
    Contains a list of actions.  Each goal has persona values associated with it.
    This file is imported from Entity.py
============================================================================="""
"""=============================================================================

IMPORTS

============================================================================="""
import datetime
import math
import random 

"""=============================================================================

Actions

============================================================================="""
#TODO:
#   -Keep track of all action classes
#   -Keep track of all actions commited
class Action(object):
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

    ACTIONS = {
        #Actions is a dict containing all action classes        
    }

    '''ACTIONS_BY_GOALS
    --------------------
    Contains a dictionary of 'goal IDs', each goal containing a list of
        actions which may satisfy that goal
    '''
    ACTIONS_BY_GOALS = {
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
    '''====================================================================
    
    Actions

    ======================================================================='''
    #Actions are events that entities perform to help them accomplish goals.
    #   Most actions have a source and target entity (or object or location),
    #   requirements that must be met to perform the action, and effects the
    #   action has on other entities (or objects or locations)
    def converse(self, 
        target=None):
        '''converse(self, target)
        -------------------------
        Takes in a required target Entity.  The result of the conversation
        will depend on both Entity's persona'''
        if target is None:
            return 'Cannot converse without a target Entity'
        #--------------------------------
        #REQUIREMENTS
        #--------------------------------
        #Define requirements Entity must have to preform this action
        requirements = {
            #Define the source (this entity's) requirements for this action
            'source': {
                'persona': {
                    'extraversion_min': -80,
                    'agreeableness_min': -50,
                },
            },
            'target': {
                'persona': {
                    'extraversion_min': -80, 
                    'agreeableness_min': -50,
                },
            },
        }

        #--------------------------------
        #Effects
        #--------------------------------
        #effects is an array of dictionary objects containing the effects
        #   this action has.  Each effect contains a target, which can be
        #   an entity / object / location, etc., along with persona (if
        #   Entity) and other effects
        effects = {
            #First effect affects source
            #----------------------------
            'source': {
                'target': self,
                'network': [ [target, 0] ],
            },
            #Second effect affects target
            #----------------------------
            'target': {
                'target': target,
                'network': [ [self, 0] ],
            }
        }

        #Update the 'network' value of the effect
        #   First, get the distance between the extraversion and agreeableness
        #   values
        extraversion_dist = abs(self.persona[
            'extraversion'] \
                - target.persona[
            'extraversion']) 

        agreeableness_dist = abs(self.persona[
            'agreeableness'] \
            - target.persona[
            'agreeableness']) 

        #Setup value to adjust the Entities' network value by
        total_dist = abs(extraversion_dist + agreeableness_dist) / 2.0

        #Randomize the value a bit, so the conversation doesn't always add the
        #   same value
        #Use -total_dist / 2 as min, +total_dist / 2 as max
        #TODO: Think about a better way to do this...
        total_dist = random.randint(
            (int((total_dist * -1) / 2)),
            (int(total_dist)))

        #Multiple total_dist by the combined similarity values shared
        #   between the two Entities
        temp_total = abs(
            total_dist * self.get_similarity_total(target))

        #If total_dist was below 0, then multiple the temp_total
        #   by negative 1 (It's possible the total_dist AND
        #   their similarity rankings could be negative, which
        #   would result in a positive
        if total_dist < 0:
            temp_total *= -1

        #Set total_dist as the temp_total (needed the above intermediate
        #   step to check if it is a negative or positive value
        total_dist = temp_total

        #   For this entity, update value of the target entity's network effect
        effects['source']['network'][0][1] = total_dist 
        effects['target']['network'][0][1] = total_dist 

        self.action_perform_effects(target=self, effects=effects)
        #self.action_perform_effects(target=self, effects=effects['source'])
        #self.action_perform_effects(target=target, effects=effects['target'])
