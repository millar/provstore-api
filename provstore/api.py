from provstore.document import Document

class Api(object):
    def __init__(self,
                 username=None,
                 api_key=None,
                 base_url=None):

        if base_url is None:
            self.base_url = 'https://provenance.ecs.soton.ac.uk/store/api/v0'
        else:
            self.base_uri = base_url.rstrip('/')


    @property
    def document(self):
        return Document(self)


# from provstore import Api
#
# api = Api()
#
# document = ProvDocument()
#
# stored_document = api.document.create(document, name="Given name")
# stored_document.id
# stored_document.prov
#
# read_document = api.document.get(document_id)
# read_document.add_bundle()
# # or
# api.bundle.save(document_id, prov_bundle)
#
# read_document.bundles['identifier']
#
#
