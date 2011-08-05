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
import Race

"""=============================================================================

CLASS DEFINITIONS

============================================================================="""
class Entity(object):
    '''Entity Class
    -------------------------------------
    The Entity class controls all the logic for creating and interacting with 
    entities (characters, creatures, etc.).  When instaniating an Entity object
    we can pass in persona, name, etc. values OR have the entity automatically
    generate those attributes for us.  By default, it will automatically 
    generate values'''
    #Keep a count of how many entities have been created
    _entity_created_count = 0
    #_entity_objects will be a dict of all created entity objects, represented
    #   by their ID and the value being the object itself
    _entity_objects = {}

    #Store gender values
    GENDER = (
        (0, 'Male'),
        (1, 'Female'),
    )
    #=====================================================================
    #
    #   Entity Description
    #
    #=====================================================================
    def __init__(self, *args, **kwargs):
        '''init
        ---------------------------------
        Create an entity.  Various parameters can be passed in to override
        default attributes.  Init sets up the entity's attributes and
        other initialization processes'''
        #=====================================================================
        #   Entity ID
        #=====================================================================
        #Generate a random ID.  TODO: Use hash?
        self.id = 'entity_%s_%s' % (
            #First parameter is the current count of how many entityies have 
            #   been created
            Entity._entity_created_count,
            #Second parameters is a more or less random string
            ''.join([random.choice(
            'abcdefghijklmnopqrstuvwxyz0123456789'
            ) for i in \
            range(18)]))
    
        #=====================================================================
        #
        #   Entity Description
        #
        #=====================================================================
        #Entity's name
        try:
            self.name = kwargs['name']
        except KeyError:
            self.name = self.generate_name()
        #=====================================================================
        #   Characteristics
        #=====================================================================
        #
        #   Characteristics define certain properties of the entity that are 
        #   more or less not affected by outside influences - attribtues such
        #   as age, race, gender, skin color, etc.
        #
        #--------------------------------
        #Age
        #
        #Age is how old the entity is.  While age isn't something that is
        #   affected by external influences (like personality is), it can 
        #   affect how other entities perceive this entity.  Age also affects
        #   the value of certain persona attributes (like in real life, 
        #   certain people mature with age.  Also like in real life, age does 
        #   not always critically affect persona - here, age is more or less a
        #   weight, or a heueristic, for determing persona atrributes)
        #--------------------------------
        try:
            self.age = kwargs['age']
        except KeyError:
            self.age = random.randint(0,120)

        #------------------------------
        #Race
        #
        #Race determines which type of entity the entity is - for example,
        #   elf, human, dwarf, etc.  The race is an object from the Race class,
        #   so we can specify the possible races and how they affect other
        #   entites (by modifying the Race class)
        #--------------------------------
        try:
            self.race = kwargs['race']
        except KeyError:
            self.race = Race.Race()

        #------------------------------
        #Gender
        #
        #Specifies if the entity is male or female.  Gender can affect how
        #   other entities interact with this entity.  Procreation is also
        #   a desire to take into consideration
        #--------------------------------
        try:
            self.gender = kwargs['gender']
        except KeyError:
            #Pick a gender at random
            self.gender = Entity.GENDER[
                random.randint(0, 1)]

        #=====================================================================
        #   Persona
        #=====================================================================
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
        #Randomize persona values? If nothing is passed is, then we
        #   assume we DO want ranomized persona values
        try:
            #randomize_persona can be either True or False
            randomize_persona = kwargs['randomize_persona']
        except KeyError:
            randomize_persona = True
        
        #If randomize_persona is true, call the class method which
        #   will randomize persona values
        if randomize_persona is True:
            self.randomize_persona()

        #=====================================================================
        #   Entity's Network
        #=====================================================================
        #
        #   The entity's NETWORK consists of other entities that this entity
        #   has knowledge of or has some sort of connection with.  Entities
        #   can be known through their connections with other entities (i.e.,
        #   six degrees of separation).  
        #
        #   The data structure will be such that the key will be some entity
        #   object and the value will be information about the relationship
        #
        #   e.g. { 'id': { 'entity': <obj>, 'attitude': <int> } }
        #--------------------------------
        #TODO: Figure out what kind of variables to use
        self.network = {}
        #Example:
        #   self.network = {
        #       'entity_0_zxc42': {
        #           'entity': Entity._entity_objects['entity_0_zxc42'],
        #           'attitude': 129,
        #       }
        #   }

        #=====================================================================
        #   Finalize Entity
        #=====================================================================
        #Increase the _entity_created_count value
        Entity._entity_created_count += 1

        #Add this entity to the list of entities created
        Entity._entity_objects[self.id] = self


    '''====================================================================
    
    Class Methods

    ======================================================================='''
    #=====================================================================
    #
    #   Built-in overrides
    #   ---------------------------------
    #   Functions that overwrite or extend built in behavior
    #
    #=====================================================================
    def __repr__(self):
        return '''
ID: %s
Name: %s
Persona: %s
        ''' % (
        self.get_id(),
        self.get_name(),
        self.persona,
        )
    #=====================================================================
    #
    #   getter functions
    #   ---------------------------------
    #   Functions whose purpose is to get various attributes
    #
    #=====================================================================
    def get_id(self):
        '''get_id(self)
        ---------------------------------
        Returns the ID of the entity'''
        return self.id
    def get_name(self):
        '''get_name(self)
        ---------------------------------
        Returns the name of the entity'''
        return self.name
    
    #=====================================================================
    #
    #   randomize_persona
    #
    #=====================================================================
    def randomize_persona(self):
        '''randomize_persona(self)
        ---------------------------------
        This method goes through each persona attribute and assigns a random
        value to it'''
        for attribute in self.persona:
            self.persona[attribute] = random.randint(0, 500)

    #=====================================================================
    #
    #   generate_name
    #
    #=====================================================================
    def generate_name(self):
        '''generate_name(self)
        ---------------------------------
        This method randomly generates a name for the entity'''
        name = [random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in \
            range(random.randint(2,18))]
        name = ''.join(name)
        name = name[0] + name[1:].lower()
        return name
