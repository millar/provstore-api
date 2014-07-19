import os
import unittest
import datetime

from provstore.api import Api, NotFoundException
from provstore.document import AbstractDocumentException, ImmutableDocumentException, EmptyDocumentException
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

        self.assertEqual(self.api.document.read_meta(stored_document.id).name, "test_basic_bundle_storage")

        self.assertTrue(isinstance(stored_document.bundles['ex:bundle-2'].created_at, datetime.datetime))

        stored_document.delete()


    def test_bundle_iteration(self):
        prov_document = examples.flat_document()

        stored_document = self.api.document.create(prov_document, refresh=True,
                                                    name="test_basic_bundle_storage")

        stored_document.add_bundle(prov_document, identifier="ex:bundle-1")
        stored_document.bundles['ex:bundle-2'] = prov_document

        self.assertEqual(len(stored_document.bundles), 0)
        self.assertEqual(set([u'ex:bundle-1', u'ex:bundle-2']), set([bundle.identifier for bundle in stored_document.bundles]))
        self.assertEqual(len(stored_document.bundles.refresh()), 2)

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


    def test_lazy_instantiation_of_props(self):
        prov_document = examples.flat_document()

        stored_document = self.api.document.create(prov_document, refresh=True,
                                                   name="test_lazy_instantiation_of_props")

        self.assertEqual(self.api.document.set(stored_document.id).views, 0)
        self.assertEqual(self.api.document.set(stored_document.id).owner, self.api._username)
        self.assertTrue(isinstance(self.api.document.set(stored_document.id).created_at, datetime.datetime))
        self.assertEqual(self.api.document.set(stored_document.id).prov, prov_document)
        self.assertFalse(self.api.document.set(stored_document.id).public)
        self.assertEqual(self.api.document.set(stored_document.id).name, "test_lazy_instantiation_of_props")

        stored_document.delete()


    def test_document_props(self):
        prov_document = examples.flat_document()

        stored_document = self.api.document.create(prov_document, refresh=True,
                                                   name="test_document_props")

        self.assertEqual(stored_document.views, 0)
        self.assertEqual(stored_document.owner, self.api._username)
        self.assertTrue(isinstance(stored_document.created_at, datetime.datetime))
        self.assertEqual(stored_document.prov, prov_document)
        self.assertFalse(stored_document.public)
        self.assertEqual(stored_document.name, "test_document_props")

        stored_document.delete()


    def test_empty_exceptions(self):
        with self.assertRaises(EmptyDocumentException):
            self.api.document.views
        with self.assertRaises(EmptyDocumentException):
            self.api.document.created_at
        with self.assertRaises(EmptyDocumentException):
            self.api.document.owner
        with self.assertRaises(EmptyDocumentException):
            self.api.document.prov
        with self.assertRaises(EmptyDocumentException):
            self.api.document.public
        with self.assertRaises(EmptyDocumentException):
            self.api.document.name


    def test_abstract_exceptions(self):
        prov_document = examples.flat_document()

        abstract_document = self.api.document

        with self.assertRaises(AbstractDocumentException):
            abstract_document.bundles
        self.assertRaises(AbstractDocumentException, abstract_document.delete)
        with self.assertRaises(AbstractDocumentException):
            abstract_document.add_bundle(prov_document, 'ex:bundle')
        self.assertRaises(AbstractDocumentException, abstract_document.read_meta)
        self.assertRaises(AbstractDocumentException, abstract_document.read_prov)


    def test_immutable_exceptions(self):
        prov_document = examples.flat_document()

        stored_document = self.api.document.create(prov_document, name="test_immutable_exceptions")

        self.assertRaises(ImmutableDocumentException, stored_document.create, (stored_document,))
        self.assertRaises(ImmutableDocumentException, stored_document.set, (1,))
        self.assertRaises(ImmutableDocumentException, stored_document.get, (1,))
        self.assertRaises(ImmutableDocumentException, stored_document.read_prov, (1,))
        self.assertRaises(ImmutableDocumentException, stored_document.read_meta, (1,))
        self.assertRaises(ImmutableDocumentException, stored_document.read, (1,))

        stored_document.delete()


    def test_equality(self):
        prov_document = examples.flat_document()

        stored_document = self.api.document.create(prov_document, name="test_immutable_exceptions")

        self.assertFalse(stored_document == "document")

        stored_document.delete()
