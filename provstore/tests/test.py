import os
import unittest

from prov.model import ProvDocument
from provstore.api import Api
import provstore.tests.examples as examples



PROVSTORE_USERNAME  = os.environ.get('PROVSTORE_USERNAME', 'provstore-api-test')
PROVSTORE_API_KEY   = os.environ.get('PROVSTORE_API_KEY', '56f7db0b9f1651d2cb0dd9b11c53b5fdc2dcacf4')


class ProvStoreAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = Api(username=PROVSTORE_USERNAME, api_key=PROVSTORE_API_KEY)


    def test_basic_storage(self):
        prov_document = examples.flat_document()

        stored_document = self.api.document.create(prov_document, refresh=True,
                                                   name="test_basic_storage: flat_document")

        stored_document.add_bundle(prov_document, identifier="ex:bundle-1")
        stored_document.bundles['ex:bundle-2'] = prov_document

        self.assertEqual(stored_document.prov, prov_document)
        self.assertEqual(stored_document.bundles['ex:bundle-2'].prov, prov_document)

        stored_document.delete()
