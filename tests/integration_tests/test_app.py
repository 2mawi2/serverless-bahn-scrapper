from unittest import TestCase
import json

from src import app, static


class TestIntegrationsApp(TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_stations(self):
        response = self.app.get('/stations')
        data = json.loads(response.data)['stations']
        assert response.status_code is 200
        for station in static.stations:
            assert station in data

    def test_search(self):
        response = self.app.post('/search',
                                 data='{"time":"2018-03-05T21:22:51.293Z","origin":"kurhessenstrasse","destination":"huegelstrasse"}',
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_search_invalid_time(self):
        response = self.app.post('/search',
                                 data='{"time":"","origin":"kurhessenstrasse","destination":"huegelstrasse"}',
                                 content_type='application/json')
        self.assertEqual(response.status_code, 418)

    def test_search_destination_equals_origin(self):
        response = self.app.post('/search',
                                 data='{"time":"2018-03-05T21:22:51.293Z","origin":"huegelstrasse","destination":"huegelstrasse"}',
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)
