from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace

class QCSM(DefinedNamespace):
    _NS = Namespace("https://quantifarm.eu/ontology/")
    DigitalAgriculturalTechnology: URIRef
    TechnologyProvider: URIRef
    hasLaunchYear: URIRef
    lastUpdateYear: URIRef
    hasKeyword: URIRef
    hasSupportedLanguage: URIRef
    hasWebPage: URIRef
    isTargetedTowardsAgriculturalSector: str
    hasFunctionality: str
    hasBenefits: str
    hasDigitalForm: str
    hasTitle: str
    hasProvider: URIRef
    isTargetedTowardsCountry: URIRef
    hasCostStructure: str
    isUsedInTestcase: URIRef
    hasSource: str
    

    # Test case graphs
    Testcase: URIRef
    hasTestcaseNumber: URIRef
    hasDatsInformation: URIRef
    hasDatsName: URIRef

    # TODO: Are not in QCSM yet actually
    assesses: URIRef  # for linking test cases to DATs [test case] assesses [DAT]
    participatesIn: URIRef  # for linking parcels to test cases
    uses: URIRef  # for linking parcels to DATs


    # HACK: Fake property for mapping farmer profile options to literals in DAT data
    mapsTo_FAKE: URIRef

    # HACK: Also fake
    canUseTechnology_FAKE: URIRef
    requiresFunctionality_FAKE: URIRef
    wantsBenefits_FAKE: URIRef
    
