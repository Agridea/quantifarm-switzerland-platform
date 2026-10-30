from time import sleep
import logging
import json
import os
from urllib.parse import urlparse
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD
from qcsm_namespaces import QCSM, S4AGRI, GS1
from qcsm_utils.querying import sparql_select
import requests
from xlrd import open_workbook
import pprint
import json

logger = logging.getLogger(__name__)

FAIRSHARE_FILE_PATH = os.getenv("FAIRSHARE_FILE_PATH", "./fairshare-dats-30-09-2026.json")
TESTCASE_FILE_PATH = os.getenv("TESTCASE_FILE_PATH", "./testcase-dats.xls")
COST_BENEFIT_ARABLE_FILE_PATH = os.getenv("COSTBENEFITARABLEDATS_FILE_PATH", "./cost-benefit-arable-dats.xls")
COST_BENEFIT_LIFESTOCK_FILE_PATH = os.getenv("COSTBENEFITLIFESTOCKDATS_FILE_PATH", "./cost-benefit-lifestock-dats.xls")
ISO3166_PATH = os.getenv("ISO3166_PATH","./ISO3166-country-code-name.json")
WEBSITE_FILE_PATH = os.getenv("WEBSITE_FILE_PATH", "./website-registered-dats.xls")

TRIPLE_STORE_ENDPOINT = os.getenv("TRIPLE_STORE_ENDPOINT", "http://triple-store:3030")
GRAPH_NAME = "https://quantifarm.eu/graphs/dats"
NAMESPACE = Namespace("https://quantifarm.eu/data/")

ISO3166_mapping = {}


def collect_country_codes():
    with open(ISO3166_PATH) as f:
        ISO3166_countries = json.load(f)
        for country in ISO3166_countries:
            ISO3166_mapping[country['Name']] = country['Code']
        #for m in ISO3166_mapping.keys():
        #    print(m, ISO3166_mapping[m])
             

