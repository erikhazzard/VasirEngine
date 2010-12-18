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

    def test_init(self):
        '''Test that init creates an entity object'''
        assert self.entity.persona is not None

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
