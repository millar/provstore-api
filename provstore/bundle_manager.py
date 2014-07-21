from provstore.bundle import Bundle


class BundleManager(object):
    """
    A document's bundle manager.

    This is an iterable and will iterate through all of a document's bundles.

    Example getting and adding bundles:
      >>> api = Api()
      >>> api.document.create(prov_document, name="name")
      >>> api.bundles
      A BundleManager object for this document
      >>> api.bundles['ex:bundle']
      A Bundle with the identifier given (if exists)
      >>> api.bundles['ex:new_bundle'] = prov_bundle
      Saves a new bundle with the identifier specified

    """
    def __init__(self, api, document):
        self._api = api
        self._document = document
        self._bundles = None

    def __getitem__(self, key):
        if not self._bundles:
            self.refresh()

        if key not in self._bundles:
            from provstore.api import NotFoundException
            raise NotFoundException()

        return self._bundles[key]

    def __setitem__(self, key, prov_bundle):
        self._document.add_bundle(prov_bundle, key)

    def __iter__(self):
        if not self._bundles:
            self.refresh()

        return self._bundles.itervalues()

    def __len__(self):
        if self._bundles:
            return len(self._bundles)
        else:
            return 0

    def refresh(self):
        """
        Reload list of bundles from the store

        :return: self
        """
        self._bundles = {}

        bundles = self._api.get_bundles(self._document.id)
        for bundle in bundles:
            self._bundles[bundle['identifier']] = Bundle(self._api, self._document, bundle)
        
        return self
