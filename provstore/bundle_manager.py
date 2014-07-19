from provstore.bundle import Bundle


class BundleManager(object):
    def __init__(self, api, document):
        self._api = api
        self._document = document
        self._bundles = None


    def __getitem__(self, key):
        if not self._bundles:
            self.refresh()

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
        self._bundles = {}

        bundles = self._api.get_bundles(self._document.id)
        for bundle in bundles:
            self._bundles[bundle['identifier']] = Bundle(self._api, self._document, bundle)
