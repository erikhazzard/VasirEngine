"""=============================================================================
    Actions.py
    ------------
    Contains all possible actions.

    Actions are functions here.  When the action function gets called, it will
    create an Action object (from the Action class)  
============================================================================="""
"""=============================================================================

IMPORTS

============================================================================="""
import math
import random
import datetime

"""=============================================================================

ACTIONS

============================================================================="""
#Actions are events that entities perform to help them accomplish goals.
#   Most actions have a source and target entity (or object or location),
#   requirements that must be met to perform the action, and effects the
#   action has on other entities (or objects or locations)
def converse(
    source=None,
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
            'target': source,
            'network': [ [target, 0] ],
        },
        #Second effect affects target
        #----------------------------
        'target': {
            'target': target,
            'network': [ [source, 0] ],
        }
    }

    #Update the 'network' value of the effect
    #   First, get the distance between the extraversion and agreeableness
    #   values
    extraversion_dist = abs(source.persona[
        'extraversion'] \
            - target.persona[
        'extraversion']) 

    agreeableness_dist = abs(source.persona[
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
        total_dist * source.get_similarity_total(target))

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

    #Return a dict of all the sources / effects, which will be used to
    #   generate an Action object (in Action.py)
    return {
        'source':source,
        'target':target,
        'requirements':requirements,
        'effects':effects,
        'string_repr': 'Conversation',
    }

    #source.action_perform_effects(target=source, effects=effects)

    #self.action_perform_effects(target=self, effects=effects['source'])
    #self.action_perform_effects(target=target, effects=effects['target'])
