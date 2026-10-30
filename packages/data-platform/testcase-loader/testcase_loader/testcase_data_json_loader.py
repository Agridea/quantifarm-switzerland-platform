from rdflib import RDF, Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD
from qcsm_namespaces import QCSM, S4AGRI

import logging
import json
import uuid

logger = logging.getLogger(__name__)

QFDATA = Namespace("https://quantifarm.eu/data/")




def load(data) -> Graph:
    g = Graph()
    g.bind("qcsm", QCSM)
    g.bind("s4agri", S4AGRI)
    g.bind("qcsmdata", QFDATA)
    
    # create a new class for the testcase data
    testcaseNumber = data['testcaseNumber']
    test_case = QFDATA[f"testcases/testcase{testcaseNumber}"]
    g.add((test_case, RDF.type, QCSM.Testcase))

    filename = "json-schemas/Testcase.schema.json"
    
    # call the parser of the json data based on the json schema in the file
    # this one will recursively walk through the nested json and parse with corresponding json-schemas
    parse_json_based_on_schema(test_case, filename, data, g)

    return g, testcaseNumber


    '''
    parameters are:
      1: the class in the graph to add the properties and related classes to
      2: the filename that contains the schema for this class and its properties
      3: the json itself that contains the data structured according to the schema
      4: the graph to add everything to
    '''
      
def parse_json_based_on_schema(current_class, filename, data, g) -> Graph:
    '''
    steps to take:
      1: get the properties list from the schema
      2: for each property do:
        a) if the type is integer/string/number/boolean:
          - add a triple ( class , qcsm.property , literal-of-integer-or-string )
        b) if the type is array of integers/strings/numbers:
          - loop over all items
          - add a triple ( class , qcsm.property , literal-of-integer-or-string )
        c) if the type is array of objects in a $ref:
          - loop over all items
          - get the $ref that contains the type of class of the item
          - create a new class of this type
          - add a triple ( class , qcsm.property , new-class )
          - call the recursive operation with new-class
        d) if there is no type, but only a $ref:
          - create a new class of this type
          - add a triple ( class , qcsm.property , new-class )
          - call the recursive operation with new-class 
    '''

    # get the properties from the testcase schema
    with open(filename, "r") as f:
        schema = json.load(f)
        properties = schema['properties']
        for property in properties.keys():
            logger.debug("Property is: %s", property)
            if property in data.keys():
                if 'type' in properties[property].keys():
                    type = properties[property]['type']
                    match type:
                        case "integer" | "string" | "number" | "boolean": 
                            # this is case a)
                            relation = f"has{property[0].upper()+property[1:]}"
                            range = "xsd:decimal" if type == "number" else "xsd:"+type
                            g.add((current_class, QCSM[relation], Literal(data[property])))
                        case "array":
                            # it is assumed that there is an "items" field with a type or $ref
                            if 'type' in properties[property]['items'].keys():
                                # this is case b)
                                for element in data[property]:
                                    logger.debug("Element in array is %s", element)
                                    relation = f"has{property[0].upper()+property[1:]}"
                                    range = "xsd:decimal" if type == "number" else "xsd:"+type
                                    g.add((current_class, QCSM[relation], Literal(element)))
                            elif '$ref' in properties[property]['items'].keys():
                                # this is case c)
                                schema_file = "json-schemas/" + properties[property]['items']['$ref'].split('/')[-1]
                                logger.debug(f"Schema file is: {schema_file}")
                                item_type = properties[property]['items']['$ref'].split('/')[-1].split('.')[0]
                                logger.debug(f"New class type is: {item_type}")
                                for element in data[property]:
                                    logger.debug(f"Element in array is: {element}")
                                    new_class = QFDATA[item_type + "-" + str(uuid.uuid4())]
                                    g.add((new_class, RDF.type, QCSM[item_type]))
                                    relation = f"has{property[0].upper()+property[1:]}"
                                    g.add((current_class, QCSM[relation], new_class))
                                    # call the recursive operation with the new class
                                    g = parse_json_based_on_schema(new_class, schema_file, element, g)
                                    
                            else:
                                logger.warning("Items of array property %s do not have a type or a $ref", property)
                                
                        case _: # this case is not covered yet!
                            logger.warning("This type is not covered yet: %s", type)
                elif '$ref' in properties[property].keys():
                    # this is case d)
                    schema_file = "json-schemas/" + properties[property]['$ref'].split('/')[-1]
                    logger.debug(f"Schema file is: {schema_file}")
                    item_type = properties[property]['$ref'].split('/')[-1].split('.')[0]
                    logger.debug(f"New class type is: {item_type}")
                    new_class = QFDATA[item_type + "-" + str(uuid.uuid4())]
                    g.add((new_class, RDF.type, QCSM[item_type]))
                    relation = f"has{property[0].upper()+property[1:]}"
                    g.add((current_class, QCSM[relation], new_class))
                    # call the recursive operation with the new class
                    g = parse_json_based_on_schema(new_class, schema_file, data[property], g)
                    
                else: # this case is not covered yet!
                    logger.warning("Property %s does not have a type or a $ref", property)
            else:
                logger.warning(f"Field {property} of schema {filename} not present in the provided data!")

    return g





