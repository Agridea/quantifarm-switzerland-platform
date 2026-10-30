import requests


def sparql_construct_where(endpoint, query):
    resp = requests.get(
        endpoint, params={"query": query}, headers={"Accept": "application/ld+json"}
    )
    if resp.ok:
        return resp.json()
    elif resp.status_code == 400:
        raise ValueError("Bad request to SPARQL endpoint")
    else:
        raise Exception(f"received status {resp.status_code} from triple store")


def sparql_select(endpoint, query):
    resp = requests.get(
        endpoint, params={"query": query}, headers={"Accept": "application/json"}
    )
    if resp.ok:
        return resp.json()
    elif resp.status_code == 400:
        raise ValueError("Bad request to SPARQL endpoint")
    else:
        raise Exception(f"received status {resp.status_code} from triple store")
