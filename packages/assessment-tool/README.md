# Introduction

<h3 align="center">Quantifarm Assessment Tool</h3>

<p align="center">
  This common component aims to act as a single point of access,
  capable to provide Revenue Benefits from the use of DATs.
</p>

<p align="center">
  The following Technolgies / APIs / Libraries are utilised:
  <br>
  Python 3 : <a href="https://docs.python.org/3/"><strong>Explore Python 3.6+ docs »</strong></a>
  <br>
  FastAPI : <a href="https://fastapi.tiangolo.com/"><strong>FastAPI »</strong></a>
</p>


## Table of contents

- [Quick start](#quick-start)

## Quick start

### Python and Libraries

- Install [Python 3.6+](https://www.python.org/downloads/)

### Procedure Overview
<p>
We begin by extracting user input from the front end for each Test Case as a JSON object.

```console
{
   "testcaseNumber": 2,
   "testcaseLeader": "Agromais",
   "cultivationType": "Arable",
   "crop":"Maiz",
   "datsInformation": [
      {
         "datsName": "Farm manager",
         "datsInitialInvestmentCosts": 1500,
         "datsAnnualFees": 0,
         "datsMaintenanceCosts": 0,
         "datsExpectedLifespan": 10,
         "datsInstallationTime": 2,
         "datsTrainingTime": 1,
         "datsTrainers": 1,
         "datsTrainingCosts": 0
      }
   ],
...
```

We then manually create a JSON that has a direct mapping between the exported JSON from the Front End and the cells inside the Polimi Formula Excel.
So we end up with a mapping similar to the following : 

```console
{
 "G6":"parcelinformation_cultivationtype",
 "G7":"parcelinformation_producttype"
}
```

Using VBScript, ("extract_formulas.vbs") we extract the formulas from the Polimi Excel file. 
Example of the export is below:

```console
$E$19: ='Parcel 1 with DATSs'!K214 | sust kpis dats_Economic EFFICIENCY _Number of wrong orders | E19
$E$24: ='Parcel 1 with DATSs'!K216 | sust kpis dats_PRODUCT QUALITY  _Protein % DRY MATTER | E24
$E$25: ='Parcel 1 with DATSs'!K217 | sust kpis dats_PRODUCT QUALITY  _Humidity | E25
$E$26: ='Parcel 1 with DATSs'!K218 | sust kpis dats_PRODUCT QUALITY  _Test Weight  | E26
```

When all the previous steps have been completed we :

1. We load in memory the JSON property mapping we created earlier.
2. With the help of tools provided in this repository ("convert_formulas_to_json.py"), the exported Excel formulas are converted into JSON format.Simultaneously, we replace cell references with actual values from our in-memory object and incorporate custom Pythonic formulas to replace any dynamic Excel formulas.
3. At the end of the conversion process, we successfully transform Excel formulas into Pythonic equivalents that can be efficiently evaluated to produce a result.
4. Lastly we execute the "main.py" which will evaluate all the Pythonic formulas.
5. The final evaluated result is then exported as a JSON object.

Example of the output: 

```console
{
    "sust_kpis_dats": {
        "economic_productivity_": {
            "yield": "1.0",
            "labour_productivity_arable_and_horticulture": "0.04",
            "labour_productivity_dairy_livestock": "0.04",
            "labour_productivity__meat_livestock": "0.04",
            "labour_productivity__aquaculture": "0.04",
            "labour_productivity__apiculture": "0.04",
            "labour_productivity_silos": "0.04",
            "milk_productivity": "1.0",
            "meat_productivity": "1.0",
            "bees_productivity": "1.0",
            "oyster_productivity": "1.0"
...
```
</p>


