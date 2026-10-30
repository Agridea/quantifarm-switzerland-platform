from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace
import string


class GS1(DefinedNamespace):
    _NS = Namespace("https://gs1.org/voc/")
    Country: URIRef
    countryCode: URIRef
    address: URIRef
    addressCountry: URIRef
