from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class WGS84(DefinedNamespace):
    _NS = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
    location: URIRef
    lat: URIRef
    long: URIRef
    alt: URIRef
