from horosh.tests import *

class TestDummyController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='dummy', action='index'))
        # Test response...
