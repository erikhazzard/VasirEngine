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
#Standard python imports
import datetime
import math
import random 

#Other imports
import Race
import Goals

#Third party
import cairo_plot_new.cairoplot as CairoPlot
import cairo
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
    DEFAULT_PERSONA_ATTRIBUTE_VALUE = 0
    MIN_PERSONA_ATTRIBUTE_VALUE = -100
    MAX_PERSONA_ATTRIBUTE_VALUE = 100
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

        #------------------------------
        #Hunger
        #
        #Entities need nourishment.  Having a very high hunger value affects
        #   stats and possibly behavior.  Eating lowers hunger value
        #--------------------------------
        try:
            self.hunger = kwargs['hunger']
        except KeyError:
            #Pick a gender at random
            self.hunger = 0

        #=====================================================================
        #
        #   Entity Stats
        #
        #TODO: Comment
        #=====================================================================
        #Stats
        self.stats = {}
        
        #Agility
        try:
            self.stats['agility'] = kwargs['agility']
        except KeyError:
            self.stats['agility'] = 10
        
        #Dexterity
        try:
            self.stats['dexterity'] = kwargs['dexterity']
        except KeyError:
            self.stats['dexterity'] = 10
        
        #Intelligence
        try:
            self.stats['intelligence'] = kwargs['intelligence']
        except KeyError:
            self.stats['intelligence'] = 10

        #Stamina
        try:
            self.stats['stamina'] = kwargs['stamina']
        except KeyError:
            self.stats['stamina'] = 10

        #Strength
        try:
            self.stats['strength'] = kwargs['strength']
        except KeyError:
            self.stats['strength'] = 10
            
        #Wisdom
        try:
            self.stats['wisdom'] = kwargs['wisdom']
        except KeyError:
            self.stats['wisdom'] = 10

        #=====================================================================
        #
        #   Entity Description
        #
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
        #
        #   Negative values of attributes affect how much of the 'opposite' 
        #   value of the attribute the entity has.  For instance, -100 in
        #   'Openness' would mean the entity is NOT open and is very reserved
        #   and cautious
        #--------------------------------
        #Set up a base persona object
        #Define attributes, if any are passed in then use them
        self.persona = {}

        #Set default value
        try:
            self.DEFAULT_ATTRIBUTE_VALUE = kwargs['DEFAULT_ATTRIBUTE_VALUE']
        except KeyError:
            self.DEFAULT_ATTRIBUTE_VALUE = Entity.DEFAULT_PERSONA_ATTRIBUTE_VALUE 

        #--------------------------------
        #
        #Group 1: OPENNESS
        #
        #--------------------------------
        #(inventive/curious vs. consistent/cautious). Appreciation for art, 
        #   emotion, adventure, unusual ideas, curiosity, and variety of
        #   experience.  Openness is affects how much (to a degree) an 
        #   entity wants to experience new things. 
        try:
            self.persona['openness'] = kwargs['persona']['openness']
        except KeyError:
            self.persona['openness'] = self.DEFAULT_ATTRIBUTE_VALUE


        #--------------------------------
        #
        #Group 2: Conscientiousness 
        #
        #--------------------------------
        #Conscientiousness affects how much a character focuses on getting things
        #   done, to some extent - self discipline, acheivement based, etc.
        #   Low values would mean entity is more spontaneous
        try:
            self.persona['conscientiousness'] = kwargs['persona']['conscientious']
        except KeyError:
            self.persona['conscientiousness'] = self.DEFAULT_ATTRIBUTE_VALUE

        #--------------------------------
        #
        #Group 3: Extraversion 
        #
        #--------------------------------
        #Extraversion affects how much the entity desires to seek stimulation
        #   with other entities, how outgoing / energetic vs. how solitary /
        #   reserved they are
        try:
            self.persona['extraversion'] = kwargs['persona']['extraversion']
        except KeyError:
            self.persona['extraversion'] = self.DEFAULT_ATTRIBUTE_VALUE

        #--------------------------------
        #
        #Group 4: Agreeableness 
        #
        #--------------------------------
        #Agreeableness affects the entity's ability to relate to other entities
        #   Lower values mean entity tends to be suspicious of other entities /
        #   unkind or cold
        try:
            self.persona['agreeableness'] = kwargs['persona']['agreeableness']
        except KeyError:
            self.persona['agreeableness'] = self.DEFAULT_ATTRIBUTE_VALUE

 
        #--------------------------------
        #
        #Group 5: Neuroticism 
        #
        #--------------------------------       
        #Neuroticism affects how an entity experiences unpleasent emotions
        #   easily - such as anger, axiety, depression, etc.  
        #   This affects secure / confidence vs. sensitive / nervousness
        try:
            self.persona['neuroticism'] = kwargs['persona']['neuroticism']
        except KeyError:
            self.persona['neuroticism'] = self.DEFAULT_ATTRIBUTE_VALUE

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
        #
        #   History (Memory / events that have occured to entity)
        #
        #=====================================================================
        #
        #   The entity must keep track of all events it has experienced, i.e.
        #   have a sort of memory.  Certain events may affect personality 
        #   attributes or relationships with other entities.  
        #   
        #   There is an Storeme (event) class which events derive from, and instances of
        #   the Storeme class are stored in a list here
        #
        #--------------------------------
        self.history = []

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
        #   Entity's Goals
        #=====================================================================
        #
        #   Entity is goal based, so grab the goals by calling the entity's
        #   get_goals func
        #--------------------------------
        self.goals = self.get_goals()

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
Stats: %s
Persona: %s
Goals: %s
        ''' % (
        self.get_id(),
        self.get_name(),
        self.stats,
        self.persona,
        self.goals,
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
    #   Get Goals
    #
    #=====================================================================
    def get_goals(self):
        '''get_goals(self)
        ---------------------------------
        Get goals for the entity based on their persona values, pulls in
        from Goals.py'''
        #Get copy of goals
        goals = Goals.GOALS
        
        #This will be the dict object that we return which will contain
        #   goals and their weights (e.g. {'goal': {'weight': 0.8}} )
        entity_goals = {}

        #Loop through each goal
        for goal in goals:
            #If persona values are in range, add this goal to the entity's
            #   goal dict
            add_to_goals = True 
            for attribute in goals[goal]['persona']:
                if self.persona[attribute] >= goals[goal]['persona'][
                    attribute][0] \
                    and self.persona[attribute] <= goals[goal]['persona'][
                    attribute][1]:
                    pass
                else:
                    add_to_goals = False
            if add_to_goals is True:
                entity_goals[goal] = {'test': 42}

        #return entity_goals dict
        return entity_goals
            

    #=====================================================================
    #
    #   print persona graph
    #
    #=====================================================================
    def visualize_persona(self, other_entity=None):
        '''visual_persona(self, other_entity)
        ---------------------------------
        This function will visualize the persona of this entity.  Right
        now, we'll just print an ASCII bar graph
        
        If other entity_entity is passed in, this will print a scattor plot
        with both entity values'''

        #--------------------------------
        #Print bar graph of self persona
        #--------------------------------
        if other_entity is None:
            #Line chart
            CairoPlot.dot_line_plot(
                'cairo_output/self_line_plot.png', 
                data={'self': [self.persona[i] for i in self.persona]},
                width=800,
                height=600,
                series_colors='blue_darkblue',
                x_labels = [i for i in self.persona],
                y_bounds = (Entity.MIN_PERSONA_ATTRIBUTE_VALUE,
                            Entity.MAX_PERSONA_ATTRIBUTE_VALUE),
                axis=True,
                grid=True,
                dots=5)
            #Bar plot
            CairoPlot.vertical_bar_plot(
                'cairo_output/self_bar_plot.png', 
                data={'self': [self.persona[i] for i in self.persona]},
                width=800,
                height=600,
                x_labels = [i for i in self.persona],
                grid=True,
                y_bounds = (
                    Entity.MIN_PERSONA_ATTRIBUTE_VALUE, 
                    Entity.MAX_PERSONA_ATTRIBUTE_VALUE),)
            #Pie chart
            CairoPlot.pie_plot(
                'cairo_output/self_pie_plot.png',
                #The data
                data=self.persona,
                width=800,
                height=600)


        #--------------------------------
        #Print scattor plot with other entity
        #--------------------------------
        else:
            #Get persona list that both entities share
            attribute_list = []
            for i in self.persona:
                if i in other_entity.persona:
                    attribute_list.append(i)

            #Line chart
            CairoPlot.dot_line_plot(
                'cairo_output/entity_comparison_line_chart.png', 
                data={
                    'self': [self.persona[i] for i in self.persona],
                    'other_entity': [other_entity.persona[i] \
                        for i in other_entity.persona],
                },
                width=800,
                height=600,
                series_colors='blue_darkblue',
                x_labels = ['%s' % (i) for i in self.persona],
                y_bounds = (
                    Entity.MIN_PERSONA_ATTRIBUTE_VALUE,
                    Entity.MAX_PERSONA_ATTRIBUTE_VALUE),
                axis=True,
                grid=True,
                dots=5)
            #Scatter chart
            CairoPlot.scatter_plot(
                'cairo_output/entity_comparison_scatter_plot.png', 
                data={
                    'similarity = %s' % (
                        self.get_similarity(other_entity)): [(self.persona[i],
                            other_entity.persona[i]) for i in attribute_list],
                },
                series_colors='blue_darkblue',
                series_legend=True,
                width=800,
                height=600,
                y_bounds = (
                    Entity.MIN_PERSONA_ATTRIBUTE_VALUE,
                    Entity.MAX_PERSONA_ATTRIBUTE_VALUE),
                x_bounds = (
                    Entity.MIN_PERSONA_ATTRIBUTE_VALUE,
                    Entity.MAX_PERSONA_ATTRIBUTE_VALUE),
                axis=True,
                dots=5,
                discrete=True,
                grid=True,)

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
        random.seed(datetime.datetime.now())
        for attribute in self.persona:
            self.persona[attribute] = random.randint(
                Entity.MIN_PERSONA_ATTRIBUTE_VALUE,
                Entity.MAX_PERSONA_ATTRIBUTE_VALUE)


    #=====================================================================
    #
    #   compare this entity with another
    #
    #=====================================================================
    def get_similarity(self, other_entity=None):
        '''get_similarity(self, other_entity)
        ---------------------------------
        This function takes in itself and other_entity (an Entity object). It
        uses Pearson correlation to determine how similar this an another 
        entity are.  1 is perfectly similar, 0 is not at all'''
        if other_entity is None:
            return 'Other Entity must be provided'

        #Get attributes shared by both entities (should be every attribute now,
        #   but certain entities may lack attributes in the future)
        attribute_list = {}
        for i in self.persona:
            if i in other_entity.persona:
                attribute_list[i] = 1
            
        #Get sum of all preferences for both entities
        ent1_sum = sum([self.persona[i] for i in attribute_list])
        ent2_sum = sum([other_entity.persona[i] for i in attribute_list])
    
        #Sum up the squares
        ent1_sum_sq = sum([pow(self.persona[i],2) for i in attribute_list])
        ent2_sum_sq = sum([pow(other_entity.persona[i],2) for i in attribute_list])

        #Sum the products
        product_sum = sum([self.persona[i] * other_entity.persona[i] \
            for i in attribute_list])

        #Calculate the Pearson score
        attr_len = len(attribute_list)
        pearson_numerator = product_sum - (ent1_sum * ent2_sum / attr_len)
        pearson_den = math.sqrt((ent1_sum_sq - pow(ent1_sum,2) / attr_len) \
            * (ent2_sum_sq - pow(ent2_sum,2) / attr_len))

        if pearson_den == 0:
            return 0
        else:
            pearson_value = pearson_numerator / pearson_den
            return pearson_value

