"""=============================================================================
    Race.py
    ------------
    Contains the Race class definition.  Controls what
    races (creatures / entity types) are available, and how the race affects
    interactions with other entities
============================================================================="""
"""=============================================================================

IMPORTS

============================================================================="""
import random 

"""=============================================================================

CLASS DEFINITIONS

============================================================================="""
class Race(object):
    '''Race Class
    -------------------------------------
    Contains logic for how races affect entities'''
    def __init__(self, *args, **kwargs):
        self.name = 'Elf'
