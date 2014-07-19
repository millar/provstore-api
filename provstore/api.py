import os
import json
import requests
from copy import copy
from prov.model import ProvDocument
from provstore.document import Document


"""
  Usage:

  from provstore import Api

  api = Api()

  document = ProvDocument()

  stored_document = api.document.create(document, name="Given name")
  stored_document.id
  stored_document.prov

  read_document = api.document.get(document_id)
  read_document.add_bundle()
  # or
  api.bundle.save(document_id, prov_bundle)

  read_document.bundles['identifier']
"""
class Api(object):
    FORMAT_MAP = {
        'json': 'application/json'
    }


    def __init__(self,
                 username=None,
                 api_key=None,
                 base_url=None):

        if base_url is None:
            self.base_url = 'https://provenance.ecs.soton.ac.uk/store/api/v0'
        else:
            self.base_url = base_url.rstrip('/')


        self._username = username
        self._api_key = api_key

        if not self._username:
            self._username = os.environ.get('PROVSTORE_USERNAME', None)
        if not self._api_key:
            self._api_key = os.environ.get('PROVSTORE_API_KEY', None)


    @property
    def document(self):
        return Document(self)


    @property
    def headers(self):
        headers = {}

        headers['Accept'] = 'application/json'

        if self._username and self._api_key:
            headers['Authorization'] = self._authorization_header

        return headers


    def _request(self, method, *args, **kwargs):
        r = requests.request(method, *args, **kwargs)

        # TODO: Catch error reponses and raise our own exceptions

        # Fallback
        r.raise_for_status()

        return r


    @property
    def _authorization_header(self):
        return "ApiKey %s:%s" % (self._username, self._api_key)


    def get_document_prov(self, document_id, prov_format=ProvDocument):
        if prov_format == ProvDocument:
            extension = 'json'
        else:
            extension = prov_format

        r = self._request('get', self.base_url + "/documents/%i.%s" % (document_id, extension),
                          headers=self.headers)

        if prov_format == ProvDocument:
            return ProvDocument.deserialize(content=r.content)
        else:
            return r.content


    def get_document_meta(self, document_id):
        r = self._request('get', self.base_url + "/documents/%i/" % document_id,
                          headers=self.headers)
        return r.json()


    def post_document(self, prov_document, prov_format, name, public=False):
        headers = copy(self.headers)
        headers.update({'Content-type': self.FORMAT_MAP[prov_format]})

        r = self._request('post', self.base_url + '/documents/',
                          data=json.dumps({
                            'content': prov_document,
                            'public':  public,
                            'rec_id':  name
                          }),
                          headers=headers)
        return r.json()


    def add_bundle(self, document_id, prov_bundle, identifier):
        headers = copy(self.headers)
        headers.update({'Content-type': 'application/json'})

        r = self._request('post', self.base_url + "/documents/%i/bundles/" % document_id,
                          data=json.dumps({
                            'content': json.loads(prov_bundle),
                            'rec_id':  str(identifier)
                          }),
                          headers=headers)

        return True


    def get_bundles(self, document_id):
        r = self._request('get', self.base_url + "/documents/%i/bundles/" % document_id,
                          headers=self.headers)

        return r.json()['objects']


    def get_bundle(self, document_id, bundle_id, prov_format=ProvDocument):
        if prov_format == ProvDocument:
            extension = 'json'
        else:
            extension = prov_format

        r = self._request('get', self.base_url + "/documents/%i/bundles/%i.%s" % (document_id, bundle_id, extension),
                          headers=self.headers)

        if prov_format == ProvDocument:
            return ProvDocument.deserialize(content=r.content)
        else:
            return r.content


    def delete_document(self, document_id):
        r = self._request('delete', self.base_url + "/documents/%i/" % document_id,
                          headers=self.headers)
        return True
