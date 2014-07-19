import prov.model as prov

def flat_document():
    document = prov.ProvDocument()

    ns = document.add_namespace('ex', 'http://example.com/')

    document.entity(ns['entity-1'])

    return document
