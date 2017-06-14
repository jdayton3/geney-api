

import sys
sys.path.append('../')

import unittest
import requests
import json
from app import *


class RouteTester(unittest.TestCase):
    def setUp(self):
        api = MyAPI()
        api.app.testing = True
        self.app = api.app.test_client()

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

    def test_ResponseIsJsonArray(self):
        response = self.app.get('/api/datasets')
        try:
            expected = json.loads(response.data)
        except ValueError as e:
            self.fail("Failed to load JSON (%s). %s" % (response.data, e))
        self.assertEqual(list, type(expected))

class TestMeta(RouteTester):
    def test_MetaRouteExists(self):
        response = self.app.get('/api/meta/sampledataset')
        self.assertEqual(response.status_code, 200)


    def test_ResponseIsJsonObj(self):
        response = self.app.get('/api/meta/sampledataset')
        try:
            expected = json.loads(response.data)
        except ValueError as e:
            self.fail("Failed to load JSON (%s). %s" % (response.data, e))
        self.assertEqual(dict, type(expected))

    def test_NextSteps(self):
        message = "I need to include a DBAccess object in the __init__ function of MyAPI"
        self.fail(message)