def map_to_graph(data_namespace: Namespace = Namespace("http://example.org")) -> Graph:
    g = Graph()
    nr_of_dats = 0
    dat_uris = []

    # First go through all FairShare DATs
    logger.info(" ============ Let's first go through the Fairshare DATs!! ============")
    with open(FAIRSHARE_FILE_PATH) as f:
        fairshare_dats = json.load(f)
        for fairshare_dat in fairshare_dats:
            nr_of_dats = nr_of_dats + 1
            dat_name = fairshare_dat["name"].replace(" ","_").lower()
            dat = data_namespace[f"dats/{dat_name}"]
            #dat = data_namespace[f"dats/{fairshare_dat['_id']['$oid']}"]
            g.add((dat, QCSM.hasSource, Literal("fairshare")))
            if dat not in dat_uris:
                dat_uris.append(dat)
                g.add((dat, RDF.type, QCSM.DigitalAgriculturalTechnology))
                g.add((dat, RDFS.label, Literal(fairshare_dat["name"])))
                g.add((dat, QCSM.hasTitle, Literal(fairshare_dat["title"])))
                g.add((dat, RDFS.comment, Literal(fairshare_dat["desc"])))
                try:
                    launch_year = int(fairshare_dat["launchYear"])
                    g.add(
                        (dat, QCSM.hasLaunchYear, Literal(launch_year, datatype=XSD.gYear))
                    )
                except ValueError:
                    logger.warning(
                        f"{dat} doesn't have a valid launch year but '{fairshare_dat['launchYear']}'."
                    )
    
                try:
                    update_year = int(fairshare_dat["updateYear"])
                    g.add(
                        (dat, QCSM.lastUpdateYear, Literal(update_year, datatype=XSD.gYear))
                    )
                except ValueError:
                    logger.warning(
                        f"{dat} doesn't have a valid update year but '{fairshare_dat['updateYear']}'."
                    )
    
                keywords = [kw.strip() for kw in fairshare_dat["keywords"].split(",")]
                for keyword in keywords:
                    if len(keywords) == 1 and keyword == "null":
                        break
                    elif len(keyword) == 0:
                        continue
                    g.add((dat, QCSM.hasKeyword, Literal(keyword)))
    
                sectors = fairshare_dat["sector"]
                for sector in sectors:
                    g.add((dat, QCSM.isTargetedTowardsAgriculturalSector, Literal(sector)))
    
                challenges = fairshare_dat["challenges"]
                for challenge in challenges:
                    g.add((dat, QCSM.hasFunctionality, Literal(challenge)))
    
                benefits = fairshare_dat["benefits"]
                for benefit in benefits:
                    g.add((dat, QCSM.hasBenefits, Literal(benefit)))
    
                languages = fairshare_dat["languages"]
                for language in languages:
                    g.add((dat, QCSM.hasSupportedLanguage, Literal(language)))
    
                deliveries = fairshare_dat["delivery"]
                for delivery in deliveries:
                    g.add((dat, QCSM.hasDigitalForm, Literal(delivery)))
    
                web_pages = fairshare_dat["website"].split()
                for web_page in web_pages:
                    if is_url(web_page):
                        g.add((dat, QCSM.hasWebPage, URIRef(web_page)))
                    elif is_url("https://" + web_page):
                        logger.warning(
                            f"prepended 'https://' to {web_page} to make it a valid URL."
                        )
                        g.add((dat, QCSM.hasWebPage, URIRef("https://" + web_page)))
                    else:
                        logger.warning(
                            f"{web_page} doesn't seem to be a valid URL; skipped it."
                        )
                
                try:
                    provider = data_namespace[f"providers/{fairshare_dat['providerName'].replace(' ','_')}"]
                    g.add((provider, RDF.type, QCSM.TechnologyProvider))
                    g.add((provider, S4AGRI.hasName, Literal(fairshare_dat["providerName"])))
                    g.add((dat, QCSM.hasProvider, provider))
                except ValueError:
                    logger.warning(
                        f"{provider} doesn't have a valid name but '{fairshare_dat['providerName']}'."
                    )
    
                countries = fairshare_dat["countries"]
                for c in countries:
                    if c in ISO3166_mapping.keys():
                        country = data_namespace[f"countries/{c.replace(' ','_')}"]
                        g.add((country, RDF.type, GS1.Country))
                        g.add((country, RDFS.label, Literal(c)))
                        g.add((country, GS1.countryCode, Literal(ISO3166_mapping[c])))
                        g.add((dat, QCSM.isTargetedTowardsCountry, country))
                    else:
                        logger.warning(
                            f"{c} is not in the ISO3166 list of countries."
                        )
                
                try:
                    if fairshare_dat["cost"] != "null":
                        g.add((dat, QCSM.hasCostStructure, Literal(fairshare_dat["cost"])))                    
                except ValueError:
                    logger.warning(
                        f"{fairshare_dat['name']} doesn't have a cost structure defined."
                    )
            else:
                print("existing DAT:", dat, "of provider ",fairshare_dat['providerName'])

    # Second, go through all testcase DATs
    logger.info(" ============ Let's secondly go through the Testcase DATs!! ============= ")
    wb = open_workbook(TESTCASE_FILE_PATH)
    sh = wb.sheet_by_index(5)
    for rx in range(sh.nrows):
        if rx > 1:
            nr_of_dats = nr_of_dats + 1
            dat_name = sh.cell_value(rx,2).replace(" ","_").lower()
            dat = data_namespace[f"dats/{dat_name}"]
            g.add((dat, QCSM.hasSource, Literal("testcase")))
            try:
                testcase_number = sh.cell_value(rx,0).replace(" ","").replace("TC","")
                if testcase_number == "":
                    raise ValueError
                testcase = data_namespace[f"testcases/testcase{testcase_number}"]
                #print(nr_of_dats, provider)
                g.add((dat, QCSM.isUsedInTestcase, testcase))
            except ValueError:
                logger.warning(
                    f"{dat} has no testcase number."
                )
            if dat not in dat_uris:
                dat_uris.append(dat)
                #print(dat)
                g.add((dat, RDF.type, QCSM.DigitalAgriculturalTechnology))
                #print(sh.cell_value(rx,2))
                g.add((dat, RDFS.label, Literal(sh.cell_value(rx,2))))
                g.add((dat, QCSM.hasTitle, Literal(sh.cell_value(rx,2))))
                #print(sh.cell_value(rx,4))
                g.add((dat, RDFS.comment, Literal(sh.cell_value(rx,4))))
                g.add((dat, QCSM.hasDescription, Literal(sh.cell_value(rx,4))))
                try:
                    provider_name = sh.cell_value(rx,3).replace(" ","_")
                    if provider_name == "":
                        raise ValueError
                    provider = data_namespace[f"providers/{provider_name}"]
                    #print(nr_of_dats, provider)
                    g.add((provider, RDF.type, QCSM.TechnologyProvider))
                    g.add((provider, S4AGRI.hasName, Literal(provider_name)))
                    g.add((dat, QCSM.hasProvider, provider))
                except ValueError:
                    logger.warning(
                        f"{dat} has an empty provider name."
                    )
                try:
                    if sh.cell_value(rx,5) == "":
                        raise ValueError
                    g.add((dat, QCSM.hasWebPage, URIRef(sh.cell_value(rx,5))))
                except ValueError:
                    logger.warning(
                        f"{dat} has an empty webpage."
                    )
                # add cost structure
                g.add((dat, QCSM.hasCostStructure, Literal(sh.cell_value(rx,6))))
                
            # add in both cases: sector 7, functionality 8, country 9, languages 10, digital form 11, benefits 12
            sectors = [sector.strip().capitalize() for sector in sh.cell_value(rx,7).split(",")]
            for sector in sectors:
                g.add((dat, QCSM.isTargetedTowardsAgriculturalSector, Literal(sector)))
            functions = [function.strip().capitalize() for function in sh.cell_value(rx,8).split(",")]            
            for function in functions:
                g.add((dat, QCSM.hasFunctionality, Literal(function)))
                #logger.info(f"function = {function}")
                
            countries = [c.strip().capitalize() for c in sh.cell_value(rx,9).split(",")]
            for c in countries:
                if c in ISO3166_mapping.keys():
                    country = data_namespace[f"countries/{c.replace(' ','_')}"]
                    g.add((country, RDF.type, GS1.Country))
                    g.add((country, RDFS.label, Literal(c)))
                    g.add((country, GS1.countryCode, Literal(ISO3166_mapping[c])))
                    g.add((dat, QCSM.isTargetedTowardsCountry, country))
                else:
                    logger.warning(
                        f"{c} is not in the ISO3166 list of countries."
                    )
            
            languages = [l.strip().capitalize() for l in sh.cell_value(rx,10).split(",")]
            for language in languages:
                g.add((dat, QCSM.hasSupportedLanguage, Literal(language)))
            deliveries = [d.strip().capitalize() for d in sh.cell_value(rx,11).split(",")]
            for delivery in deliveries:
                g.add((dat, QCSM.hasDigitalForm, Literal(delivery)))
                #logger.info(f"Digital form = {delivery}")
            benefits = [b.strip().capitalize() for b in sh.cell_value(rx,12).split(",")]
            for benefit in benefits:
                g.add((dat, QCSM.hasBenefits, Literal(benefit)))
                logger.info(f"Benefit = {benefit}")

    # Third, go through all website registered DATs
    logger.info(" ============ Let's thirdly go through the Website registered DATs!! ============")
    wb = open_workbook(WEBSITE_FILE_PATH)
    sh = wb.sheet_by_index(0)
    for rx in range(sh.nrows):
        if rx > 2:
            nr_of_dats = nr_of_dats + 1
            dat_name = sh.cell_value(rx,1).replace(" ","_").lower()
            dat = data_namespace[f"dats/{dat_name}"]
            g.add((dat, QCSM.hasSource, Literal("website")))
            if dat not in dat_uris:
                dat_uris.append(dat)
                logger.info(dat)
                g.add((dat, RDF.type, QCSM.DigitalAgriculturalTechnology))
                #print(sh.cell_value(rx,2))
                g.add((dat, RDFS.label, Literal(sh.cell_value(rx,1))))
                g.add((dat, QCSM.hasTitle, Literal(sh.cell_value(rx,1))))
                #print(sh.cell_value(rx,4))
                g.add((dat, RDFS.comment, Literal(sh.cell_value(rx,12))))
                g.add((dat, QCSM.hasDescription, Literal(sh.cell_value(rx,12))))
                try:
                    provider_name = sh.cell_value(rx,4).replace(" ","_")
                    if provider_name == "":
                        raise ValueError
                    provider = data_namespace[f"providers/{provider_name}"]
                    #print(nr_of_dats, provider)
                    g.add((provider, RDF.type, QCSM.TechnologyProvider))
                    g.add((provider, S4AGRI.hasName, Literal(provider_name)))
                    g.add((dat, QCSM.hasProvider, provider))
                except ValueError:
                    logger.warning(
                        f"{dat} has an empty provider name."
                    )
                try:
                    if sh.cell_value(rx,10) == "":
                        raise ValueError
                    g.add((dat, QCSM.hasWebPage, URIRef(sh.cell_value(rx,10))))
                except ValueError:
                    logger.warning(
                        f"{dat} has an empty webpage."
                    )
                functionalities = [function.strip().capitalize() for function in sh.cell_value(rx,6).split(",")]            
                for function in functionalities:
                    g.add((dat, QCSM.hasFunctionality, Literal(function)))
                sectors = [sector.strip().capitalize() for sector in sh.cell_value(rx,14).split(",")]            
                for sector in sectors:
                    if sector == "Arable": sector = "Arable farming"
                    g.add((dat, QCSM.isTargetedTowardsAgriculturalSector, Literal(sector)))  
                    #logger.info(f"Sector = {sector}")
                g.add((dat, QCSM.hasCostStructure, Literal(sh.cell_value(rx,17))))
                
            else:
                logger.info("existing DAT:", dat, "of provider",sh.cell_value(rx,3).replace(" ","_"))

    # Fourth, go through all cost-benefit DATs
    logger.info(" =========== Let's fourthly go through the cost-benefit DATs!! ===========")
    filenames = [COST_BENEFIT_ARABLE_FILE_PATH,COST_BENEFIT_LIFESTOCK_FILE_PATH]
    for file in filenames:   
        logger.info(f" =========== Let's go through {file}!! ===========")
        wb = open_workbook(file)
        sh = wb.sheet_by_index(0)
        for rx in range(sh.nrows):
            if rx > 1:
                nr_of_dats = nr_of_dats + 1
                dat_name = sh.cell_value(rx,3).replace(" ","_").lower()
                dat = data_namespace[f"dats/{dat_name}"]
                #print(dat)
                g.add((dat, QCSM.hasSource, Literal("costbenefit")))
                if dat not in dat_uris:
                    dat_uris.append(dat)
                    g.add((dat, RDF.type, QCSM.DigitalAgriculturalTechnology))
                    
                    functionalities = [function.strip().capitalize() for function in sh.cell_value(rx,18).split(",")] #must be column 17
                    for function in functionalities:
                        g.add((dat, QCSM.hasFunctionality, Literal(function)))
                        logger.info(f"Function = {function}")
                    
                    g.add((dat, RDFS.label, Literal(sh.cell_value(rx,3))))
                    g.add((dat, QCSM.hasTitle, Literal(sh.cell_value(rx,3))))
                    try:
                        provider_name = sh.cell_value(rx,4).replace(" ","_")
                        if provider_name == "":
                            raise ValueError
                        provider = data_namespace[f"providers/{provider_name}"]
                        g.add((provider, RDF.type, QCSM.TechnologyProvider))
                        g.add((provider, S4AGRI.hasName, Literal(provider_name)))
                        g.add((dat, QCSM.hasProvider, provider))
                    except ValueError:
                        logger.warning(
                            f"{dat} has an empty provider name."
                        )
                    g.add((dat, RDFS.comment, Literal(sh.cell_value(rx,5))))
                    g.add((dat, QCSM.hasDescription, Literal(sh.cell_value(rx,5))))
                    g.add((dat, QCSM.hasWebPage, URIRef(sh.cell_value(rx,6))))
                    cultivation_types = [ct.strip().capitalize() for ct in sh.cell_value(rx,8).split(",")]
                    for cultivation_type in cultivation_types:
                        if file == COST_BENEFIT_ARABLE_FILE_PATH:
                            if cultivation_type == "All" or cultivation_type == "Arable": cultivation_type = "Arable farming"
                            g.add((dat, QCSM.canBeUsedToCultivateCropType, Literal(cultivation_type)))
                            g.add((dat, QCSM.isTargetedTowardsAgriculturalSector, Literal(cultivation_type)))
                            #logger.info(f"Sector = {cultivation_type}")
                        else:
                            if cultivation_type == "All": cultivation_type = "Livestock"
                            g.add((dat, QCSM.canBeUsedToCultivateLifestockType, Literal(cultivation_type)))                            
                            g.add((dat, QCSM.isTargetedTowardsAgriculturalSector, Literal(cultivation_type)))
                            #logger.info(f"Sector = {cultivation_type}")
                    g.add((dat, QCSM.hasMinimumInitialCosts, Literal(sh.cell_value(rx,9), datatype=XSD.decimal)))
                    g.add((dat, QCSM.hasMaximumInitialCosts, Literal(sh.cell_value(rx,10), datatype=XSD.decimal)))
                    g.add((dat, QCSM.hasInitialCostItem, Literal(sh.cell_value(rx,11))))
                    g.add((dat, QCSM.hasAnnualFeePerItem, Literal(sh.cell_value(rx,12), datatype=XSD.decimal)))
                    g.add((dat, QCSM.hasAnnualFeeItem, Literal(sh.cell_value(rx,13))))
                    
                    if sh.cell_value(rx,10) > 0:
                        value = "Initial investment costs"
                        if sh.cell_value(rx,11) != "none":
                            value = value + " per " + sh.cell_value(rx,11)
                        if sh.cell_value(rx,12) > 0:
                            value = value + " and Annual fee"
                            if sh.cell_value(rx,13) != "none":
                                value = value + " per " + sh.cell_value(rx,13)
                    else:                    
                        if sh.cell_value(rx,12) > 0:
                            value = "Annual fee"
                            if sh.cell_value(rx,13) != "none":
                                value = value + " per " + sh.cell_value(rx,13)
                    #print(value)
                    g.add((dat, QCSM.hasCostStructure, Literal(value)))
                    deliveries = [d.strip().capitalize() for d in sh.cell_value(rx,21).split(",")]
                    for delivery in deliveries:
                        g.add((dat, QCSM.hasDigitalForm, Literal(delivery)))
                        #logger.info(f"Digital form = {delivery}")
                    benefits = [b.strip().capitalize() for b in sh.cell_value(rx,22).split(",")]
                    for benefit in benefits:
                        g.add((dat, QCSM.hasBenefits, Literal(benefit)))
                        logger.info(f"Benefit = {benefit}")
                else:
                    print("existing DAT:", dat, "of provider",sh.cell_value(rx,4).replace(" ","_"))
                    # add functionality in column 2
                    functionalities = [function.strip().capitalize() for function in sh.cell_value(rx,18).split(",")]            
                    for function in functionalities:
                        g.add((dat, QCSM.hasFunctionality, Literal(function)))
                        #logger.info(f"Function = {function}")
                    deliveries = [d.strip().capitalize() for d in sh.cell_value(rx,21).split(",")]
                    for delivery in deliveries:
                        g.add((dat, QCSM.hasDigitalForm, Literal(delivery)))
                        #logger.info(f"Digital form = {delivery}")
                    benefits = [b.strip().capitalize() for b in sh.cell_value(rx,22).split(",")]
                    for benefit in benefits:
                        g.add((dat, QCSM.hasBenefits, Literal(benefit)))
                        logger.info(f"Benefit = {benefit}")

    print("nr of dats processed is:", nr_of_dats)
    print("nr of DAT uris is:", len(dat_uris))
    #data=g.serialize(format="nt", encoding="utf-8"),
    #print(data)

    return g


