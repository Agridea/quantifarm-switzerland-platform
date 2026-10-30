from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace
import string
from _decimal import Decimal


class QCSM(DefinedNamespace):
    _NS = Namespace("https://quantifarm.eu/ontology/")
    DigitalAgriculturalTechnology: URIRef
    TechnologyProvider: URIRef
    hasSource: string
    hasLaunchYear: URIRef
    lastUpdateYear: URIRef
    hasKeyword: URIRef
    hasSupportedLanguage: URIRef
    hasWebPage: URIRef
    isTargetedTowardsAgriculturalSector: string
    hasFunctionality: string
    hasBenefits: string
    hasDigitalForm: string
    hasTitle: string
    hasDescription: string
    hasProvider: URIRef
    isTargetedTowardsCountry: URIRef
    canBeUsedToCultivateCropType: string
    hasCostStructure: string
    Testcase: URIRef
    isAssessingDigitalAgriculturalTechnology: URIRef
    isExecutedOnFarm: URIRef
    isAppliedOnParcel: URIRef
    hasInitialInvestmentCosts: Decimal
    hasMaintenanceCosts: Decimal
    hasMinimumInitialCosts: Decimal
    hasMaximumInitialCosts: Decimal
    hasInitialCostItem: string
    hasAnnualFeePerItem: Decimal
    hasAnnualFeeItem: string
    isParticipatingIn: URIRef
    hasExpectedLifespan: Decimal
    hasInstallationTime: Decimal
    canBeUsedToCultivateLifestockType: URIRef
    testcaseNumber: Decimal
    testcaseLeader: string
    cultivationType: string
    DatsInformation: URIRef
    datsInformation: URIRef
    
