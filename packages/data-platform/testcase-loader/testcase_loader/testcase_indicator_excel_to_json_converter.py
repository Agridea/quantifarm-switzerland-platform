from time import sleep
import logging
import json
import os, sys
from urllib.parse import urlparse
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD
from qcsm_namespaces import QCSM, S4AGRI, GS1
import requests
from xlrd import open_workbook
import pprint
import json

logger = logging.getLogger(__name__)

json_file = open("indicators.json", "w")

def convert_excel_to_json(file):
    
    logger.info("Let's open the testcase Excel!!")
    wb = open_workbook(file)
    sh = wb.sheet_by_index(8)

    json_file.write('{\n')
    
    ### 1: add the indicators that are underlying the aggregated impact categories
    json_file.write('               "calculatedIndicatorInformation": [\n')
    # first count the number of rows with a 1 in column L, i.e. number of aggregated impact indicators
    number_of_indicators = 0
    for rx in range(sh.nrows):
        if sh.cell_value(rx,11) == 1:
            number_of_indicators += 1
    logger.info(f"number of calculated indicators that underly the aggregation of impacts: {number_of_indicators}")
        
    # second run through the aggregated impact indicators in Column L and add a JSON object for each of them
    for rx in range(sh.nrows):
        if sh.cell_value(rx,11) == 1:
            #logger.info(sh.cell_value(rx,2))
            json_file.write('                  {\n')
            json_file.write('                     "indicatorName": "' + sh.cell_value(rx,2)+ '",\n')
            json_file.write('                     "indicatorUnit": "' + sh.cell_value(rx,3)+ '",\n')
            value = str(sh.cell_value(rx,4)) if sh.cell_value(rx,4) != "" else "null"
            json_file.write('                     "absoluteDifference": ' + value + ',\n')
            value = str(sh.cell_value(rx,5)) if sh.cell_value(rx,5) != "" else "null"
            json_file.write('                     "percentageDifference": ' + value + '\n')            
            json_file.write('                  }')
            
            # decrease the number of impacted KPIs dealt with
            if number_of_indicators > 1:
                json_file.write(',\n')
                number_of_indicators -= 1
            else:
                json_file.write('\n')
            
    json_file.write('               ],\n')

    # 2: add the three sustainability category scores => 3 parts in column Z
    json_file.write('               "calculatedSustainabilityInformation": [\n')
    json_file.write('                  {\n')
    json_file.write('                     "sustainabilityParameterName": "economic sustainability",\n')
    json_file.write('                     "sustainabilityParameterUnit": "percentage",\n')
    json_file.write('                     "absoluteDifference": null,\n')
    json_file.write('                     "percentageDifference": ' + str(sh.cell_value(3,25)) + '\n')
    json_file.write('                  },\n')

    json_file.write('                  {\n')
    json_file.write('                     "sustainabilityParameterName": "envionmental sustainability",\n')
    json_file.write('                     "sustainabilityParameterUnit": "percentage",\n')
    json_file.write('                     "absoluteDifference": null,\n')
    json_file.write('                     "percentageDifference": ' + str(sh.cell_value(5,25)) + '\n')
    json_file.write('                  },\n')

    json_file.write('                  {\n')
    json_file.write('                     "sustainabilityParameterName": "social sustainability",\n')
    json_file.write('                     "sustainabilityParameterUnit": "percentage",\n')
    json_file.write('                     "absoluteDifference": null,\n')
    json_file.write('                     "percentageDifference": ' + str(sh.cell_value(7,25)) + '\n')
    json_file.write('                  }\n')

    json_file.write('               ],\n')
    
    ### 3: add the 7 aggregated impact categories
    json_file.write('               "aggregatedImpactInformation": [\n')
    
    number_of_indicators = 7
    for rx in range(2,9):
        json_file.write('                  {\n')
        json_file.write('                     "aggregatedImpactName": "total ' + sh.cell_value(rx,18)+ '",\n')
        json_file.write('                     "aggregatedImpactUnit": "percentage",\n')
        json_file.write('                     "aggregatedImpactValue": ' + str(sh.cell_value(rx,19))+ ',\n')
        json_file.write('                     "aggregatedImpactMaxRangeValue": ' + str(sh.cell_value(rx,20))+ '\n')
        json_file.write('                  }')

        # decrease the number of impacted KPIs dealt with
        if number_of_indicators > 1:
            json_file.write(',\n')
            number_of_indicators -= 1
        else:
            json_file.write('\n')
        
    json_file.write('               ],\n')

    
    ### 4: add the DATS main impacts
    json_file.write('               "mainImpactInformation": [\n')
    # first count the number of rows with a 1 in column J, i.e. the main impacts
    number_of_indicators = 0
    for rx in range(sh.nrows):
        if sh.cell_value(rx,9) == 1:
            number_of_indicators += 1
    logger.info(f"number of calculated main impacts: {number_of_indicators}")
        
    # second run through the impacted KPIs and add a JSON object for each of them
    for rx in range(sh.nrows):
        if sh.cell_value(rx,9) == 1:
            #logger.info(sh.cell_value(rx,2))
            json_file.write('                  {\n')
            json_file.write('                     "mainImpactName": "' + sh.cell_value(rx,2)+ '",\n')
            json_file.write('                     "mainImpactUnit": "' + sh.cell_value(rx,3)+ '",\n')
            value = str(sh.cell_value(rx,4)) if sh.cell_value(rx,4) != "" else "null"
            json_file.write('                     "absoluteDifference": ' + value + ',\n')
            value = str(sh.cell_value(rx,5)) if sh.cell_value(rx,5) != "" else "null"
            json_file.write('                     "percentageDifference": ' + value + ',\n')   
            value = "true" if sh.cell_value(rx,7) == 1 else "false"
            json_file.write('                     "higherIsBetterMeaning": "' + str(value) + '",\n')
            json_file.write('                     "impactLevel": ' + str(sh.cell_value(rx,16)) + ',\n')
            json_file.write('                     "mainImpactTitle": "' + sh.cell_value(rx,12)+ '",\n')
            json_file.write('                     "mainImpactSubtitle": "' + sh.cell_value(rx,13)+ '"\n')
            json_file.write('                  }')
            
            # decrease the number of impacted KPIs dealt with
            if number_of_indicators > 1:
                json_file.write(',\n')
                number_of_indicators -= 1
            else:
                json_file.write('\n')
            
    json_file.write('               ],\n')
 
    ### 5: cost and revenue impacts => DATS costs and those with a 1 in the K column
    json_file.write('               "costRevenueImpactInformation": [\n')
    # first count the number of rows with a 1 in column K, i.e. the cost revenue impacts
    number_of_indicators = 0
    for rx in range(sh.nrows):
        if sh.cell_value(rx,10) == 1:
            number_of_indicators += 1
    logger.info(f"number of calculated cost revenue impacts: {number_of_indicators}")

    # second run through the impacted KPIs and add a JSON object for each of them
    for rx in range(sh.nrows):
        if sh.cell_value(rx,10) == 1:
            #logger.info(sh.cell_value(rx,2))
            json_file.write('                  {\n')
            json_file.write('                     "costRevenueImpactCategory": "' + sh.cell_value(rx,1)+ '",\n')
            json_file.write('                     "costRevenueImpactName": "' + sh.cell_value(rx,2)+ '",\n')
            json_file.write('                     "costRevenueImpactUnit": "' + sh.cell_value(rx,3)+ '",\n')
            value = str(sh.cell_value(rx,4)) if sh.cell_value(rx,4) != "" else "null"
            json_file.write('                     "absoluteDifference": ' + value + ',\n')
            value = str(sh.cell_value(rx,5)) if sh.cell_value(rx,5) != "" else "null"
            json_file.write('                     "percentageDifference": ' + value + ',\n')   
            value = "true" if sh.cell_value(rx,7) == 1 else "false"
            json_file.write('                     "higherIsBetterMeaning": "' + str(value) + '",\n')   
            json_file.write('                     "impactLevel": ' + str(sh.cell_value(rx,16)) + ',\n')
            json_file.write('                     "costRevenueImpactShortDescription": "' + sh.cell_value(rx,14)+ '"\n')
            json_file.write('                  }')
            
            # decrease the number of impacted KPIs dealt with
            if number_of_indicators > 1:
                json_file.write(',\n')
                number_of_indicators -= 1
            else:
                json_file.write('\n')
            
    json_file.write('               ]\n')

    ### 6: three year averages
    #sh = wb.sheet_by_index(12)

    # first count the number of rows with a dimension in column A
    #number_of_indicators = 0
    #for rx in range(sh.nrows):
    #    if sh.cell_value(rx,0) != "" and sh.cell_value(rx,0) != "Dimension":
    #        number_of_indicators += 1
    #logger.info(f"number of three year averages: {number_of_indicators}")

    # second run through the averages
    #json_file.write('               "threeYearAverages": [\n')
    #for rx in range(sh.nrows):
    #    if sh.cell_value(rx,0) != "" and sh.cell_value(rx,0) != "Dimension":
    #        json_file.write('                  {\n')
    #        json_file.write('                     "threeYearAverageCategory": "' + sh.cell_value(rx,0)+ '",\n')
    #        json_file.write('                     "threeYearAverageImpactName": "' + sh.cell_value(rx,1)+ '",\n')
    #        if 2 <= rx <= 7:
    #            json_file.write('                     "threeYearAverageImpactUnit": "€/ha",\n')
    #            json_file.write('                     "threeYearAverageImpactValue": ' + str(sh.cell_value(rx,5))+ ',\n')
    #            json_file.write('                     "threeYearAverageImpactStandardDeviation": ' + str(sh.cell_value(rx,6))+ '\n')
    #        else:
    #            json_file.write('                     "threeYearAverageImpactUnit": "%",\n')
    #            json_file.write('                     "threeYearAverageImpactValue": ' + str(100*sh.cell_value(rx,5))+ ',\n')
    #            json_file.write('                     "threeYearAverageImpactStandardDeviation": ' + str(100*sh.cell_value(rx,6))+ '\n')
    #        json_file.write('                  }')

            # decrease the number of impacted KPIs dealt with
    #        if number_of_indicators > 1:
    #            json_file.write(',\n')
    #            number_of_indicators -= 1
    #        else:
    #            json_file.write('\n')

    #json_file.write('               ]\n')

    # close the indicators
    json_file.write('}')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Hello!")

    try:
        filename = input("Which testcase Excel file do you want to parse and convert to json?:")
    except:
        logger.info(f'Filename could not be read')
    file = "/Users/jack.verhoosel/Dropbox/Projecten/QuantiFarm/Testcase data in Excel/"+filename+".xlsx"
    if os.path.exists(file):
        convert_excel_to_json(file)
    else: 
        logger.info("File does not exist!")
        sys.exit()


    
    
