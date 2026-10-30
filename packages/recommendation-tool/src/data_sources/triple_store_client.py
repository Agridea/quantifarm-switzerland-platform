import logging
from typing import Literal
from urllib.parse import urlparse, urlunparse

import requests

from .graph_client import GraphClient

QueryTypes = Literal["ask", "construct", "select"]

class TripleStoreClient:
    """Client to connect with a remote triple store and load graphs into graph clients.
    Currently set up for Apache Jena Fuseki stores.
    Also has functionality for executing SPARQL queries on the store.
    
    Args:
        endpoint (str): Full triple store endpoint URL. Format as \"http://www.example.com:80/storename\".
    """

    def __init__(self, endpoint: str):
        self.logger = logging.getLogger("TripleStore")

        try:
            self.set_triple_store_endpoint(endpoint)
        except ValueError as e:
            self.logger.error(
                f"Cannot parse triple store endpoint URL: {endpoint}, "
                f"caught error:\n{e}"
            )
            return
        
        self.test_connection()
        return
    
    def test_connection(self) -> None:
        """ Tests the connection with the triple store endpoint that is stored."""
        # Use simple ask query to check if the store contains any triple.
        test_query = "ASK WHERE { ?s ?p ?o }"
        try:
            _ = self.sparql_request(test_query, "ask")
        except Exception as e:
            self.logger.error(f"Error connecting to triple store, "
                              f"URL: {self._endpoint} \n{e}")
            return
        
        self.logger.info(f"Triple store endpoint is responding, URL: {self._endpoint}")
        return

    def set_triple_store_endpoint(self, endpoint: str) -> None:
        """Parses the triple store endpoint and sets the query and data endpoint.

        Args:
            endpoint (str): The endpoint to parse.

        Raises:
            ValueError: If the endpoint is invalid.
        """
        parsed = urlparse(endpoint)
        if parsed.netloc == "":
            raise ValueError(
                f"Provided endpoint is parsed with empty network location part, "
                f"please provide endpoint as \"http://www.example.com:80/\". "
                f"Endpoint URL: {endpoint}"
            )

        if not parsed.path.startswith("/quantifarm"):
            self.logger.warning(
                f"Provided endpoint url does not have a path that starts with "
                f"\"/quantifarm\", are you sure this is the correct endpoint? "
                f"URL: {endpoint}"
            )
        
        self._endpoint = urlunparse(parsed) \
                         .removesuffix("/query") \
                         .removesuffix("/data") \
                         .removesuffix("/get")
        self._query_endpoint = self._endpoint + "/query"
        self._data_endpoint = self._endpoint + "/data"
        return


    def load_graph(self, graph_client: GraphClient) -> None:
        """
        #TODO
        """
        query = (f"CONSTRUCT {{ ?s ?p ?o }} \n"
                 f"FROM {graph_client.uri.n3()} \n"
                 f"WHERE {{ ?s ?p ?o }}")
        
        data = self.sparql_request(query, "construct")
        graph_client.graph.parse(data=data, format='json-ld')
        return

    
    def sparql_request(self, query: str, type: QueryTypes = "select") -> dict:
        """SPARQL request function that sends a query to the triple store query 
        endpoint and returns data in JSON format.
        
        Args:
            query (str): a formatted SPARQL query (see 
                         https://www.w3.org/TR/rdf-sparql-query/#QueryForms)
            type (str): the type of SPARQL query to execute. Options: "ask", 
                        "construct", "select"
        
        Raises:
            ValueError: If the query or type is invalid.
            ConnectionError: If received status code 404 from triple store.
            Exception: If received another error code from triple store.
        """
        match type:
            case "ask" | "select":
                accepted_format = "json"
            case "construct":
                accepted_format = "ld+json"
            case _:
                raise ValueError(f"Provided query type unknown: \"{type}\"")
        
        response = requests.get(self._query_endpoint, 
                                params={"query": query}, 
                                headers={"Accept": f"application/{accepted_format}"})
        if response.ok:
            return response.json()
        elif response.status_code == 400:
            raise ValueError(f"Provided query leads to invalid request, query {query}")
        elif response.status_code == 404:
            raise ConnectionError(
                f"Triple store endpoint can not be found, URL: {self._endpoint}"
            )
        else:
            raise Exception(f"Received status {response.status_code} from triple store")


    @property
    def endpoint_url(self) -> str:
        return self._endpoint
    
    @property
    def query_endpoint_url(self) -> str:
        return self._query_endpoint
    
    @property
    def data_endpoint_url(self) -> str:
        return self._data_endpoint

