import logging

from src.data_sources import FarmerProfileGraphClient
from src.models import FarmerProfileEntry


def build_recommend_query(
    farmer_profile: FarmerProfileGraphClient, 
    logger: logging.Logger, 
    literals_mapping: dict
) -> str:
    query = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX qcsm: <https://quantifarm.eu/ontology/>
            PREFIX qfdata: <https://quantifarm.eu/data/>
            PREFIX gs1: <https://gs1.org/voc/>
            SELECT ?dat ?name 
            WHERE {
                ?dat a qcsm:DigitalAgriculturalTechnology .
                ?dat rdfs:label ?name ."""

    for name, entry in farmer_profile:
        if entry is None:
            continue
        if name == "other":
            continue
        query += _add_farmer_profile_entry_for_where(
            name, 
            entry, 
            logger, 
            literals_mapping
        )

    query += "\n}"

    logger.debug(f"Produced the following SPARQL query from farmer profile:\n {query}")

    return query


# ADD PATTERNS #
def _add_farmer_profile_entry_for_where(
    entry_name: str, 
    entry: FarmerProfileEntry | list[FarmerProfileEntry],
    logger: logging.Logger,
    literals_mapping: dict
) -> str:
    result = ""
    # if not entry.requireExactMatch:
    #     result += f"OPTIONAL {{"

    values = [e.value for e in entry] if isinstance(entry, list) else [entry.value]
    match entry_name:
        case "language":
            result += f"""?dat qcsm:hasSupportedLanguage ?{entry_name} . 
                VALUES ?{entry_name} {{\"{'" "'.join(values)}\"}} .
                """
        case "farm_type":
            listed = list()
            for value in values:
                listed.extend(literals_mapping["farm_type"][value])
            result += f"""?dat qcsm:isTargetedTowardsAgriculturalSector ?{entry_name} . 
                VALUES ?{entry_name} {{\"{'" "'.join(listed)}\"}} .
                """
        case "country":
            result += f"""?dat qcsm:isTargetedTowardsCountry ?country . 
                    ?country a gs1:Country . 
                    ?country gs1:countryCode ?countryCode . 
                    ?country rdfs:label ?countryName . 
                    VALUES ?countryName {{\"{'" "'.join(values)}\"}} .
                    """
        case "functionalities":
            listed = list()
            for value in values:
                listed.extend(literals_mapping["functionalities"][value])
            result += f"""?dat qcsm:hasFunctionality ?{entry_name} . 
                VALUES ?{entry_name} {{\"{'" "'.join(listed)}\"}} .
                """
        case "digital_forms":
            listed = list()
            for value in values:
                listed.extend(literals_mapping["digital_forms"][value])
            result += f"""?dat qcsm:hasDigitalForm ?{entry_name} . 
                VALUES ?{entry_name} {{\"{'" "'.join(listed)}\"}} .
                """
        case "benefits":
            listed = list()
            for value in values:
                listed.extend(literals_mapping["benefits"][value])
            result += f"""?dat qcsm:hasBenefits ?{entry_name} . 
                VALUES ?{entry_name} {{\"{'" "'.join(listed)}\"}} .
                """
        # Case for profile entries not used in recommendation of DATs
        case "other":
            pass
        case _:
            logger.warning(
                f"Adding '{entry_name}' FarmerProfileEntry for SPARQL query not "
                f"implemented. Please implement in QueryBuilder.")
            pass
    # if not entry.requireExactMatch:
    #     result += f"}}"

    return result
