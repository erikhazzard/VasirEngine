"""======================================================================== 
    Weapon.py
    -------------------------------------
    Contains logic for generating weapons.

   ========================================================================"""
"""=============================================================================

IMPORTS

============================================================================="""
import random 

"""=============================================================================

CLASS DEFINITION

============================================================================="""
class Weapon(object):
    def __init__(self, args, **kwargs):
        '''__init__
        ---------------------------------
        Sets up weapon attributes.  Generator function will provide attribute
        values'''
        #--------------------------------
        #   Entity Description
        #--------------------------------
        #Weapon name
        try:
            self.name = kwargs['name']
        except KeyError:
            self.name = self.generate_name()

        #Description
        try:
            self.description= kwargs['description']
        except KeyError:
            self.description = self.generate_description() 


