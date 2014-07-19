import os
import unittest

from provstore.api import Api, NotFoundException
import provstore.tests.examples as examples


PROVSTORE_USERNAME  = os.environ.get('PROVSTORE_USERNAME', 'provstore-api-test')
PROVSTORE_API_KEY   = os.environ.get('PROVSTORE_API_KEY', '56f7db0b9f1651d2cb0dd9b11c53b5fdc2dcacf4')


class LoggedInAPITestMixin(object):
    @classmethod
    def setUpClass(cls):
        cls.api = Api(username=PROVSTORE_USERNAME, api_key=PROVSTORE_API_KEY)
        return super(LoggedInAPITestMixin, cls).setUpClass()


class ProvStoreAPITests(LoggedInAPITestMixin, unittest.TestCase):
    def test_basic_storage(self):
        prov_document = examples.flat_document()

        stored_document = self.api.document.create(prov_document, refresh=True,
                                                   name="test_basic_storage")

        self.assertEqual(stored_document.prov, prov_document)

        stored_document.delete()


    def test_basic_bundle_storage(self):
        prov_document = examples.flat_document()

        stored_document = self.api.document.create(prov_document, refresh=True,
                                                    name="test_basic_bundle_storage")

        stored_document.add_bundle(prov_document, identifier="ex:bundle-1")
        stored_document.bundles['ex:bundle-2'] = prov_document


        # should be a match even though we've added a bundle, this is a stale
        # instance
        self.assertEqual(stored_document.prov, prov_document)

        # when we refresh it, it should no longer match
        self.assertNotEqual(stored_document.refresh().prov, prov_document)

        self.assertEqual(stored_document.bundles['ex:bundle-2'].prov, prov_document)

        stored_document.delete()


    def test_basic_bundle_retrieval(self):
        prov_document = examples.flat_document()

        stored_document1 = self.api.document.create(prov_document, refresh=True,
                                                    name="test_basic_bundle_storage")

        stored_document2 = self.api.document.create(prov_document, refresh=True,
                                                    name="test_basic_bundle_storage")

        retrieved_document = self.api.document.get(stored_document1.id)


        self.assertEqual(stored_document1, retrieved_document)
        self.assertNotEqual(stored_document2, retrieved_document)


    def test_non_existent_bundle(self):
        prov_document = examples.flat_document()

        stored_document = self.api.document.create(prov_document, refresh=True,
                                                    name="test_basic_bundle_storage")

        with self.assertRaises(NotFoundException):
            stored_document.bundles['ex:not-there']

        stored_document.delete()


    def test_non_existent_document(self):
        with self.assertRaises(NotFoundException):
            stored_document = self.api.document.get(-1)
