from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class GEO(DefinedNamespace):
    _NS = Namespace("http://www.opengis.net/ont/geosparql#")
    asWKT: URIRef
    wktLiteral: URIRef
    hasGeometry: URIRef
