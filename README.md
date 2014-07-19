provstore
=========

Client for the [ProvStore](https://provenance.ecs.soton.ac.uk/store/)'s [API](https://provenance.ecs.soton.ac.uk/store/help/api/).

## Installation
```bash
pip install provstore-api
```

## Usage

To use the client import the API and configure your access credentials:

```python
from provstore.api import Api

# API key can be found at https://provenance.ecs.soton.ac.uk/store/account/developer/
api = Api(userame="your_provstore_username", api_key="your_api_key")
```

*Note: credentials can also be set via the `PROVSTORE_USERNAME` and `PROVSTORE_API_KEY` environment variables and ommited from the initialization.*

For demonstrations purposes we will use the ProvDocuments given in the examples module like so
```python
import provstore.tests.examples as examples
```

but you would use your documents instead

```python
prov_document = examples.flat_document()
prov_bundle = examples.flat_document()

# Store the document to ProvStore:
#   - the public parameter is optional and defaults to False
stored_document = api.document.create(prov_document,
                                      name="name",
                                      public=False)

# => This will store the document and return a ProvStore Document object

# Document instance has the following API:
#
#   property: id(int) -> the document's ID on the Store
#   property: name(string) -> the document's name on Store
#   property: public(bool) -> wether the document is publicly visible
#   property: owner(string) -> owner's username
#   property: created_at(datetime) -> when the document was uploaded
#   property: views(int) -> document view count
#   property: prov(ProvDocument) -> prov model object
#   property: bundles(BundleManager) -> bundle manager
#
#   method: refresh() -> refreshes the document to update it with any changes on the server
#   method: add_bundle(<ProvBundle object>, <QName identifier for this bundle>) -> adds a bundle to the document
#   method: delete() -> permanently deletes the document from the store

# Add a bundle to the document:
stored_document.add_bundle(prov_bundle, identifier="ex:bundle-1")

# or the shorthand:
stored_document.bundles['ex:bundle-1'] = prov_document

# To later fetch the bundle or retrieve and existing bundle we use its identifier
stored_bundle = stored_document.bundles['ex:bundle-1']

# Bundle instance has the following API:
#
#   property: identifier(string) -> the bundles's identifier
#   property: created_at(datetime) -> when the document was uploaded
#   property: prov(ProvDocument) -> prov model object

# We can iterate over a documents bundles to, for example, print their identifiers:
for bundle in stored_document.bundles:
    print bundle.identifier
    # the bundle's provenance is at:
    bundle.prov
