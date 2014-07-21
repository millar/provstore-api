from prov.model import parse_xsd_datetime


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
        """
        :return: When the bundle was added
        :rtype: :py:class:`datetime.datetime`
        """
        return self._created_at

    @property
    def identifier(self):
        """
        :return: Identifier of the document, used as index on :py:class:`provstore.bundle_manager.BundleManager`
        :rtype: str
        """
        return self._identifier

    @property
    def prov(self):
        """
        :return: This bundle's provenance
        :rtype: :py:class:`prov.model.ProvDocument`
        """
        if not self._prov:
            self._prov = self._api.get_bundle(self._document.id, self._id)

        return self._prov
