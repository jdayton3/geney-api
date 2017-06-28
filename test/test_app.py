

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

    def test_NoGenesFoundReturnsEmptyString(self):
        self.response = self.app.get("/api/meta/sampledataset/gene?search=cantfindme")
        expected = []
        self.assertEqual(expected, json.loads(self.response.data))

    def test_EmptySearchStringReturnsAllVals(self):
        self.response = self.app.get("/api/meta/sampledataset/gene?search=")
        expected = ['gene1', 'gene2', "AF10", "ALOX12", "ARHGEF12", "RNT", "AXL", "BAX", "BCL3", "CL6", "BTG1", "AV1", "CBFB", "DC23", "DH17", "CDX2", "CEBPA", "CLC", "R1", "CREBBP", "EK", "DLEU1", "DLEU2", "GFR", "ETS1", "EVI2A", "EVI2B", "OXO3A", "FUS", "LI2", "MPS", "HOX11", "OXA9", "RF1", "IT", "AF4", "LCP1", "LDB1", "LMO1", "LMO2", "LYL1", "ADH5", "LL3", "LLT2", "LLT3", "MOV10L1", "TCP1", "YC", "NFKB2", "OTCH1", "NOTCH3", "PM1", "UP214", "NUP98", "BX1", "BX2", "BX3", "BXP1", "ITX2", "PML", "AB7", "GS2", "RUNX1", "ET", "P140", "AL1", "AL2", "TCL1B", "TCL6", "THRA", "TRA", "NFN1A1"]
        self.assertEqual(expected, json.loads(self.response.data))

class TestMetaSearch(RouteTester):
    # Arrange, Act, Assert
    def send_request(self, request):
        response = self.app.get(request)
        return response

    def make_request(self, id, variable, search):
        request = "/api/meta/%s/metaType/%s?search=%s" % (id, variable, search)
        return request

    def test_SearchReturns200Response(self):
        route = self.make_request("sampledataset", "var1", "val")
        response = self.send_request(route)
        self.assertEqual(200, response.status_code)

    def test_ResponseIsAsDefinedByDocumentation(self):
        expected = ["val1", "val2"]
        route = self.make_request("sampledataset", "var1", "val")
        response = self.send_request(route)
        self.assertEqual(expected, json.loads(response.data))

    def test_SearchWorks(self):
        expected = ["val1"]
        route = self.make_request("sampledataset", "var1", "al1")
        response = self.send_request(route)
        self.assertEqual(expected, json.loads(response.data))

    def test_EmptySearchStringReturnsAllVals(self):
        expected = ["val1", "val2", "thing3", "thing4"]
        route = self.make_request("sampledataset", "var1", "")
        response = self.send_request(route)
        self.assertEqual(expected, json.loads(response.data))

    def test_CanFindValsFromOtherVariables(self):
        expected = ["option1", "option2", "option3"]
        route = self.make_request("sampledataset", "variable1", "")
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
        response = self.empty_query()
        self.assertEqual(200, response.status_code)

    def test_ResponseIsValidJsonObj(self):
        response = self.empty_query()
        obj = json.loads(response.data)
        self.assertEqual(dict, type(obj))

    def test_404ErrorForInvalidQueryObject(self):
        data = {}
        response = self.post_request("sampledataset", data)
        self.assertEqual(404, response.status_code)

    def test_ResponseHasSamplesKey(self):
        response = self.empty_query()
        obj = json.loads(response.data)
        self.assertEqual("samples", obj.keys()[0])
        self.assertEqual(1, len(obj.keys()))

    # There are 123 fake samples.  There are three options in the "variable1"
    # meta type, and we're assuming that the samples are equally divided 
    # across the three values.
    def test_SamplesIs123ForEmptyQueryObject(self):
        response = self.empty_query()
        obj = json.loads(response.data)
        self.assertEqual(123, obj["samples"])

    def test_SamplesIs82ForTwoValQuery(self):
        data = {"meta": {"variable1": ["option1", "option2"]}}
        response = self.post_request("sampledataset", data)
        obj = json.loads(response.data)
        self.assertEqual(82, obj["samples"])