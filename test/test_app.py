

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
        self.response = self.app.get('/api/datasets/sampledataset/meta')
        self.meta = {
            "meta": {
                "variable1": {
                    "numOptions": 3,
                    "options": ["option1","option2","option3"]
                },
                "var1": {
                    "numOptions": 4,
                    "options": [
                        "val1",
                        "val2",
                        "thing3",
                        "thing4",
                    ]
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
        self.response = self.search("gene")
        self.genes = ["gene1", "gene2"]

    def search(self, search_str):
        return self.app.get("/api/datasets/sampledataset/meta/gene/search/" + search_str)

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
        self.response = self.search("ene1")
        expected = ["gene1"]
        self.assertEqual(expected, json.loads(self.response.data))

    def test_NoGenesFoundReturnsEmptyArray(self):
        self.response = self.search("cantfindme")
        expected = []
        self.assertEqual(expected, json.loads(self.response.data))

class TestMetaSearch(RouteTester):
    # Arrange, Act, Assert
    def send_request(self, request):
        response = self.app.get(request)
        return response

    def make_route(self, id, variable, search):
        request = "/api/meta/%s/metaType/%s?search=%s" % (id, variable, search)
        return request

    def test_SearchReturns200Response(self):
# Unchanged
        route = self.make_route("sampledataset", "var1", "val")
        response = self.send_request(route)
        self.assertEqual(200, response.status_code)

    def test_ResponseIsAsDefinedByDocumentation(self):
# Unchanged
        expected = ["val1", "val2"]
        route = self.make_route("sampledataset", "var1", "val")
        response = self.send_request(route)
        self.assertEqual(expected, json.loads(response.data))

    def test_SearchWorks(self):
# Unchanged
        expected = ["val1"]
        route = self.make_route("sampledataset", "var1", "al1")
        response = self.send_request(route)
        self.assertEqual(expected, json.loads(response.data))

    def test_EmptySearchStringReturnsAllVals(self):
# Unchanged
        expected = ["val1", "val2", "thing3", "thing4"]
        route = self.make_route("sampledataset", "var1", "")
        response = self.send_request(route)
        self.assertEqual(expected, json.loads(response.data))

    def test_CanFindValsFromOtherVariables(self):
# Unchanged
        expected = ["option1", "option2", "option3"]
        route = self.make_route("sampledataset", "variable1", "")
        response = self.send_request(route)
        self.assertEqual(expected, json.loads(response.data))

class TestSamples(RouteTester):
    def post_request(self, dataset_id, post_data):
        post_data = json.dumps(post_data)
        route = "/api/%s/samples" % dataset_id
        response = self.app.post(route, data=post_data)
        return response

    def empty_query(self, dataset_id="sampledataset"):
        data = {"meta": {}}
        return self.post_request(dataset_id, data)
    
    def test_RouteExists(self):
# Unchanged
        response = self.empty_query()
        self.assertEqual(200, response.status_code)

    def test_ResponseIsValidJsonObj(self):
# Unchanged
        response = self.empty_query()
        obj = json.loads(response.data)
        self.assertEqual(dict, type(obj))

    def test_404ErrorForInvalidQueryObject(self):
# Unchanged
        data = {}
        response = self.post_request("sampledataset", data)
        self.assertEqual(404, response.status_code)

    def test_ResponseHasSamplesKey(self):
# Unchanged
        response = self.empty_query()
        obj = json.loads(response.data)
        self.assertEqual("samples", obj.keys()[0])
        self.assertEqual(1, len(obj.keys()))

    # There are 123 fake samples.  There are three options in the "variable1"
    # meta type, and we're assuming that the samples are equally divided 
    # across the three values.
    def test_SamplesIs123ForEmptyQueryObject(self):
# Unchanged
        response = self.empty_query()
        obj = json.loads(response.data)
        self.assertEqual(123, obj["samples"])

    def test_SamplesIs82ForTwoValQuery(self):
# Unchanged
        data = {"meta": {"variable1": ["option1", "option2"]}}
        response = self.post_request("sampledataset", data)
        obj = json.loads(response.data)
        self.assertEqual(82, obj["samples"])

class TestDownloadFile(RouteTester):
    def post_request(self, dataset_id, post_data):
        post_data = json.dumps(post_data)
        route = "/api/%s/download" % dataset_id
        response = self.app.post(route, data=post_data)
        return response

    def basic_query(self, dataset_id="sampledataset"):
        data = {
            "query": {
                "meta": {
                    "variable1": ["option1", "option3"]
                },
                "genes": [],
                "options": {
                    "fileformat": "csv",
                    "filename": "example"
                }
            }
        }
        return self.post_request(dataset_id, data)
    
    def test_RouteExists(self):
# Unchanged
        response = self.basic_query()
        self.assertEqual(200, response.status_code)

    def test_DownloadsCsv(self):
# Unchanged
        response = self.basic_query()
        self.assertRegexpMatches(response.headers["Content-Type"], "text/csv")
        self.assertRegexpMatches(
            response.headers["Content-Disposition"], "attachment"
        )
        # TODO: this only checks that the mimetype is correct, not that the
        # actual body is a CSV...

    def test_CorrectFilename(self):
# Unchanged
        response = self.basic_query()
        self.assertRegexpMatches(
            response.headers["Content-Disposition"], "filename=example.csv"
        )
        # TODO: this needs to check multiple filenames