def check_triplestore():
    print("Hello, checking triplestore for correct input!")
    r = sparql_select(
        f"{TRIPLE_STORE_ENDPOINT}/quantifarm/query",
        """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX qcsm: <https://quantifarm.eu/ontology/>
            PREFIX s4agri: <https://saref.etsi.org/saref4agri/>
            PREFIX gs1: <https://gs1.org/voc/>
            SELECT DISTINCT ?sector
            FROM <https://quantifarm.eu/graphs/dats>
            WHERE {
                ?dat a qcsm:DigitalAgriculturalTechnology .
                ?dat rdfs:label ?datname .
                #?dat qcsm:hasFunctionality ?func .
                ?dat qcsm:isTargetedTowardsAgriculturalSector ?sector .
                #?dat qcsm:hasProvider ?provider .
                #?provider s4agri:hasName ?provname .
            }
        """,
    )
    data = [{b["sector"]["value"]} for b in r["results"]["bindings"]]
    print(data)
    #for b in r["results"]["bindings"]:
        #print(b['provname']['value'])
        #print(b['datname']['value'], ' ====== ', b['func']['value'])


def check_triplestore1():
    print("Hello, checking triplestore for correct input!")
    r = sparql_select(
        f"{TRIPLE_STORE_ENDPOINT}/quantifarm/query",
        """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX qcsm: <https://quantifarm.eu/ontology/>
            PREFIX s4agri: <https://saref.etsi.org/saref4agri/>
            PREFIX gs1: <https://gs1.org/voc/>
            #SELECT (COUNT(DISTINCT ?function) AS ?count) WHERE {
            SELECT DISTINCT ?function WHERE {
                ?dats a qcsm:DigitalAgriculturalTechnology .
                #?dats qcsm:hasFunctionality ?function .
                #?dats qcsm:hasDigitalForm ?function .
                ?dats qcsm:hasBenefits ?function . 
                #?country a gs1:Country .
                #?country gs1:countryCode ?code .
                #?country rdfs:label ?name .
            }
            ORDER BY ?function
        """,
    )
    #print(r["results"]["bindings"])
    dattoprov = [{b["function"]["value"]} for b in r["results"]["bindings"]]
    #dattoprov = [{b["country"]["value"],b["code"]["value"],b["name"]["value"]} for b in r["results"]["bindings"]]
    print(dattoprov)


