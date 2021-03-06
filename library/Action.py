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

import Actions
#TODO: Don't import Entity, use some other way to check if instance is
#   entity in the method functions below
import Entity

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
    Actions are events that entities perform to help them accomplish goals.'''

    _ACTIONS = {
        'converse': Actions.converse_definition,
        'move': Actions.move_definition,
    }

    '''ACTIONS_BY_GOALS
    --------------------
    Contains a dictionary of 'goal IDs', each goal containing a list of
        actions which may satisfy that goal
    '''
    _ACTIONS_BY_GOALS = {
        #Example:
        #'goal': [ action_object1, action_object2 ]
    }

    @classmethod
    def _create_action(
        cls,
        action_key=None,
        source=None,
        target=None,):
        '''_create_action:
        ------------------
        Class method which returns an Action object.  Used as a sort
        of factory to create Action objects.  Takes in an action key (
        which is used to get an action from the _ACTIONS dict), a source,
        and optional target (when necessary)'''
        #Get the parameters
        action_params = Action._ACTIONS[action_key]['function'](
            source=source,
            target=target,
        )

        if isinstance(action_params, dict):
            #Return an action object
            return Action(**action_params)
        else:
            #If the action could NOT be created (the action itself returned
            #   something other than a dict)
            print 'Could not create action'
            return False
    

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

        #--------------------------------
        #Add this action to the entity's memory?
        #--------------------------------
        add_to_memory=True,

        #--------------------------------
        #String representation of action
        #--------------------------------
        string_repr=None,
            ):
        '''These are properties that every action class will receive by
        default. Sub classes can override and provide more properties.'''
        self.source = source
        self.target = target
        self.requirements = requirements
        self.effects = effects
        self.add_to_memory = add_to_memory

        self.string_repr = string_repr

    '''====================================================================
    
    Base overrides

    ======================================================================='''
    def __repr__(self):
        #Return a 'pretty version' of the action
        return '%s: %s to %s' % (
            self.string_repr,
            self.source,
            self.target,
        )

    '''====================================================================
    
    Perform effects

    ======================================================================='''
    #Define general functions that multiple (or all) actions can or will use
    #TODO: Fix
    def action_meets_requirements(self,
        target=None,
        requirements=None):
        '''action_meets_requirements(self, target, requirements)
        ------------------------------------------
        This function takes in an optional target Entity (or object) and
        checks to see if the entity matches the passed in requirements.  
        If it does, it returns True - otherwise, it returns false'''
        #If this action has no requirements, return True
        if requirements is None:
            return True
        
        #Set the taget entity.  If 'target' is not passed in, we use self
        if target is None:
            target_to_check = self
        elif target is not None:
            target_to_check = target

        #Assume the requirements are met.  If we encounter something
        #   that doesn't meet requirements, set this as False and return
        meets_requirements = True
   
        #Now, check for requirements.  The target_to_check could be either
        #   an entity, object, or location, so we need to do different
        #   checks depending on the target type
        #-------------------------------
        #ENTITY Check
        #--------------------------------
        if isinstance(target_to_check, Entity.Entity):
            for requirement in requirements:
                #If the current requirement object is a dictionary
                if isinstance(requirements[requirement], dict):
                    #Loop through each item in the current requirement dict
                    for item in requirements[requirement]:
                        #--------------------
                        #Check for min and max values
                        #--------------------
                        if 'min' in item or 'max' in item:
                            #Min or max values are provided, so check on the
                            #   supplied value
                            if 'min' in item:
                                #Make sure to remove the min_ text
                                if target_to_check.__dict__[requirement][item.replace(
                                        'min', '').replace('_', '')] \
                                    < requirements[requirement][item]:
                                    meets_requirements = False
                                    break
                            elif 'max' in item:
                                #Make sure to remove the max_ text
                                if target_to_check.__dict__[requirement][item.replace(
                                        'max', '').replace('_','')] \
                                    > requirements[requirement][item]:
                                    meets_requirements = False
                                    break

                        #--------------------
                        #Min / max not specified, so assume min
                        #--------------------
                        elif 'min' not in item and 'max' not in item:
                            #There is no min or max, so assume it's a minimum
                            #   value
                            if target_to_check.__dict__[requirement][item] \
                                < requirements[requirement][item]:
                                meets_requirements = False
                                break

        return meets_requirements

    def perform(self):
        '''perform(self)
        ------------------------------------------
        This function performs the action'''
        #If this action has no effects, return True
        if self.effects is None:
            #This action doesn't have any effects, so we're done
            return True

        #-------------------------------
        #ENTITY Check
        #--------------------------------
        #Perform effects for each target in the self.effects list
        for target in self.effects:
            #Get the current target to do effects on
            target_to_use = self.effects[target]['target']

            #Update this target's memory, adding this action object
            if self.add_to_memory:
                target_to_use.memory.append(self)

            #Do specific things if the passed in target is an entity
            if isinstance(target_to_use, Entity.Entity):
                for effect in self.effects[target]:

                    #If the current key is 'target', continue on with the loop
                    #   because we explictly use the 'target' key to determine
                    #   which Entity should be affected
                    if effect == 'target':
                        continue

                    #------------------------
                    #If the current requirement object is a dictionary, 
                    #   simply add the provided values
                    #------------------------
                    if isinstance(self.effects[target][effect], dict):
                        #Loop through each item in the current dict
                        for item in self.effects[target][effect]:
                            target_to_use.__dict__[effect][item] \
                                += self.effects[target][effect][item]

                    #------------------------
                    #If the current item is 'network', we need to update
                    #   the Entity's network with the Entity provided and update
                    #   the value associated with that Entity
                    #------------------------
                    elif effect == 'network':
                        #The network will always be an array, but it may also be 
                        #   an array of arrays containing multiple Entitys to update
                        for network_items in self.effects[target][effect]:
                            #The first item will always be either an Entity, or a 
                            #   List
                            if isinstance(network_items, Entity.Entity):
                                #If the first item is an Entity, wrap it in a list
                                network_items = [ self.effects[target][effect][network_items] ]

                            #Now this should always occur
                            if isinstance(network_items, list):
                                try:
                                    #Update THIS Entity's network
                                    target_to_use.network[
                                        network_items[0].id][
                                        'value'] += network_items[1]
                                except KeyError:
                                    #Entity is not in this entity's network
                                    target_to_use.network[
                                        network_items[0].id] = {
                                            'entity': network_items[0],
                                            'value': network_items[1]}

                    #------------------------
                    #If the current requirement object is position,
                    #   update the entity's position.
                    #TODO: This code really applies to ANY list or
                    #   whatnot
                    #------------------------
                    elif effect == 'position':
                        target_to_use.__dict__[effect] = self.effects[target][effect]

        #We're done here
        return True

