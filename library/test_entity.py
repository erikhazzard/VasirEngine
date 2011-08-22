"""=============================================================================
    test_entity.py
    ------------
    Contains tests specific for the Entity class
============================================================================="""
"""=============================================================================

IMPORTS / CONSTANTS

============================================================================="""
import unittest
import Entity

"""=============================================================================

TESTS

============================================================================="""
class testEntity(unittest.TestCase):
    '''Entity Test'''
    def setUp(self):
        '''Start the test object. Called on every test_ function'''
        self.entity = Entity.Entity()
        assert Entity.Entity._entity_created_count > 0

    def test_init(self):
        '''Test that init creates an entity object'''
        assert self.entity.persona is not None
        '''Test the entity's gender'''
        assert self.entity.gender is not None
        assert self.entity.id is not None
        assert self.entity.gender is not None
        #Make sure it has a semi valid ID
        assert len(self.entity.id) > 10
        #Make sure this entity ID is in the list of entities
        assert self.entity.id in Entity.Entity._entity_objects
        #Make sure history and network exists
        assert self.entity.history is not None
        assert self.entity.network is not None
        print 'test_init OK'

    def test_name(self):
        '''Test that the name function generates a valid name'''
        assert self.entity.generate_name() is not None
        assert self.entity.generate_name() != ''
        assert len(self.entity.generate_name()) > 0
        print 'test_name OK'
        
    def test_randomize_persona(self):
        '''Test that randomize_persona works'''
        self.entity.randomize_persona()
        assert self.entity.persona is not None
        print 'test_randomize_persona OK'

    def test_action_meets_requirements(self):
        assert self.entity.action_meets_requirements() == True
        assert self.entity.action_meets_requirements(requirements=None) == True
        #Test passing in a persona value (no min / max)
        self.entity.persona['openness'] = 42
        assert self.entity.action_meets_requirements(requirements={'persona':{'openness':40}}) == True
        assert self.entity.action_meets_requirements(requirements={'persona':{'openness':50}}) == False
        #Test min 
        assert self.entity.action_meets_requirements(requirements={'persona':{'openness_min':40}}) == True
        assert self.entity.action_meets_requirements(requirements={'persona':{'openness_min':50}}) == False
        #Test max 
        assert self.entity.action_meets_requirements(requirements={'persona':{'openness_max':40}}) == False
        assert self.entity.action_meets_requirements(requirements={'persona':{'openness_max':50}}) == True

        #Test for other entity
        another_entity = Entity.Entity()
        another_entity.persona['openness'] = 42
        #Test no value
        assert self.entity.action_meets_requirements(target=another_entity,
            requirements={'persona':{'openness':40}}) == True
        assert self.entity.action_meets_requirements(target=another_entity,
            requirements={'persona':{'openness':50}}) == False
        #Test min 
        assert self.entity.action_meets_requirements(target=another_entity,
            requirements={'persona':{'openness_min':40}}) == True
        assert self.entity.action_meets_requirements(target=another_entity,
            requirements={'persona':{'openness_min':50}}) == False
        #Test max 
        assert self.entity.action_meets_requirements(target=another_entity,
            requirements={'persona':{'openness_max':40}}) == False
        assert self.entity.action_meets_requirements(target=another_entity,
            requirements={'persona':{'openness_max':50}}) == True

        print 'test_action_meets_requirement OK'

    def tearDown(self):
        '''Done with test'''
        self.entity = None

"""=============================================================================

RUN TESTS

============================================================================="""
if __name__ == '__main__':
    unittest.main()
