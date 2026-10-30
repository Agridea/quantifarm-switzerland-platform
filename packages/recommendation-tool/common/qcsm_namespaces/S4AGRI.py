from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class S4AGRI(DefinedNamespace):
    _NS = Namespace("https://saref.etsi.org/saref4agri/")
    hasName: URIRef
    contains: URIRef
    Farm: URIRef
    Farmer: URIRef
    managesFarm: URIRef

class S4AGRI_NEW(DefinedNamespace):
    _NS = Namespace("https://saref.etsi.org/saref4agri-new/")
    prefersLanguage: URIRef
    hasFarmType: URIRef


    # Used for metapath creation, not actually in S4AGGRI
    hasAddress_FAKE: URIRef
    
