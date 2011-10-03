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

#Actions Entity will inherit / can perform 
import Action

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
    #_entities will be a dict of all created entity objects, represented
    #   by their ID and the value being the object itself
    _entities = {}

    #Store gender values
    GENDER = (
        (0, 'Male'),
        (1, 'Female'),
    )
    DEFAULT_PERSONA_ATTRIBUTE_VALUE = 0
    MAX_PERSONA_ATTRIBUTE_VALUE = 100
    MIN_PERSONA_ATTRIBUTE_VALUE = -MAX_PERSONA_ATTRIBUTE_VALUE

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
        #   Entity ID
        #=====================================================================
        #Generate a random ID.  TODO: Use hash?
        self.id = 'entity_%s_%s' % (
            #First parameter is the current count of how many entityies have 
            #   been created
            Entity._entity_created_count,
            #And their name
            self.name,)

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

        #------------------------------
        #Restedness
        #
        #How tired the entity is.  The more tired an entity is, the more sleep
        #   or rest it needs to become less tired.  Tiredness can affect stats
        #   and persona (more tired, less alert)
        #--------------------------------
        try:
            self.restedness = kwargs['restedness']
        except KeyError:
            #Pick a gender at random
            self.restedness = 0

        #TODO: States / Emotions? (e.g., sleeping, attacking, and angry, etc.)

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
        #   Wealth / Money
        #=====================================================================
        try:
            self.money = kwargs['money']
        except KeyError:
            self.money = random.randint(-10000,10000)

        #=====================================================================
        #
        #   Entity Persona / Psychology
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
        #   Memory (actions that have occured to entity)
        #=====================================================================
        #
        #   The entity must keep track of all actions it has experienced, i.e.
        #   have a sort of memory.  Certain events may affect personality 
        #   attributes or relationships with other entities.  
        #   
        #--------------------------------
        self.memory = []

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
        #           'entity': Entity._entities['entity_0_zxc42'],
        #           'attitude': 129,
        #       }
        #   }

        #=====================================================================
        #   Mood / Emotional State
        #=====================================================================
        #The Entity's mood affects their persona values (temporarily).  Persona
        #   values affect how easily an Entity gets into a particular mood
        self.mood = {}

        #=====================================================================
        #   Entity's Goals
        #=====================================================================
        #
        #   Entity is goal based, so grab the goals by calling the entity's
        #   get_goals func
        #--------------------------------
        self.goals = self.get_goals()


        #=====================================================================
        #
        #   Entity - Geographic Properties
        #
        #
        #=====================================================================
        #Store the position of the Entity.  Depending on how we generate
        #   geography, this may change.  For now, we'll assume a three
        #   deminsional cartesian space
        #Store as x,y,z
        #   TODO: For now, we'll always assume z is 0
        #   TODO: Entities can't be directly on top of each other (occupy same
        #   same space)
        self.position = [
            random.randint(0,20),
            random.randint(0,20),
            0]

        #=====================================================================
        #   Target
        #=====================================================================
        #The entity's current target
        #   Should be set either as None, a single Entity object, or a list
        #   of Entities
        self.target = None

        #=====================================================================
        #   Finalize Entity
        #=====================================================================
        #Increase the _entity_created_count value
        Entity._entity_created_count += 1

        #Add this entity to the list of entities created
        Entity._entities[self.id] = self


    '''====================================================================
    
    Class Methods

    ======================================================================='''
    #=====================================================================
    #
    #   Built-in overrides
    #
    #=====================================================================
    def __repr__(self):
        return '''< %s >''' % (self.id)

    def print_info(self):
        print '''
ID: %s
Name: %s
Target: %s

Gender: %s
Position: %s
Money: %s

Stats: %s

Persona: %s

Goals: %s

Network: %s
        ''' % (
        self.id,
        self.name,
        self.target,
        self.gender[1],
        self.position,
        self.money,
        self.stats,
        self.persona,
        self.print_goals(),
        self.print_network(),
        )

    def get_info_json(self):
        '''get_info_json:
        -----------------
        Returns a JSON string containing the entity info, similar to print_info
        but in a JSON friendly format'''
        #Try to get target
        if self.target is None:
            target = 'undefined'
        else:
            target = "'%s'" % (self.target.id)

        return '''({
            id: '%s',
            name: '%s',
            target: %s,
            gender: '%s',
            position: [%s, %s, %s],
            money: %s,
            stats: %s,
            persona: %s,
            goals: %s,
            network: %s
        })''' % (
            self.id,
            self.name,
            target,
            self.gender[1],
            self.position[0],
            self.position[1],
            self.position[2],
            self.money,
            self.stats,
            self.persona,
            self.print_goals(),
            self.print_network(),
        )

    #=====================================================================
    #
    #   getter functions
    #
    #=====================================================================
    def print_goals(self):
        '''print_goals(self):
        ---------------------------------
        Prints the goals in an easier to read way, useful for __repr__'''
        #Add a space so the { won't get trimmed
        goal_string = '{ '
        for goal in self.goals:
            goal_string += '''\t'%s': %s \n,''' % (
                goal, self.goals[goal]['priority'],
            )
        #Remove trailing comma and add a }
        goal_string = goal_string[:-1] + '}'
        return goal_string
    
    def print_network(self):
        '''print_network(self):
        ---------------------------------
        Prints the network in an easier to read way, useful for __repr__'''
        #Add a space so the { won't get trimmed
        network_string = '{ '
        for network in self.network:
            network_string += '''\t'%s': %s \n,''' % (
                network, self.network[network]['value']
            )
        #Remove trailing comma and add a }
        network_string = network_string[:-1] + '}'
        return network_string

    '''--------------------------------------------------------------------
    Utility Functions
    -----------------------------------------------------------------------'''
    def get_attribute_value(self,
        dict_key=None, 
        dict_key_2=None,
        dict_key_3=None,
        alternative_return_value=None):
        '''Takes in possible keys / values to look up from the Entity
        and returns the value if it is found.  If it is NOT found,
        it will return the alternative_return_value'''

        #Get the dict representation of the entity and return the 
        #   disired value from the passed in parameters
        ret_value = alternative_return_value

        if dict_key is not None:
            #First key passed in
            try:
                ret_value = self.__dict__[dict_key]
            except KeyError:
                ret_value = alternative_return_value
            if dict_key_2 is not None:
                #Second key passed in key passed in
                try:
                    ret_value = self.__dict__[dict_key][dict_key_2]
                except KeyError:
                    ret_value = alternative_return_value
                if dict_key_3 is not None:
                    #Third key passed in
                    try:
                        ret_value = self.__dict__[dict_key][dict_key_2][dict_key_3]
                    except KeyError:
                        ret_value = alternative_return_value
        #return it
        return ret_value

    '''=====================================================================
    
       Get Goals
    
    ======================================================================='''
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
            #We also need to keep a list of percentages that represent
            #   how 'close' a persona value is to the range of possible
            #   persona values from the goal.  For instance, if a
            #   goal has a persona attribute 'openness' range from (20, 80)
            #   and the Entity's openness value is 40, the closeness would be
            #   33%.  If the goal has multiple persona attributes, each % value
            #   is added to the current_persona_closeness list
            #TODO: Determine the 'range' of closeness
            current_persona_closeness = []
            for attribute in goals[goal]['persona']:
                #A goal will likely have multiple persona attributes, so
                #   if the Entity does NOT fall in range of even one of them,
                #   they won't get the goal.  We'll use a variable called
                #   add_to_goals to keep track if the goal can be added
                #   or not.  The first time a persona value does not fall
                #   within the proper range, this will be set to false.

                #Get current attribute's goal persona min and max bounds
                #   Use MAX value for both, because the MIN value is always negative.
                #   We don't want to potentially multiple two negatives which would give
                #   an undesired positive
                cur_attribute_min_bound = (Entity.MAX_PERSONA_ATTRIBUTE_VALUE \
                        * goals[goal]['persona'][attribute][0])
                cur_attribute_max_bound = (Entity.MAX_PERSONA_ATTRIBUTE_VALUE \
                        * goals[goal]['persona'][attribute][1])
                
                #For each attribute of the persona dict in the current goal,
                #   check if the entity's persona values are in range.  
                if self.persona[attribute] >= cur_attribute_min_bound \
                    and self.persona[attribute] <= cur_attribute_max_bound:
                    #The goal values in GOALS dict are percentages, so get
                    #   the actual value from the max / min values.
                    #If the current persona attribute value is within
                    #   the valid percentage range, then grab the 'closeness'
                    #Percentage is 100 * (x-a)/(b-a), where a and b are the
                    #   interval to check against (in this case, the goal's
                    #   persona attribute value range)
                    closeness = ( 100 * (
                        (self.persona[attribute] - cur_attribute_min_bound) / (
                        cur_attribute_max_bound - cur_attribute_min_bound)))
                    #Now that we have the closeness value, we need to figure
                    #   out on which 'side' the closeness value is on.  If 
                    #   a goal has a value range of (-100, 40) then the -100
                    #   is more important since it is higher, so the closness
                    #   needs to be inverted (by default, the closeness is
                    #   always how much % it is to B, which is the second value
                    #   in the range of values)
                    #Get absolute value to compare ranges
                    if abs(cur_attribute_min_bound) \
                        > abs(cur_attribute_max_bound):
                        #If the min bound absolute value is bigger than the max
                        #   bound, the interval range [a,b] should really be
                        #   reversed to [b,a], which means the closeness needs
                        #   to be inverted
                        closeness = 100 - closeness
                    elif abs(cur_attribute_min_bound) \
                        == abs(cur_attribute_max_bound):
                        #If the min_bound and max_bound equal each other, the
                        #   closeness value is irrelevant
                        #When weighing goals, if closeness has a value of none
                        #   then the weight of this attribtue in determining
                        #   the overall goal weight will be irrelevant, and be
                        #   randomized
                        closeness = None
                        

                    #Add closeness to the current_persona_closeness list
                    current_persona_closeness.append(closeness)

                else:
                    #Otherwise, this is not a goal the entity has
                    add_to_goals = False

            if add_to_goals is True:
                #Add this goal to the Entity's stored goals.  Add a weight
                #   to it, which will affect how badly this Entity wants
                #   to pursue this goal in relation to their other goals
                entity_goals[goal] = {'closeness': current_persona_closeness}

        #--------------------------------
        #Get priority of goals
        #--------------------------------
        #Now, loop through the goals we just defined for this entity and
        #   set the priority for each goal
        for goal in entity_goals:
            #Get average of closeness values
            closeness_average = sum(entity_goals[goal]['closeness']) / len(
                entity_goals[goal]['closeness'])
            #Store average closeness
            entity_goals[goal]['closeness_average'] = closeness_average
        #Now get the combined values of the averages for all goals
        combined_goal_average = [entity_goals[goal]['closeness_average'] for \
            goal in entity_goals]
        
        #Get sum of the combined goal average
        combined_goal_average = sum(combined_goal_average)
        #Now we need to divide 100 by this so we can assign proper values
        #   for the 'weight' each goal has, percentage wise, out of 100
        if combined_goal_average == 0:
            combined_goal_average = 100.0

        goal_value_modifier = 100.0 / combined_goal_average
        #Finally, set the 'priority', or a weight, for each goal based on this 
        #   modifier and it's previous closeness averages
        for goal in entity_goals:
            entity_goals[goal]['priority'] = entity_goals[goal][
                'closeness_average'] * goal_value_modifier

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
            '''
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
            '''

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
                'cairo_output/entity_comparison_scatter_plot_persona.png', 
                data={
                    'similarity = %s' % (
                        self.get_similarity_persona(other_entity)): [(self.persona[i],
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

            #Goals
            #Get persona list that both entities share
            attribute_list = []
            for i in self.goals:
                attribute_list.append(i)
            for i in other_entity.goals:
                attribute_list.append(i)
            CairoPlot.scatter_plot(
                'cairo_output/entity_comparison_scatter_plot_goals.png', 
                data={
                    'similarity = %s' % (
                        self.get_similarity_goals(other_entity)): [(
                            self.get_attribute_value(
                                'goals', i, 'closeness_average',
                                alternative_return_value=0),
                            other_entity.get_attribute_value(
                                'goals', i, 'closeness_average',
                                alternative_return_value=0)) for i in attribute_list],
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
    #   get_persona_similairty
    #   ----------------------
    #   This returns a value that represents the similarity of the two 
    #   entities based on their persona
    #
    #=====================================================================
    def get_similarity(self,
        other_entity=None,
        dict_key_1='persona',
        dict_key_2=None,
        dict_key_3=None,
        values_exist_for_both=True):
        '''get_similarity(self, 
            other_entity,dict_key_1, dict_key_2,dict_key_3,
            values_exist_for_both)
        ---------------------------------
        This function takes in itself and other_entity (an Entity object). It
        uses Pearson correlation to determine how similar this an another 
        entity are based on their goals.  1 is perfectly similar, 0 is not at all.
        
        It also takes in 3 dict keys, which are used to specify what attributes
        of the entity we should compare. The values_exist_for_both parameter
        specifies if values MUST exist for both entities before checking (
        this is required for persona, but not for goals)'''
        if other_entity is None:
            return 'Other Entity must be provided'

        #TODO: Should we use closeness_average or priority?

        #Get ALL the goals shared between the two entities.  We do this because
        #   if entities do not have the same goals, they are not as similar, so we
        #   DO need to take into account goals that entities do not share.
        #If an entity does not have a goal the other entity does, the value will be
        #   stored as 0.  This makes sense too - if an entity has some goal X that
        #   has a very low closeness average, it's almost like not have the goal
        #TODO: Does this give invalid results though?  If entity A has one goal
        #   with a really high priority, but entity B has 10 goals with 10% 
        #   priority each, does it ruin the results?
    
        #
        if values_exist_for_both is True:
            attribute_list = {}
            for i in self.persona:
                if i in other_entity.persona:
                    attribute_list[i] = 1
        else:
            attribute_list = []
            for i in self.goals:
                attribute_list.append(i)
            for i in other_entity.goals:
                attribute_list.append(i)

        #Get sum of values for both entities
        ent1_sum = sum([self.get_attribute_value(
            dict_key_1, i, dict_key_3, 
            alternative_return_value=0) for i in attribute_list])
        ent2_sum = sum([other_entity.get_attribute_value(
            dict_key_1, i, dict_key_3,
            alternative_return_value=0) for i in attribute_list])
    
        #Sum up the squares
        ent1_sum_sq = sum([pow(self.get_attribute_value(
            dict_key_1, i, dict_key_3, 
            alternative_return_value=0) 
            ,2) for i in attribute_list])

        ent2_sum_sq = sum([pow(other_entity.get_attribute_value(
            dict_key_1, i, dict_key_3, 
            alternative_return_value=0)
            ,2) for i in attribute_list])

        #Sum the products
        product_sum = sum([self.get_attribute_value(
            dict_key_1, i, dict_key_3, 
            alternative_return_value=0) \
            *  other_entity.get_attribute_value(
            dict_key_1, i, dict_key_3, 
            alternative_return_value=0)\
            for i in attribute_list])

        #Calculate the Pearson score
        attr_len = len(attribute_list)
        pearson_numerator = product_sum - (ent1_sum * ent2_sum / attr_len)
        pearson_den = math.sqrt((ent1_sum_sq - pow(ent1_sum,2) / attr_len) \
            * (ent2_sum_sq - pow(ent2_sum,2) / attr_len))

        if pearson_den == 0:
            if pearson_numerator == 0:
                #If both values are 0, it means everything is exactly the same
                #   so return 1
                return 1
            else:
                return 0
        else:
            pearson_value = pearson_numerator / pearson_den
            return pearson_value

    #-------------------------------------------------------------------------
    #get persona similarity
    #-------------------------------------------------------------------------
    def get_similarity_persona(self, other_entity=None):
        '''get_similarity_persona(self, other_entity)
        ---------------------------------
        this function takes in itself and other_entity (an entity object). it
        uses pearson correlation to determine how similar this an another 
        entity are based on persona.  1 is perfectly similar, 0 is not at all'''
        return self.get_similarity(
            other_entity=other_entity,
            dict_key_1='persona',)
    
    #-------------------------------------------------------------------------
    #get stat similarity
    #-------------------------------------------------------------------------
    def get_similarity_stats(self, other_entity=None):
        '''get_similarity_persona(self, other_entity)
        ---------------------------------
        this function takes in itself and other_entity (an entity object). it
        uses pearson correlation to determine how similar this an another 
        entity are based on persona.  1 is perfectly similar, 0 is not at all'''
        return self.get_similarity(
            other_entity=other_entity,
            dict_key_1='stats')


    #-------------------------------------------------------------------------
    #Get goal similarity
    #-------------------------------------------------------------------------
    def get_similarity_goals(self, other_entity=None):
        '''get_similarity_goals(self, other_entity)
        ---------------------------------
        This function takes in itself and other_entity (an Entity object). It
        uses Pearson correlation to determine how similar this an another 
        entity are based on their goals.  1 is perfectly similar, 0 is not at all'''
        #dict_key_2 is passed in from a loop in the function call itself, 
        #   so we don't set or use it
        return self.get_similarity(
            other_entity=other_entity,
            dict_key_1='goals',
            dict_key_3='closeness_average',
            values_exist_for_both=False)

    def get_similarity_total(self, other_entity=None):
        '''get_similarity_total(self, other_entity)
        ---------------------------------
        This function return the total similarity values between the two
        Entities (their goals + persona / 2). 
        TODO: Weight goals or persona? Add stats?'''

        return (
            (self.get_similarity_goals(other_entity=other_entity) \
            + self.get_similarity_persona(other_entity=other_entity) 
        ) / 2)


    '''====================================================================
    
    Geography Related

    ======================================================================='''
    def get_nearest_entities(self):
        '''get_nearest_entities(self)
        ---------------------------------
        This function gets the closet entities, geographically speaking'''
        #Store distances between this entity and all others
        distances = {}

        #Loop through all the Entities to get their positions
        #TODO: Optimize, we don't want to always loop through EVERYTHING
        for entity in Entity._entities:
            dist = math.sqrt(
                math.pow((self.position[0] - Entity._entities[
                    entity].position[0]), 2) + math.pow(
                    (self.position[1] - Entity._entities[entity].position[1]),2)
            )
            distances[Entity._entities[entity].id] = dist

        #Remove self from list
        distances.pop(self.id)

        #Get a list of entities, along with distance
        sorted_list = sorted(distances, key=distances.get)

        #Loop through list, turn each item in the list to a list containing
        #   the Entity's ID and distance value
        for i in range(len(sorted_list)):
            sorted_list[i] = [
                #Get actual entity object
                Entity._entities[sorted_list[i]], 
                #Add distance
                distances[sorted_list[i]]]

        return sorted_list

    '''====================================================================
    
    Target Related

    ======================================================================='''
    def set_target(self, target=None):
        '''set_target(self, target):
        ----------------------------
        Set's this entity's target to the passed in target. Can be
        a list of targets, an individual target, or None (will clear target).
        Can also be set as self.'''
        if isinstance(target, str):
            target = Entity._entities[target]
        self.target = target

    def get_target(self):
        '''get_target(self):
        ----------------------------
        This will get a target entity based on a variety of things, such
            as nearby entities.'''
        #TODO: Think more about this.  For now, just get nearest entity
        try:
            self.target = self.get_nearest_entities()[0][0]
        except IndexError:
            self.target = self

    '''====================================================================
    
    Action Related

    ======================================================================='''
    #TODO: General: Get rid of target parameter (use self.target)
    #   (How to handle position / object / item as targets?)
    def get_action(self, 
        action_key='converse',
        target=None):
        '''get_action(self)
        ----------------------------------------------
        Determines which action the Entity should perform.  Will return an
        Action object, but not actually perform the action'''
        if target is None:
            target = self.target

        return Action.Action._create_action(action_key, self, target)

    def perform_action(self, action=None,
        target=None):
        '''perform_action(self, action, target)
        ----------------------------------------------
        Takes in an action (could be either an Action object or
            a key to use to grab an object based on the _ACTIONS
            dict) and a target (can be either an entity object or
            list of entities, or a location, item, etc).'''

        #Set target to self target if nothing is passed in
        if target is None:
            target = self.target

        if action is None:
            #Get the action object
            action = self.get_action()

        elif isinstance(action, str):
            action = self.get_action(action, target)
    
        #Perform the action(s)
        if not isinstance(action, list):
            if isinstance(action, Action.Action):
                action.perform()
                print 'Performed %s' % (action)
            else:
                print 'Failed to perform action'

        else:
            for i in range(len(action)):
                if isinstance(action[i], Action.Action):
                    action[i].perform()
