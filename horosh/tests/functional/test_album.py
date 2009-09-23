from horosh.tests import *

class TestAlbumController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='album', action='index'))
        # Test response...
