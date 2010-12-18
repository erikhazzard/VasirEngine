"""=============================================================================
    Entity.py
    ------------
    Contains the entity class definition.  An entity could be a character, 
    monster, etc. The various attributes affect how the entity interacts
    with the world and other entities.
============================================================================="""
"""=============================================================================

IMPORTS

============================================================================="""
import random 

"""=============================================================================

CLASS DEFINITION

============================================================================="""
class Entity(object):
    def __init__(self, *args, **kwargs):
        '''init
        ---------------------------------
        Create an entity.  Various parameters can be passed in to override
        default attributes.  Init sets up the entity's attributes and
        other initialization processes'''
        #--------------------------------
        #   Entity Description
        #--------------------------------
        #Entity's name
        try:
            self.name = kwargs['name']
        except KeyError:
            self.name = [random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in \
                range(random.randint(2,18))]
            self.name = ''.join(self.name)
            self.name = self.name[0] + self.name[1:].lower()
        #--------------------------------
        #   Persona
        #
        #   The persona is based on five 'personality' traits as observed by
        #   psychologists.  They are Openness, Conscientiousness, Extraversion,
        #   Agreeableness, and Neuroticism.  These are the five 'groups', which
        #   have further subproperties.  Events affect the values of the
        #   personality properties
        #   
        #   Attributes alone will not always determine what actions an entity
        #   does.  Sometimes an entity may do things completely outside their
        #   normal behavior, and these events would affect their attributes.
        #--------------------------------
        #Set up a base persona object
        #Define attributes, if any are passed in then use them
        self.persona = {}

        #Set default value
        try:
            self.DEFAULT_ATTRIBUTE_VALUE = kwargs['DEFAULT_ATTRIBUTE_VALUE']
        except KeyError:
            self.DEFAULT_ATTRIBUTE_VALUE = 100

        #--------------------------------
        #
        #Group 1: OPENNESS
        #
        #--------------------------------
        #Curosity (Opposite: Cautious)
        #--------------------------------
        #Curiosity affects how much, to some degree, an entity wants to
        #   experience new things. 
        try:
            self.persona['curiosity'] = kwargs['persona']['curiosity']
        except KeyError:
            self.persona['curiosity'] = self.DEFAULT_ATTRIBUTE_VALUE
        
        #Inventive (Opposite: Consistent)
        #--------------------------------
        #Inventive affects, to some degree, how much an entity desires to
        #   create and try new things.  Related to curiosity to some degree
        try:
            self.persona['inventive'] = kwargs['persona']['inventive']
        except KeyError:
            self.persona['inventive'] = self.DEFAULT_ATTRIBUTE_VALUE

        #LOGIC
        #--------------------------------
        #Logic affects how much an entity plans out their decisions, and
        #   how, to some degree, the entity is open to changing attributes
        #   and viewpoints.  Too much logic can, to some degree, cause 
        #   decision paralysis and lack of action
        try:
            self.persona['logic'] = kwargs['persona']['logic']
        except KeyError:
            self.persona['logic'] = self.DEFAULT_ATTRIBUTE_VALUE

        #--------------------------------
        #
        #Group 2: Conscientiousness 
        #
        #--------------------------------
        #Efficient (Opposite: Easy-going)
        #--------------------------------
        #Efficient affects how much a character focuses on getting things
        #   done, to some extent.  Exteremely efficient entities may
        #   affect the perception that entities have of them to a negative
        #   degree, for instance.
        try:
            self.persona['efficient'] = kwargs['persona']['efficient']
        except KeyError:
            self.persona['efficient'] = self.DEFAULT_ATTRIBUTE_VALUE

        #Organized (Opposite: Care less)
        #--------------------------------
        #Organized affects how much a character likes structure and order,
        #   to some degree.
        try:
            self.persona['organized'] = kwargs['persona']['organized']
        except KeyError:
            self.persona['organized'] = self.DEFAULT_ATTRIBUTE_VALUE

        #--------------------------------
        #
        #Group 3: Extraversion 
        #
        #--------------------------------
        #Outgoing (Opposite: Shy)
        #--------------------------------
        try:
            self.persona['outgoing'] = kwargs['persona']['outgoing']
        except KeyError:
            self.persona['outgoing'] = self.DEFAULT_ATTRIBUTE_VALUE

        #Energetic (Opposite: Reserved)
        #--------------------------------
        try:
            self.persona['energetic'] = kwargs['persona']['energetic']
        except KeyError:
            self.persona['energetic'] = self.DEFAULT_ATTRIBUTE_VALUE

        #--------------------------------
        #
        #Group 4: Agreeableness 
        #
        #--------------------------------
        #Friendly (Opposite: Cold)
        #--------------------------------
        try:
            self.persona['friendly'] = kwargs['persona']['friendly']
        except KeyError:
            self.persona['friendly'] = self.DEFAULT_ATTRIBUTE_VALUE

        #Empathy / Compassion (Opposite: Unkind)
        #--------------------------------
        #Empathy affects the entity's ability to relate to other entities
        #   It affects, to some degree, how this entity's attributes can
        #   change based on interactions with other entities.  
        try:
            self.persona['empathy'] = kwargs['persona']['empathy']
        except KeyError:
            self.persona['empathy'] = self.DEFAULT_ATTRIBUTE_VALUE

 
        #--------------------------------
        #
        #Group 5: Neuroticism 
        #
        #--------------------------------       
        #Sensitive (Opposite: Secure)
        #--------------------------------
        try:
            self.persona['sensitive'] = kwargs['persona']['sensitive']
        except KeyError:
            self.persona['sensitive'] = self.DEFAULT_ATTRIBUTE_VALUE


        #Confident (Opposite: Nervous)
        #--------------------------------
        try:
            self.persona['confident'] = kwargs['persona']['confident']
        except KeyError:
            self.persona['confident'] = self.DEFAULT_ATTRIBUTE_VALUE

        #GREED
        #--------------------------------
        #Greed affects how much an entity wants things and, to some degree,
        #   the lengths it will go to obtain them
        try:
            self.persona['greed'] = kwargs['persona']['empathy']
        except KeyError:
            self.persona['greed'] = self.DEFAULT_ATTRIBUTE_VALUE

        '''------------------------------
            Set up function calls
            -----------------------------'''
        #Randomize persona values?
        try:
            #randomize_persona can be either True or False
            randomize_persona = kwargs['randomize_persona']
        except KeyError:
            randomize_persona = True
        
        if randomize_persona is True:
            self.randomize_persona()



    '''--------------------------------------------------------------------
    
    Class Methods

    -----------------------------------------------------------------------'''
    def randomize_persona(self):
        '''randomize_persona(self)
        ---------------------------------
        This method goes through each persona attribute and assigns a random
        value to it'''
        for attribute in self.persona:
            self.persona[attribute] = random.randint(0, 500)
        
            
