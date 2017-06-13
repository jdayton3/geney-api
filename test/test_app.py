

import sys
sys.path.append('../')

import unittest
import requests
import json
from app import *


class RouteTester(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

class TestRoutesWork(RouteTester):
    def test_IndexDoesNotExist(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 404)

    def test_404ReturnsJSON(self):
        response = self.app.get('/nothing/here')
        expected = {'error': 'Not found'}
        actual = json.loads(response.data)
        self.assertEqual(actual, expected)


class TestDatasets(RouteTester):
    def test_DatasetsRouteExists(self):
        response = self.app.get('/api/datasets')
        self.assertEqual(response.status_code, 200)

    def test_ResponseIsJsonObject(self):
        response = self.app.get('/api/datasets')
        try:
            expected = json.loads(response.data)
        except ValueError as e:
            self.fail("Failed to load JSON (%s). %s" % (response.data, e))

class TestMeta(RouteTester):
    def test_MetaRouteExists(self):
        response = self.app.get('/api/meta/sampledataset')
        self.assertEqual(response.status_code, 200)