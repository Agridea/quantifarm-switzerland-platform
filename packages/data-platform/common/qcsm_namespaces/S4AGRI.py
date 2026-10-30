from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace
import string
from _datetime import datetime


class S4AGRI(DefinedNamespace):
    _NS = Namespace("https://saref.etsi.org/saref4agri/")
    Farm: URIRef
    hasName: URIRef
    contains: URIRef
    inBiogeographicalRegion: string
    hasArea: string
    CropCycle: URIRef
    hasCycle: URIRef
    hasStartDatetime: datetime
    hasEndDatetime: datetime
