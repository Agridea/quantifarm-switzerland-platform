from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class SF(DefinedNamespace):
    _NS = Namespace("http://www.opengis.net/ont/sf#")
    Polygon: URIRef
