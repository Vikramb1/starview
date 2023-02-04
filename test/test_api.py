import sys
sys.path.append(r'C:\Users\vikra\starview\backend')

import app, testing
import unittest
import json
from unittest import TestCase

class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_homepage(self):
        response = self.app.get('/')
        assert response.status_code == 200
        assert response.data == b'Welcome'

    def test_fetch_stars(self):
        normal = '0.0:0.0:0.0'
        back_normal = [0.01, 0.01, 0.01]
        req = f'/stars?normal={normal}'
        response = self.app.get(req)
        backend_response = json.loads(testing.normalise_stars(back_normal))

        assert response.status_code == 200
        assert json.loads(response.data) == backend_response

    def test_fetch_planets(self):
        normal = '0.0:0.0:0.0'
        back_normal = [0.01, 0.01, 0.01]
        req = f'/planets?normal={normal}'
        response = self.app.get(req)
        backend_response = json.loads(testing.normalise_planets(back_normal))

        assert response.status_code == 200
        assert json.loads(response.data) == backend_response

if __name__ == "__main__":
    unittest.main()