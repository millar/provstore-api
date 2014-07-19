import json
from prov.model import ProvDocument, parse_xsd_datetime
from provstore.bundle_manager import BundleManager

# Document exceptions
class DocumentException(Exception):
    pass

class AbstractDocumentException(DocumentException):
    def __init__(self):
        self.message = "Unsaved documents cannot be read"

class EmptyDocumentException(DocumentException):
    def __init__(self):
        self.message = "There is no data associated with this document"

class ImmutableDocumentException(DocumentException):
    def __init__(self):
        self.message = "Cannot change document instance reference"


# API Document model
class Document(object):
    def __init__(self, api):
        self._api = api
        self._id = None

        self._name = None
        self._public = None
        self._owner = None
        self._created_at = None
        self._views = None

        self._prov = None


    def __eq__(self, other):
        if not isinstance(other, Document):
            return False

        return self._api == other._api and self.id == other.id


    def __ne__(self, other):
        return not self == other


    # Abstract methods

    def create(self, prov_document, prov_format=None, refresh=False, **props):
        if not self.abstract:
            raise ImmutableDocumentException()

        if isinstance(prov_document, ProvDocument):
            self._prov = prov_document

            prov_format = "json"
            prov_document = prov_document.serialize()

        self._id = self._api.post_document(prov_document, prov_format, **props)['id']

        if refresh:
            self.refresh()

        return self


    def set(self, document_id):
        if not self.abstract:
            raise ImmutableDocumentException()
        self._id = document_id

        return self


    def get(self, document_id):
        if not self.abstract:
            raise ImmutableDocumentException()

        return self.read(document_id)



    # Document instance methods

    def read(self, document_id=None):
        self.read_prov(document_id)
        self.read_meta()
        return self


    def refresh(self):
        # We don't alias so that users cannot specify document_id here
        return self.read()


    def read_prov(self, document_id=None):
        if document_id:
            if not self.abstract:
                raise ImmutableDocumentException()
            self._id = document_id

        if self.abstract:
            raise AbstractDocumentException()

        self._prov = self._api.get_document_prov(self.id)
        return self._prov


    def read_meta(self, document_id=None):
        if document_id:
            if not self.abstract:
                raise ImmutableDocumentException()
            self._id = document_id

        if self.abstract:
            raise AbstractDocumentException()

        metadata = self._api.get_document_meta(self.id)

        self._name = metadata['document_name']
        self._public = metadata['public']
        self._owner = metadata['owner']
        self._created_at = parse_xsd_datetime(metadata['created_at'])
        self._views = metadata['views_count']

        self._bundles = BundleManager(self._api, self)

        return self


    def add_bundle(self, prov_bundle, identifier):
        if self.abstract:
            raise AbstractDocumentException()

        self._api.add_bundle(self.id, prov_bundle.serialize(), identifier)


    @property
    def bundles(self):
        if self.abstract:
            raise AbstractDocumentException()

        return self._bundles


    def delete(self):
        if self.abstract:
            raise AbstractDocumentException()

        self._api.delete_document(self.id)
        self._id = None

        return True


    @property
    def id(self):
      return self._id

    @property
    def abstract(self):
        return self.id is None

    @property
    def name(self):
        if self._name:
            return self._name
        elif not self.abstract:
            return self.read_meta()._name

        raise EmptyDocumentException()


    @property
    def public(self):
        if self._public:
            return self._public
        elif not self.abstract:
            return self.read_meta()._public

        raise EmptyDocumentException()


    @property
    def owner(self):
        if self._owner:
            return self._owner
        elif not self.abstract:
            return self.read_meta()._owner

        raise EmptyDocumentException()


    @property
    def created_at(self):
        if self._created_at:
            return self._created_at
        elif not self.abstract:
            return self.read_meta()._created_at

        raise EmptyDocumentException()


    @property
    def views(self):
        if self._views:
            return self._views
        elif not self.abstract:
            return self.read_meta()._views

        raise EmptyDocumentException()


    @property
    def prov(self):
        if self._prov:
            return self._prov
        elif not self.abstract:
            return self.read_prov()

        raise EmptyDocumentException()
