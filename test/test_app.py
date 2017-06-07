

import sys
sys.path.append('../')

import unittest
import requests
import json
from app import *


class TestRoutesWork(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_IndexDoesNotExist(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 404)

    def test_Datasets(self):
        response = self.app.get('/api/datasets')
        self.assertEqual(response.status_code, 200)