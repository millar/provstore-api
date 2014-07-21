import os
import json
import requests
from copy import copy
from prov.model import ProvDocument
from provstore.document import Document


MAX_RETRIES = 3


class ProvStoreException(Exception):
    pass


class NotFoundException(ProvStoreException):
    pass


class RequestTimeoutException(ProvStoreException):
    pass


class InvalidCredentialsException(ProvStoreException):
    pass


class ForbiddenException(ProvStoreException):
    pass


class InvalidDataException(ProvStoreException):
    pass


class UnprocessableException(ProvStoreException):
    pass


class DocumentInvalidException(ProvStoreException):
    pass


class Api(object):
    """
    Main ProvStore API client object

    Most functions are not used directly but are instead accessed by functions of the Document, BundleManager and Bundle
    objects.

    To create a new Api object:
      >>> from provstore.api import Api
      >>> api = Api(username="provstore username", api_key="api key")

    .. note::
       The username and api_key parameters can also be omitted in which case the client will look for
       **PROVSTORE_USERNAME** and **PROVSTORE_API_KEY** environment variables.

    To read public documents no credentials need be provided.
    """
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

    def __eq__(self, other):
        if not isinstance(other, Api):
            return False

        return self.base_url == other.base_url

    def __ne__(self, other):
        return not self == other

    @property
    def document(self):
        return Document(self)

    @property
    def headers(self):
        headers = dict()

        headers['Accept'] = 'application/json'

        if self._username and self._api_key:
            headers['Authorization'] = self._authorization_header

        return headers

    def _request(self, method, url, retries=0, *args, **kwargs):
        try:
            kwargs.update({'timeout': 30})
            r = requests.request(method, url, **kwargs)
        except requests.exceptions.Timeout:
            if retries < MAX_RETRIES:
                return self._request(method, *args, retries=retries+1, **kwargs)
            raise RequestTimeoutException()

        if r.status_code == 500:
            raise ProvStoreException()
        elif r.status_code == 422:
            raise UnprocessableException()
        elif r.status_code == 410:
            raise DocumentInvalidException()
        elif r.status_code == 404:
            raise NotFoundException()
        elif r.status_code == 403:
            raise ForbiddenException()
        elif r.status_code == 401:
            raise InvalidCredentialsException()
        elif r.status_code == 400:
            raise InvalidDataException()
        else:
            # Fallback, this should not happen!
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

        self._request('post', self.base_url + "/documents/%i/bundles/" % document_id,
                      data=json.dumps({
                          'content': json.loads(prov_bundle),
                          'rec_id':  unicode(identifier)
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
        self._request('delete', self.base_url + "/documents/%i/" % document_id,
                      headers=self.headers)
        return True
