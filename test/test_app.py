

import sys, os
sys.path.append(os.path.abspath('src'))

import unittest
import requests
import json
from app import *
from data_access import DataObj

class RouteTester(unittest.TestCase):
    def setUp(self):
        api = MyAPI(DataObj())
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
    def setUp(self):
        super(self.__class__, self).setUp()
        self.response = self.app.get('/api/datasets')
        self.datasets = [{
                    "numMetaTypes": 1,
                    "numSamples": 123,
                    "numGenes": 3,
                    "description": "#Description\n##This is the Description",
                    "name": "Sample Dataset",
                    "id": "sampledataset",
                    "uploadDate": 1494195717279
                }]

    def test_DatasetsRouteExists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_ResponseIsJsonArray(self):
        try:
            actual = json.loads(self.response.data)
        except ValueError as e:
            self.fail("Failed to load JSON (%s). %s" % (self.response.data, e))
        self.assertEqual(list, type(actual))

    def test_ResponseIsAsDefinedByDocumentation(self):
        self.assertEqual(self.datasets, json.loads(self.response.data))

class TestMeta(RouteTester):
    def setUp(self):
        super(self.__class__, self).setUp()
        self.response = self.app.get('/api/meta/sampledataset')
        self.meta = {
            "meta": {
                "variable1": {
                    "numOptions": 3,
                    "options": ["option1","option2","option3"]
                }
            },
            "genes": {
                "numOptions": 190000,
                "options": None
            }
        }

    def test_MetaRouteExists(self):
        self.assertEqual(self.response.status_code, 200)

    def test_ResponseIsJsonObj(self):
        try:
            actual = json.loads(self.response.data)
        except ValueError as e:
            self.fail("Failed to load JSON (%s). %s" % (self.response.data, e))
        self.assertEqual(dict, type(actual))

    def test_ResponseIsAsDefinedByDocumentation(self):
        self.assertEqual(self.meta, json.loads(self.response.data))

class TestGeneSearchRoute(RouteTester):
    def setUp(self):
        super(self.__class__, self).setUp()
        self.response = self.app.get("/api/meta/sampledataset/gene?search=gene")
        self.genes = ["gene1", "gene2"]

    def test_RouteExists(self):
        self.assertEqual(200, self.response.status_code)

    def test_ResponseIsJsonArray(self):
        try:
            actual = json.loads(self.response.data)
        except ValueError as e:
            self.fail("Failed to load JSON (%s). %s" % (self.response.data, e))
        self.assertEqual(list, type(actual))

    def test_ResponseIsAsDefinedByDocumentation(self):
        self.assertEqual(self.genes, json.loads(self.response.data))

    def test_SearchWorks(self):
        self.response = self.app.get("/api/meta/sampledataset/gene?search=ene1")
        expected = ["gene1"]
        self.assertEqual(expected, json.loads(self.response.data))

    def test_NextSteps(self):
        message = "I need to include a DBAccess object in the __init__ function of MyAPI"
        #self.fail(message)