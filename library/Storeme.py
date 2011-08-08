"""=============================================================================
    Story.py
    ------------
    Contains class definitions for Story related things.  For example, the 
    Storeme class represents the smallest unit of a story

    Stories that are generated here are recursive in nature.  Meaning that 
    a story generated may be part of a larger story, or parts of the story
    could be expanded and stories generated from them.  A storeme is the
    smallest unit of meaning in a story.  This could be something such as
    'Entity is a ____' where ____ is a profession (e.g., blacksmith).
    A storeme could also contain conflict,e.g. 'Entity rescues another entity'
    Multiple storemes create a story

============================================================================="""
"""=============================================================================

IMPORTS

============================================================================="""
import random 

"""=============================================================================

CLASS DEFINITION

============================================================================="""
class Storeme(object):
    '''A storeme is the smallest unit of meaning in a story.  For example, 
        a character's death could be a storeme.  It is an idea, or small group
        of ideas, that represent the smallest atomic bit of a story'''
    def __init__(self, *args, **kwargs):
        '''__init___
        ---------------------------------
        Set properties and call any initialization functions'''
        #Related entities.          
        #--------------------------------
        #Related entities is a list of all entities involved in the storeme
        #This may be null, as a storeme may not relate to
        #   an entity at all.  It accepts a tuple of related entity
        try:
            self.related_entities = kwargs['related_entities']
        except KeyError:
            self.related_entities = []

