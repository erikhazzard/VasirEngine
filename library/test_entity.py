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
        '''Start the test object'''
        self.entity = Entity.Entity()
        assert Entity.Entity._entity_created_count > 0

    def test_gender(self):
        '''Test the entity's gender'''
        assert self.entity.gender is not None

    def test_init(self):
        '''Test that init creates an entity object'''
        assert self.entity.persona is not None
        '''Test the entity's gender'''
        assert self.entity.gender is not None
        assert self.entity.id is not None
        #Make sure it has a semi valid ID
        assert len(self.entity.id) > 10
        #Make sure this entity ID is in the list of entities
        assert self.entity.id in Entity.Entity._entity_objects

    def test_name(self):
        '''Test that the name function generates a valid name'''
        assert self.entity.generate_name() is not None
        assert self.entity.generate_name() != ''
        assert len(self.entity.generate_name()) > 0
        
    def test_randomize_persona(self):
        '''Test that randomize_persona works'''
        self.entity.randomize_persona()

    def tearDown(self):
        '''Done with test'''
        self.entity = None

"""=============================================================================

RUN TESTS

============================================================================="""
if __name__ == '__main__':
    unittest.main()