def wait_for_connection(ping_url, sleep_s=1):
    connected = False
    while not connected:
        try:
            resp = requests.get(ping_url)
            connected = resp.ok
            if not resp.ok:
                logger.warn(f"received http {resp.status_code}")
        except Exception as e:
            logger.exception("an exception occurred while pinging the triple store")
        finally:
            if not connected:
                logger.info("waiting for connection to triple store to be alive...")
                sleep(sleep_s)


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.netloc.count(".") > 0])
    except ValueError:
        return False


def put_graph(g: Graph, graph_store_endpoint: str, graph_name: str):
    logger.info("PUTting data into DATS graph...")
    requests.put(
        graph_store_endpoint,
        params={"graph": graph_name},
        headers={"Content-Type": "application/n-triples"},
        data=g.serialize(format="nt", encoding="utf-8"),
    )

def check_fairshare():
    resp = requests.get("https://api.fairshare-pnf.eu/api/tools")
    if resp.ok:
         result = resp.json()
         tools = result["tools"]
         #pprint.pp(result["tools"][0])
         with open(FAIRSHARE_FILE_PATH, 'w', encoding='utf-8') as f:
             json.dump(tools, f, ensure_ascii=False, indent=2)
         logger.info(f"Wrote {len(tools)} tools to {FAIRSHARE_FILE_PATH}")
    else:
         logger.warning(f"Failed to fetch FairShare data: HTTP {resp.status_code}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    collect_country_codes()
    g = map_to_graph(data_namespace=NAMESPACE)
    logger.info(f'Connecting to endpoint {TRIPLE_STORE_ENDPOINT}')
    wait_for_connection(f"{TRIPLE_STORE_ENDPOINT}/$/ping")
    put_graph(g, f"{TRIPLE_STORE_ENDPOINT}/quantifarm/data", GRAPH_NAME)
    check_triplestore1()
    