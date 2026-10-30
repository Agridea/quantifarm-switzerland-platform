import json
import random

# import dats_generator_analysis
sectors = ['Agrotourism', 'All agricultural sectors', 'Animal production in general', 'Apiculture', 'Aquaculture',
             'Arable', 'Arable farming', 'Arboriculture', 'Communication/dissemination', 'Dairy',
             'Dairy (cattle, sheep, goats)', 'Farm-based added-value processes', 'Fishing/Aquaculture', 'Flowers',
             'Forestry', 'Fruit', 'Fruits and vines', 'Herbs', 'Insects/Apiculture', 'Meat',
             'Meat (cattle, pigs, sheep, goats, poultry, rabbits, snails)',
             'Meat (cattle, pigs, sheep, goats, poultry, rabbits, snails) (cattle, sheep, goats)',
             'Plant production in general', 'Post-harvest', 'Poultry egg production', 'Vegetables', 'all', 'almond',
             'arable', 'cabbage', 'cattle', 'cow', 'dairy cow', 'fennel', 'fruit', 'goat', 'grape', 'lettuce', 'olive',
             'onion', 'pig', 'piglet', 'potato', 'poultry', 'row crop', 'sheep', 'small ruminant', 'strawberry',
             'swine', 'vegetable', 'walnut']
functionalities = ['Activity sensors', 'Agri-environmental Monitoring', 'Automated Feeding ', 'Automated monitoring',
                   'Automatic Feeding', 'Automatic Littering System', 'Automatic Milking ', 'Autosteering',
                   'Autosteering-FMIS ', 'Autosteering-VRA seed and fertilizer ', 'CAP management', 'Calving detectors',
                   'Cleaning robot', 'Compliance with legislation and standards', 'Digital  lossom map',
                   'Digital pest control', 'Digital vigour map', 'Digitally controlled dimmable led lights',
                   'Drone Flights and Elevation Maps', 'FMIS ', 'FMIS/ Financial Modelling', 'Feeding Robot',
                   'Feeding System', 'Feeding robot', 'Fever Detection', 'Finance and budgeting', 'GPS',
                   'GPS Guidance System', 'GPS Integration', 'Harvest prediction', 'Heat Checking', 'Heat detection',
                   'Heat detector', 'Improving animal care', 'Irrigation-DSS', 'Lighting ',
                   'Livestock Green House Gas (GHG) measurement and management', 'Livestock management',
                   'Livestock stock management', 'Logistics', 'Management Zones & VRA Maps', 'Markets and sales',
                   'Milking Machine', 'Milking Robot', 'Milking robot', 'Monitoring', 'Monitoring-FMIS',
                   'Monitoring-FMIS ', 'Multipurpose-DSS/FMIS', 'Multipurpose-FMIS',
                   'Nutrition/Fertilisation management', 'Operational management focus', 'Plant protection management',
                   'Post-harvest management', 'Precision Irrigation', 'Precision fertigation', 'Precision irrigation',
                   'Robotic Milking', 'Rotary Parlor', 'Rotary milking', 'Sensors and Weather Stations',
                   'Sensors for quality assessment', 'Silo management', 'Sound Monitoring', 'Strategic planning',
                   'Sustainable food production and healthy diets', 'VRA', 'Virtual fencing', 'Water management',
                   'Water sensors ', 'Weeding and thinning', 'Work safety', 'automated rotary milking',
                   'automatic feeding', 'automatic liquid feeding', 'connection', 'farrowing feeding', 'fertilization',
                   'health monitoring', 'heat and movement patterns  etection and warning', 'heat detection',
                   'irrigation ', 'lighting arrangement', 'monitoring and warning', 'multipurpose',
                   'pesticide and fertilizer application', 'pesticide application', 'pig sorting',
                   'planting and fertilization', 'pruning', 'seed and fertilizer application', 'spraying',
                   'to keep animals moving', 'virtual fencing',
                   'water disinfection system for recirculation of irrigation water', 'weeding']
digital_forms = ['Mobile app', 'Paper', 'Spreadsheet', 'Stand-alone software', 'Web app', 'Webapp']
benefits = ['Better interaction between farmer and advisor', 'Biodiversity preservation',
            'Compliance records management', 'Control of animal health problems ', 'Effective operational management',
            'Efficient strategy planning', 'Enhanced adaptation & resilience to climate change',
            'Environmental protection', 'Financial assessment / Reporting', 'Improvement of yield quality',
            'Increase of productivity', 'Increase of profit/farm income',
            'Labour saving / Limit stress / Increase farmer’s leisure time', 'Limit human exposure to chemicals',
            'Limit number or severity of human injuries',
            'Limit number or severity of property damage and related accidents', 'Minimization of input costs',
            'Optimization of resources use', 'Task scheduling / Time management']
