"""=============================================================================
    test_story.py
    ------------
    Contains tests specific for the Story class
============================================================================="""
"""=============================================================================

IMPORTS / CONSTANTS

============================================================================="""
import unittest
import Story 

"""=============================================================================

TESTS

============================================================================="""
class testStoreme(unittest.TestCase):
    '''Entity Test'''
    def setUp(self):
        '''Start the test object'''
        self.storeme = Story.Storeme()

    def test_init(self):
        '''Test that init creates a storeme object'''
        assert self.storeme is not None
        #We didn't pass in any entities, make sure it is set as an empty tuple
        assert self.storeme.related_entities is ()
        self.test_related_entity = Story.Storeme(related_entities=[None, None])
        assert self.test_related_entity.related_entities == [None, None]

    def tearDown(self):
        '''Done with test'''
        self.storeme = None

"""=============================================================================

RUN TESTS

============================================================================="""
if __name__ == '__main__':
    unittest.main()
