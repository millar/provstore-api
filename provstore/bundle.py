
from prov.model import ProvDocument, parse_xsd_datetime

class Bundle(object):
    def __init__(self, api, document, bundle):
        self._api = api

        self._id = bundle['id']
        self._created_at = parse_xsd_datetime(bundle['created_at'])
        self._identifier = bundle['identifier']
        self._document = document

        self._prov = None


    @property
    def created_at(self):
        return self._created_at


    @property
    def identifier(self):
        return self._identifier


    @property
    def prov(self):
        if not self._prov:
            self._prov = self._api.get_bundle(self._document.id, self._id)

        return self._prov