countries = ['Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kazakhstan', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova Republic of', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russian Federation', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom']
languages = ['Armenian', 'Basque', 'Bulgarian', 'Catalan', 'Croatian', 'Czech', 'Danish', 'Dutch', 'English', 'Estonian', 'Finnish', 'French', 'German', 'Greek', 'Hungarian', 'Italian', 'Japanese', 'Latvian', 'Lithuanian', 'Many', 'Norwegian', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Serbian', 'Slovak', 'Slovenian', 'Spanish', 'Swedish', 'Turkish', 'Ukranian']




def generate_random_dats(n, sectors, languages, countries, digital_forms, benefits, functionalities):
    dats = []
    for ID in range(n):

        dats.append(generate_random_dat(ID, sectors, languages, countries, digital_forms, benefits, functionalities))
    return dats

def generate_random_dat(ID, sectors, languages, countries, digital_forms, benefits, functionalities):
    sector = random.sample(sectors, random.randint(1, 2))
    language = random.sample(languages, random.randint(1, 3)) #if random.randint(1, 2) > 1 else ["Many"]
    country = random.sample(countries, random.randint(1, 3))
    digital_form = random.sample(digital_forms, 1)
    benefit = random.sample(benefits, random.randint(1, 2))
    functionality = random.sample(functionalities, random.randint(1, 2))
    dat = {
        "countries": country,
        "languages":
            language
        ,
        "category": [],
        "target": [],
        "sector":
            sector
        ,
        "delivery":
            digital_form
        ,
        "source": [

        ],
        "benefits":
            benefit
        ,
        "challenges":
            functionality
        ,
        "imagePath": [],
        "documentPath": [],
        "_id": "generated_dat" + str(ID),
        "name": "generated_dat" + str(ID),
        "website": "null",
        "cost": "null",
        "launchYear": "2025",
        "updateYear": "2025",
        "usersNo": "null",
        "downloads": "null",
        "providerName": "",
        "providerEmail": "",
        "providerWebsite": "",
        "applied": "",
        "languageOther": "null",
        "title": ".",
        "titleOther": "null",
        "desc": ".",
        "descOther": "null",
        "keywords": "",
        "keywordsOther": "null",
        "conn": "null",
        "access": "null",
        "know": "null",
        "train": "null",
        "videos": "null",
        "creator": "null",
        "__v": 0
    }
    print(dat)
    return dat






def generate_all_dats(sectors, languages, countries, digital_forms, benefits, functionalities):
    generated_dats = []
    ID = 0
    for sector in sectors:
        for language in languages:
            for country in countries:
                for digital_form in digital_forms:
                    for benefit in benefits:
                        for functionality in functionalities:
                            generated_dats.append(
                                generate_new_dat(ID, sector, language, country, digital_form, benefit, functionality))
                            ID += 1


def generate_new_dat(ID, sector, language, country, digital_form, benefit, functionality):
    dat = {
        "countries": [
            country
        ],
        "languages": [
            language
        ],
        "category": [],
        "target": [],
        "sector": [
            sector
        ],
        "delivery": [
            digital_form
        ],
        "source": [

        ],
        "benefits": [
            benefit
        ],
        "challenges": [
            functionality
        ],
        "imagePath": [],
        "documentPath": [],
        "_id": "generated_dat" + ID,
        "name": "generated_dat" + ID,
        "website": "null",
        "cost": "null",
        "launchYear": "2025",
        "updateYear": "2025",
        "usersNo": "null",
        "downloads": "null",
        "providerName": "",
        "providerEmail": "",
        "providerWebsite": "",
        "applied": "",
        "languageOther": "null",
        "title": ".",
        "titleOther": "null",
        "desc": ".",
        "descOther": "null",
        "keywords": "",
        "keywordsOther": "null",
        "conn": "null",
        "access": "null",
        "know": "null",
        "train": "null",
        "videos": "null",
        "creator": "null",
        "__v": 0
    }
    return dat


def store_dats(dats):
    with open("generated_dats.json", "w") as f:
        json.dump(dats, f, indent=4)


dats = generate_random_dats(100, sectors, languages, countries, digital_forms, benefits, functionalities)
store_dats(dats)
