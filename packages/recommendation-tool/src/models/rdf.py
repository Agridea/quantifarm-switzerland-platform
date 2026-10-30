from typing import Annotated
from urllib.parse import unwrap

from pydantic import PlainSerializer, PlainValidator
from rdflib import Literal, URIRef
from rdflib.util import from_n3


def validate_uriref(input: str | URIRef) -> URIRef:
    if isinstance(input, URIRef):
        return input
    return URIRef(unwrap(input))

def serialize_uriref(input: URIRef) -> str:
    return input.n3()

ValidatedURIRef = Annotated[
    URIRef, 
    PlainValidator(validate_uriref), 
    PlainSerializer(serialize_uriref)
]


def validate_literal(input: str | Literal) -> Literal:
    if isinstance(input, Literal):
        return input
    return from_n3(input)

def serialize_literal(input: Literal) -> str:
    return input.n3()

ValidatedLiteral = Annotated[
    Literal, 
    PlainValidator(validate_literal), 
    PlainSerializer(serialize_literal)
]
