provstore-api [![PyPI version](https://badge.fury.io/py/provstore-api.svg)](http://badge.fury.io/py/provstore-api) [![Build Status](https://travis-ci.org/millar/provstore-api.svg?branch=master)](https://travis-ci.org/millar/provstore-api) [![Coverage Status](https://coveralls.io/repos/millar/provstore-api/badge.png)](https://coveralls.io/r/millar/provstore-api)
=========

Client for the [ProvStore](https://provenance.ecs.soton.ac.uk/store/)'s [API](https://provenance.ecs.soton.ac.uk/store/help/api/).

## Installation
```bash
pip install provstore-api
```

You can view [provstore-api on PyPi's package index](https://pypi.python.org/pypi/provstore-api/)
## Usage

To use the client import the API and configure your access credentials:

```python
from provstore.api import Api

# API key can be found at https://provenance.ecs.soton.ac.uk/store/account/developer/
api = Api(userame="your_provstore_username", api_key="your_api_key")
```

*Note: credentials can also be set via the `PROVSTORE_USERNAME` and `PROVSTORE_API_KEY` environment variables and omitted from the initialization.*

For demonstrations purposes we will use the ProvDocuments given in the examples
module, but you would use your documents instead.
```python
import provstore.tests.examples as examples
```

#### Storing documents

```python
prov_document = examples.flat_document()
prov_bundle = examples.flat_document()

# Store the document to ProvStore:
#   - the public parameter is optional and defaults to False
stored_document = api.document.create(prov_document,
                                      name="name",
                                      public=False)

# => This will store the document and return a ProvStore Document object
```

#### Retrieving documents

```python
# Get a document with ID 148 from ProvStore:
stored_document = api.document.get(148)

# => This will fetch the document and return a ProvStore Document object
```

#### Deleting documents

```python
# Delete the document with ID 148 from the store:
api.document.get(148).delete()
```

#### Adding bundles

```python
# Get document with this ID's bundles
api.document.get(148).add_bundle(prov_bundle, 'ex:bundle-1')
# or the shorthand:
api.document.get(148).bundles['ex:bundle-1'] = prov_bundle
```

#### Fetching bundle

```python
# Get document's bundle with matching identifier
api.document.get(148).bundles['ex:bundle-1']
```

#### Iterating over bundles
```python
# Get document with this ID's bundles
for bundle in api.document.get(148).bundles:
    # print the bundle's identifier
    print bundle.identifier
    # the bundle's provenance is at:
    bundle.prov
```


## Contribute

- Issue Tracker: https://github.com/millar/provstore-api/issues
- Source Code: https://github.com/millar/provstore-api

## Documentation

- Available on [ReadTheDocs](http://provstore-api.readthedocs.org/en/latest/)

### API
- See the [full API reference](http://provstore-api.readthedocs.org/en/latest/provstore.html)

## License

This project is licensed under the MIT license.

## Contributors

Sam Millar &lt;http://millar.io&gt;
