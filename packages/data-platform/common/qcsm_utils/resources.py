from rdflib import Namespace, URIRef
import hashlib


def create_hash_resource(namespace: Namespace, source: str) -> URIRef:
    """Given a namespace and a unique source string, returns a
        deterministric URIRef.

    Args:
        namespace (Namespace): Namespace that the returned URIRef will
            be defined in.
        source (str): Source string where to create the deterministically
            'random' part of the URI from.

    Returns:
        URIRef: URI in the namespace that is deterministically unique.
            (In as far as MD5 creates unique hashes)
    """
    digest = hashlib.md5(source.encode("utf-8")).hexdigest()
    return namespace[digest]
