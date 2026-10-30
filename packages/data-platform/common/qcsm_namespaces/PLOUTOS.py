from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class PLOUTOS(DefinedNamespace):
    _NS = Namespace("https://www.tno.nl/agrifood/ontology/ploutos/common#")
    Farm: URIRef
    Parcel: URIRef
    hasToponym: URIRef
    hasAdministrator: URIRef
