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

    def assert_status_code(self, uri, data, statuscode):
        response = self.app.post(uri, data=data, content_type='application/json')
        self.assertEqual(response.status_code, statuscode)

    def test_search(self):
        self.assert_status_code("/search",
                                '{"time":"2018-03-05T21:22:51.293Z","origin":"kurhessenstrasse","destination":"huegelstrasse"}',
                                200)

    def test_search_invalid_time(self):
        self.assert_status_code("/search",
                                '{"time":"","origin":"kurhessenstrasse","destination":"huegelstrasse"}',
                                404)

    def test_search_destination_invalid_station(self):
        self.assert_status_code('/search',
                                '{"time":"2018-03-05T21:22:51.293Z","origin":"invalidstation","destination":"huegelstrasse"}',
                                404)

    def test_search_destination_station_is_none(self):
        self.assert_status_code('/search',
                                '{"time":"2018-03-05T21:22:51.293Z","destination":"huegelstrasse"}',
                                404)

    def test_search_destination_equals_origin(self):
        self.assert_status_code('/search',
                                '{"time":"2018-03-05T21:22:51.293Z","origin":"huegelstrasse","destination":"huegelstrasse"}',
                                404)