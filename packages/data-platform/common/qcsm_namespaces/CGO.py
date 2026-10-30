from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class CGO(DefinedNamespace):
    """
    Generated namespace for Common Greenhouse Ontology

    Generated from: https://ontology.tno.nl/ddings/Greenhouse_ontology_v1.3.ttl
    Date: 2023-03-07 14:59:57.990299
    """

    _NS = Namespace("https://www.tno.nl/agrifood/ontology/common-greenhouse-ontology#")

    AbioticStressTrait: URIRef  # All traits related to stress caused by non-living stressors. Abiotic stress is defined as the negative impact of non-living factors on the crop/plants. Most common abiotic stressors are drought, waterlogging, high/low temperatures, mineral toxicities/deficiencies, hail, and wind.
    AbsoluteHumidity: URIRef  # The actual amount of water vapor in a given volume of air is the absolute humidity; it is expressed as weight per volume. In Mollier diagrams weight per weight of air is used (kg/kg or gr/kg). Absolute humidity is rarely measured in greenhouses, however, and relative humidity is used instead.
    AgronomicalTrait: URIRef  # All main traits contributing to yield and related to the agronomic performance of crop/plants.
    Air: URIRef  #
    AirBlower: URIRef  # A fan that creates a horizontal airflow above the canopy
    AirCirculationSystem: URIRef  # This class represents a system that is responsible for the airflow inside the greenhouse.
    AirDuctSystem: URIRef  # Located either below or above the canopy
    AirHeater: URIRef  # Device which heats the air of the greenhouse by burning certain type of fuel or using warm water (the latter is more common nowadays). They are used in clusters and are autonomous
    AirToAirHeatExchanger: URIRef  #
    AirToWaterHeatExchanger: URIRef  # Air-to-water heat exchangers use the same principle of temperature differential to provide heating or cooling as air-to-air heat exchangers, however, they alter the temperature of air by forcing it across water coils.
    Aluminium: URIRef  # This is the level aluminium in a sample of water measured in µmol/l
    AluminiumStructure: URIRef  # The used aluminium profiles hold the glass in place, discharge water and provide overall strength. the aluminium greenhouse gutter does not only collect the rain and snow, but it fulfills a crucial constructive role. This ingenuous system cares for the strength in the gutter-direction of the greenhouse. It significantly reduces the amount of material required to construct the greenhouse. Next to this, the gutter also collects condensation water from the glass on the inside of the greenhouse. If required by regulation, this can be discharged separately from the rainwater. This condensation water function of the gutter prevents water dripping on the crops, which can cause damage in the form of burn spots or physical damage.
    Ammonium: URIRef  # This is the level of ammonium in a sample of water measured in mmol/l or mg/l
    AntiInsectNet: URIRef  # This class represents anti-insect nets that are used in greenhouses. Nets are used mainly in the vents
    Basin: URIRef  #
    Bench: URIRef  #
    Bicarbonate: URIRef  # This is the level of bicarbonate in a sample of water measured in mmol/l or mg/l
    BiochemicalTrait: URIRef  # All traits related to chemical components of a plat entity.
    Biomass: URIRef  # Includes solid, liquid and gas biomass, as well as organic waste gas
    BioticStressTrait: URIRef  # All traits related to stress caused by living stressors. Biotic stress is defined as the negative impact on the crop/plants of living organisms such as bacteria, viruses, fungi, parasites, nematodes, weeds, invertebrate and vertebrate pests.
    BlackoutCurtain: URIRef  #
    Block: URIRef  # A block contains only a single crop (this is a requirement) A block is part of a compartment in the greenhouse in which the plants are treated equally wrt nutrition, climate etc. Each block has a unique identifier in the greenhouse or compartment in the greenhouse This class represents blocks that are part of a greenhouse and contain a set of plants vanuit de gebruiker is het logisch om plaatsbepaling te doen per afgesloten deel van een kassencomplex. Dat kan dus een gehele kas zijn, maar ook een afdeling binnen de kas. Plaatsbepaling dient dus plaats te vinden in ieder “door middel van vaste wanden afgescheiden deel van de kas”. Dit deel wordt veelal aangeduid als afdeling of met de Engelse term “block”.
    Blueprint: URIRef  # This class represents blueprints of a building
    Boiler: URIRef  # Provides heat similar to a home boiler Sometimes also named "Burner"
    BoilerCapacity: URIRef  #
    BoilerPart: URIRef  #
    BoilerSupplySensor: URIRef  #
    BoilerWaterTemperatureSensor: URIRef  #
    Boron: URIRef  # Boron functions in the plant are not well understood. Boron seems to be important for normal meristem development in young parts such as root tips. This is the level of boron in a sample of water measured in mmol/l of mg/l
    Branch: URIRef  #
    BufferTank: URIRef  # Tank where we store heated water
    BufferWaterTemperatureSensor: URIRef  # measures the temperature at 1 of the 11 points in buffer. The temperature in the buffer differs with cool water being lower and hot water higher
    Builder: URIRef  # This class represents builders that build greenhuses and possibly support growers in their crop management activities
    Burner: URIRef  #
    CHP: URIRef  # Combined heat and power (CHP), also known as cogeneration. The concurrent production of electricity or mechanical power and useful thermal energy (heating and/or cooling) from a single source of energy. Warmte-krachtkoppeling (WKK) of cogeneratie staat voor het gelijktijdig opwekken van warmte en kracht (elektriciteit).
    CHPSystemPart: URIRef  # Unit which produces heat and electrical power
    CO2: URIRef  # For the majority of greenhouse crops, net photosynthesis increases as CO2 levels increase from 340–1,000 ppm (parts per million). Most crops show that for any given level of photosynthetically active radiation (PAR), increasing the CO2 level to 1,000 ppm will increase the photosynthesis by about 50% over ambient CO2 levels. For some crops the economics may not warrant supplementing to 1,000 ppm CO2 at low light levels. For others such as tulips, and Easter lilies, no response has been observed. Possible forms of CO2 are flue gas and liquified CO2 unit: ppm (parts per million)
    CO2EnrichmentSystem: URIRef  # The CO2 enrichment system is consist of two main components. The CO2 source, how we get CO2 and the component related to how the CO2 is distributed to the greenhouse air. For the first related to CO2 source, we have mainly two sources, either pure CO2 stored in special tanks or CO2 which is obtained from exhaust gas (we use also the term flue gas) which is emitted as a result of the combustion of fuels such as natural gas.     In general, CO2 enrichment decreases the oxygen inhibition of photosynthesis and increases the net photosynthesis in plants. This is the basis for increased growth rates caused by CO2 at low as well as at high light levels. Elevated CO2 concentrations also increase the optimal temperature for growth. Pot plants, cut flowers, vegetables and forest plants show very positive effects from CO2 enrichment by increased dry weight, plant height, number of leaves and lateral branching. Plant quality expressed by growth habit and number of flowers is often enhanced by CO2 enrichment. The rooting of cuttings is often stimulated by high CO2 levels.
    Cabriokas: URIRef  # Dek kan geheel worden geopend Roof can be fully opened
    Calcium: URIRef  # Calcium is required for calcium pectate for cell wall development. In addition, Ca is used as a cofactor of certain enzymatic reactions. This is the level of calcium in a sample of water measured in mmol/l or mg/l
    Canopy: URIRef  #
    Capacity: URIRef  #
    CapacityControlSystem: URIRef  # As its name might suggest, the capacity control system regulates the power and energy consumption, although it can also manage dehumidification or decrease compressor cycling. The on/off cycling of the compressor is the simplest form of capacity control.
    Carbon: URIRef  # Carbon is 'fixed' from CO2 from the atmosphere by photosynthesizing plants.
    CentralHeatingSystem: URIRef  #
    Chloride: URIRef  # Chloride (Cl) may also be present in many water sources. High levels of chloride are detrimental to crop growth, only low levels of chloride are acceptable. The maximum acceptable Cl level in the root zone is 0.2-0.5 mmol/l higher than the maximum acceptable level for Na. This is the level of chloride in a sample of water measured in mmol/l or mg/l
    CirculationPump: URIRef  # The pump used to put water inside the mixing tank
    CirculationSystemPart: URIRef  #
    CleanWaterTank: URIRef  # Tank that contains the clean water before it is mixed with the fertilzer
    Climate: URIRef  # The climate is a long term average of the weather outside of the greenhouse.
    ColdSource: URIRef  # The cold source (from which heat is recovered) The external medium from which heat is drawn is called a cold source. In the heat pump the refrigerant absorbs heat from the cold source by means of the evaporator.  The main cold sources are:      AIR: outside the space to be heated, typically air from the external environment;     WATER: from the water table, rivers, and lakes, when in proximity to the spaces to be heated and at a limited depth below the surface. Other reservoirs may consist of water which has accumulated in reservoirs and is subsequently heated by solar radiation.      GROUND, into which specific pipes relating to the evaporator are sunk to varying depths (these pipes constitute a geothermal system).
    Color: URIRef  #
    Column: URIRef  #
    Compartment: URIRef  # A compartment is a part of the greenhouse Each compartment has a unique identifier in the greenhouse This class represents compartments that is an area that is controlled in the same way regarding the climate. A compartment can be separated with walls or screens but not neccessarily.
    CompartmentPart: URIRef  #
    Compressor: URIRef  #
    Condenser: URIRef  # This device can extract heat from the refrigerant. Fans placed above the condenser unit draw air over the condenser coils. The temperature of condensation should range from around -12°C to -1°C; vapour will be cooled until it becomes a liquid refrigerant again, whereby it will retain some heat.
    ConstructionPart: URIRef  # Model-technical term This class represents the different parts of a construction of a building
    ControlSystem: URIRef  # The control system controls different functions and processes inside the greenhouse. In Dutch it is usually known as the climate computer, in English it is called control system.
    CoolingSystem: URIRef  # Adiabatic cooling like padd wall and fogging and active cooling with condensation of moisture on a cold surface
    CoolingSystemPart: URIRef  # This class represents the parts found in cooling systems
    Copper: URIRef  # Copper is a component of several enzymes in plants and is a part of a protein in the electron transport system in photosynthesis. This is the level of copper in a sample of water measured in mmol/l of mg/l
    Cover: URIRef  # This class represents covers of greenhouses
    CoverMaterial: URIRef  #
    Crop: URIRef  # A group of plants that have the same type and breed Een individual van gewas is een plantensoort. Gewas is een metaklasse die enkel klasses bevat, deze klasses kunnen wel individuals bevatten. Zoals we hier crop gebruiken is dus niet helemaal accuraat maar hebben we omwille van begrijpelijkheid zo gehouden. More characteristics of a crop can be defined using the guideline for creating a crop ontology published here: http://www.cropontology.org This class represents crops that are produced in a greenhouse operated by a grower
    CultivationSystem: URIRef  #
    Curtain: URIRef  #
    DehumidificationSystem: URIRef  # Example: DryGair dehumidifier
    DesiccantSystem: URIRef  # Is a combined dehumidification and cooling system
    DesiccantSystemPart: URIRef  #
    DesiccantWheel: URIRef  # Has dessicant material to absorb humidity by chemical or physical processes. While we absorb humidity the air also warms,
    DewPointTemperature: URIRef  # Dewpoint temperature indicates the temperature at which water will begin to condense out of moist air. Condensation on plants occurs when leaf surface temperature is below dew point. This is when there is too much moisture in the air to remain in the vapor state. The moisture will fall out and condense as free-moisture on surfaces that are at or below the dewpoint temperature. In other words, condensation will occur on the coldest surfaces first. The coldest surfaces will be the piping, door knobs, roof and eventually the plants. For example, when the greenhouse is 85% RH and 60°F, condensation occurs when leaf temperature is lower than 55°F. At 95 % RH and 60°F, condensation occurs when leaf temperature is only one degree lower than air temperature.
    Diesel: URIRef  #
    DiffuseGlass: URIRef  # Diffuse glass is on the rise and installed in many new greenhouse projects. Diffuse glass has an etching or a structure which changes the properties of the surface of the glass, which can be benefitial for the crops within the greenhouse.
    Direction: URIRef  #
    Disease: URIRef  # This class represents different kind of diseases that plants can get
    DisinfectionSystem: URIRef  # Desinfection of crop or of return drain water
    DisinfectionSystemPart: URIRef  #
    DisinfectionUnit: URIRef  #
    DisinfectionWaterTank: URIRef  #
    DissipatedHeatingPower: URIRef  # This term might be changed
    DistributorReturn: URIRef  #
    DistributorSupply: URIRef  #
    DoubleScreeningSystem: URIRef  # The improved characteristics of the screens make for an accurate climate regulation. A double screening system has become more and more applied, as it has proven to provide growers with the flexibility they need.  Double screens are installed above each other and are always fitted with different type of climate screens. The layers can be opened and closed to complement the functionality of both.
    DrainCollectionTray: URIRef  #
    DrainSolenoidValve: URIRef  # When the system stops this valve stops the water from running back into the system
    ECCheckSensor: URIRef  #
    ECDoseSensor: URIRef  #
    ECMixingValveSensor: URIRef  #
    ECSensor: URIRef  # The fertigation unit has at least 1, in the Netherlands usually 2, measures the electrical conductivity in the water
    Efficiency: URIRef  #
    ElectricHeatPump: URIRef  # Device for generating cooling and lift tempeature of harvested heat for reuse. If external air is used, a defrosting system is needed at temperatures of around 0ºC, which entails additional energy consumption. During this phase the heat pump uses the heat of the hot source in order to defrost the battery and so heating ceases for some minutes.
    ElectricalConductivity: URIRef  # This is the electrical conductivity of a sample of water measured in milliSiemens per centimeter (mS/cm)
    ElectricalGridEnergy: URIRef  #
    EmbeddedHeatingPipe: URIRef  # The floor heating pipe is a heating pipe that is embedded in the floor of the greenhouse such that we warm up the floor. Usually this floor is made of concrete. The temperature of this pipe isaround 30 degrees to not burn the roots of the plants
    EnergyCurtain: URIRef  #
    EnergyRecoveryWheel: URIRef  # Hot air goes into the recovery wheel and is transformed into heat
    EnergyScreen: URIRef  # This class represents energy screens in greenhouses
    EvaporativeCooler: URIRef  # One used towards the greenhouse, one used from the greenhouse to the outside air, to cool the air going into the greenhouse
    EvaporativePad: URIRef  # Saturated with water, from the surface the water evaporates. With fans you suck the air from the greenhouse such that the outside air is forced through the pad. Due to the evaporation the air is cooled.
    Evaporator: URIRef  # The sole purpose of the evaporator is to remove the unwanted heat from the product through liquid refrigerants. The liquid refrigerant must be at a low-pressure. This low-pressure can be determined by two factors – one is the heat being absorbed from the product to the liquid refrigerant and the other is the removal of low-pressure vapour by the compressor.
    ExhaustFan: URIRef  # Fans are used to suck air out of the greenhouse such that the evaporative cooling pad can function. They are installed to the opposite side of the Pad
    ExpansionValve: URIRef  #
    FertigationDirectInjectionSystem: URIRef  # A fertigation system without a mixing tank. The concentrated fertilizer is injected in the same pipe . The mixing is taking place inside the pipe. There might be differences in the mixture because there is no mixing tank
    FertigationMixingTankSystem: URIRef  # The system or device which at the same time prepares the fertilization recipe and provides the irrigation water to the plants, has a mixing tank.
    FertigationPump: URIRef  #
    FertigationRecipe: URIRef  # Fertigation recipe is the same as a nutrition recipe
    FertigationSystem: URIRef  # 'Fertigation' is the process of supplying dissolved fertiliser to crops through an irrigation system.
    FertigationSystemPart: URIRef  #
    FertigationSystemSensor: URIRef  #
    FertigationTank: URIRef  #
    FertigationUnit: URIRef  # The system or device which at the same time prepares the fertilization recipe and provides the irrigation water to the plants, has a mixing tank. Is the heart of the Fertigation System
    FertigationUnitFertilizerValve: URIRef  # Each valve is connected with a tank with concentrated fertilizer solution, the valve is used to inject the right amount of concentrated fertilizer to the mixing tank. Usually are solenoid venturi valves
    FertigationUnitMainPump: URIRef  # Mixes the fertigation solution and provides it to the greenhouse or to the fertilizer daily supply tank at the same time.
    FertigationUnitSupplyPump: URIRef  # The pump which supplies clean water to the fertigation unit from the clean water tank
    FertilityTrait: URIRef  #
    FertilizationRecipe: URIRef  # The combination of fertilizers, both macro and micro nutrients, and the concentration in the water. The recipe describes this.
    Fertilizer: URIRef  # Important considerations are ratio of ammonium to nitrate-N, trace element charge, content of calcium and magnesium, and potential acidity or basicity.
    FertilizerConcentratedSolution: URIRef  # Fertilizer solution that is inside the Fertilizer Tank, is made with the fertilization recipe
    FertilizerDailySupplyTank: URIRef  # This tank can be used to temporarily store the fertigation mix.
    FertilizerTank: URIRef  # Tank with fertilizer that is connected to the unit, has its own fertilizer recipe
    Floor: URIRef  # This class represents floors of greenhouses
    Flower: URIRef  # This class represents flowers
    FlowerConstruction: URIRef  # The preception of the flower construction of a plant as a number between 1 and 10 from bad to good
    FlowerPart: URIRef  # This class represents the different parts of a flower
    FoggingSystem: URIRef  # Adiabatic cooling in the greenhouse by spraying tiny water droplets above the canopy
    FoggingSystemPart: URIRef  # This class represents the parts found in fogging systems
    Foundation: URIRef  #
    FoundationSlope: URIRef  # Because greenhouses deal with rainfall, snowfall and also often have irrigation gutters installed, Dutch greenhouses are constructed on an angle. The slope is applied lengthwise, in the gutter-direction of the greenhouse. To ensure the optimal water discharge, the foundation has to be created accordingly. The slope that is most applied is 2.25 mm per meter gutter-length.  Horizontally, the foundation has to be perfectly levelled out. In greenhouses with larger lengths, the slope for water discharge has to be created on two sides.  This implies that the highest point of the greenhouse is in the centre of structure.
    Frame: URIRef  # This class represents frames of greenhouses
    FrontWall: URIRef  #
    Fruit: URIRef  #
    Fuel: URIRef  #
    GPSGrid: URIRef  # The grid based on GPS coordinates
    Gantry: URIRef  #
    Gas: URIRef  #
    GasAbsorptionHeatPump: URIRef  # If external air is used, a defrosting system is needed, which is automatically activated at temperatures of around 0ºC. Heat output supplied during the defrosting phase (which lasts a few minutes) falls, but does not cease completely.
    Gasoline: URIRef  #
    GeothermalEnergy: URIRef  #
    Glass: URIRef  # In vegetable production, a rule of thumb states that 1% more light equals 1% more potential production. The greenhouse covering therefore should allow the sunlight to enter the greenhouse as much as possible for a maximum potential photosynthesis. Just like every constructive element in the greenhouse, glass is evaluated carefully for its light translucency and its return on investment, if not more.
    Greenhouse: URIRef  # This class represents greenhouses in which crop is being grown by a grower
    GreenhouseAir: URIRef  #
    GreenhouseClimate: URIRef  # The greenhouse climate is a direct, day-to-day state of temperature, air pressure, moisture, and more factors inside the greenhouse. It is called greenhouse climate, but regarding the earlier use of weather and climate, greenhouse weather is probably a more correct term.
    GreenhouseConstruction: URIRef  # An efficient workflow defines the Dutch greenhouse construction industry. This is the case for the process of engineering, procurement and especially the construction of the greenhouse. Greenhouses are designed to be assembled easily and quickly. A greenhouse however, is of great value and the consequences of error and success are considerably large.  The greenhouse construction is therefore handled under strict supervision by a professional supervisor. Supervisors are experienced Dutch greenhouse builders who accompany local subcontractors on each step of the assembling process. With clear instruction manuals and videos, the right equipment and a number of local construction companies, a greenhouse is relatively easily and quickly constructed.
    GreenhouseLocalGrid: URIRef  # The x-y grid of the greenhouse based on the hortispot
    GreenhouseOwner: URIRef  #
    GreenhousePart: URIRef  # Model-technical term This class represents the different parts of a greenhouse
    GreenhouseSensor: URIRef  # Technical sensor
    GreenhouseWeatherStation: URIRef  #
    Grid: URIRef  #
    Ground: URIRef  #
    GroundCoupledHeatPump: URIRef  #
    GroundCoverNet: URIRef  # This class represents nets that cover ground that are used in greenhouses
    GroundSourceHeatPump: URIRef  # The GSHPs comprise a wide variety of systems that may use ground-water, ground, or surface water as heat sources or sinks. These systems have been basically grouped into three categories by ASHRAE [13]: (1) ground-water heat pump (GWHP) systems, (2) surface water heat pump (SWHP) systems, and (3) ground-coupled heat pump (GCHP) systems. The schematics of these different systems are shown in Figure 3. Many parallel terms exist: geothermal heat pump (GHP), earth energy system (EES), and ground-source system (GSS).
    GroundWaterHeatPump: URIRef  #
    Grower: URIRef  # This class represents growers that operate and possibly own a greenhouse to produce one or more crops as efficient and effective as possible
    GrowingHeatingPipe: URIRef  # The growing heating pipe is the heating pipe which has a diameter less than the primary heating pipe, and is installed in the middle of the canopy and operates with relatively lower water temperatures around 40 degrees
    GrowingMedia: URIRef  #
    GrowingSystem: URIRef  #
    GrowingSystemPart: URIRef  # This class represents the parts found in growing systems
    GrowthCircuit: URIRef  #
    Gutter: URIRef  #
    HPS: URIRef  # High-pressure sodium (HPS) lamps
    HeatDistributionSystem: URIRef  #
    HeatExchanger: URIRef  # Uses hot or cold water, sometimes directly with cooling media Hot water can be used for both heating and cooling
    HeatPump: URIRef  # Hybrid system that can be used for both cooling and heating, and uses multiple sources (e.g. ground warmth + fuel).
    HeatPumpSource: URIRef  #
    HeatWaterMixingValve: URIRef  #
    HeatWaterTransportPump: URIRef  #
    HeatingCoil: URIRef  # To warm up humid air before it goes into the dessicant wheel
    HeatingPipe: URIRef  #
    HeatingSystem: URIRef  #
    HeatingSystemPart: URIRef  # This class represents the parts found in heating systems
    Height: URIRef  #
    HighPressureFogging: URIRef  # "Similar to the Pad and Fan system, High Pressure Fogging works on the principal of evaporative cooling. Under a high pressure, water is introduced to a nozzle with a miniscule opening. In essence, water is divided into tiny particles, creating fog. When the temperature and humidity-levels in the greenhouse allow it, these water particles are evaporated before they hit the leaf of the crop. Just like Pad & Fan, the humidity is increased and the greenhouse air is chilled."
    HorizontalPipe: URIRef  # Horizontal pipes must be installed at a depth of 1 to 1.5 metres below the ground in order not to be unduly affected by variations in external air temperature and to retain the beneficial effects of insulation.
    HorticulturalFloatGlass: URIRef  # Two types of greenhouse glass can be distinguished; horticultural float glass and diffuse glass. The typical glass that is used for glass greenhouses is the horticultural float glass. It is a transparent glass with a high light admittance to ensure sufficient light in the greenhouse.
    Hortispot: URIRef  # het referentiepunt dient om de locatie van elementen in de afdeling te bepalen relatief ten opzichte van dit referentiepunt. Het middelpunt is gedefinieerd als een combinatie van het midden van de breedte (= X) van de afdeling, het midden van de lengte (= Y) van de afdeling en de onderkant van de kasgoot als de hoogte (=Z) van de afdeling.  a.	De X-Y positie voor de lengte-breedte is gedefinieerd vanuit een bovenaanzicht van de afdeling b.	De Z-positie voor de hoogte is gedefinieerd als een punt ter hoogte van de onderzijde van de kasgoot op de onder a bepaalde X-Y positie.  Belangrijk voordeel van deze keuze is dat het een algemeen bruikbare definitie is zonder dat er aannames worden gemaakt over de constructie van de kas. Voor de meeste gevallen zal een block een gewone rechthoek vormen, waardoor het referentiepunt in het midden van het block terecht komt. Voor een block dat geen rechthoek vormt kan het zijn dat het referentiepunt buiten het block terecht komt, omdat de X en Y-coordinaat bepaald wordt door de langste lengte en langste breedte van het block. Dat vormt echter geen probleem, omdat het referentiepunt een virtueel punt is, waarmee gerekend kan worden ongeacht de specifieke, absolute locatie.
    HortispotLocation: URIRef  # De locatie van een element in de kas ten opzichte van de hortispot Positioneringsstelsel: de positie van een element in de afdeling t.o.v. het referentiepunt wordt uitgedrukt in een XYZ-stelsel waarbij de afstand t.o.v. het referentiepunt bepaald wordt in centimeters. Om dit te kunnen bepalen is er een oriëntatie-afspraak nodig die de richting van de X-as, Y-as en Z-as bepaalt. Deze richtingen worden ook vastgelegd in deze standaard. De Y-richting loopt parallel aan de kasgoot, de X-richting staat daar loodrecht op in het horizontale vlak, en de Z-richting staat loodrecht op het X-Y-vlak. Tot slot, moet bepaald worden wat de positieve en negatieve richtingen zijn van de assen. Voor de X-as en de Y-as dient de geografische Noordpool als referentie. De coördinaten van de X-as en van de Y-as zijn positief in de richting die naar het Noorden loopt. Indien de Y-as van de kas exact op één lijn naar de Noordpool ligt, dan is de positieve richting van de X-as naar het geografische Oosten. De positieve richting van de Z-as is hemelwaarts en de negatieve richting aardwaarts. The location of an element in the greenhouse relative to the hortispot
    HotSource: URIRef  # The hot source (to which heat produced and recovered is transferred) The air or water to be heated is called a hot source. Heat may be transferred to the environment through:      Fan coils, consisting of cabinets in which air is made to circulate through heating bodies. These may be wall-mounted, ceiling-mounted or built-in models.     Coils built into the floor, in which hot water circulates. Heating occurs mainly through radiation and requires a lower water temperature.     Canalizations, which transfer the heat produced by the heat pump to the different rooms, by means of suitable air channels and inlet vents.
    HumidificationSystem: URIRef  #
    HumidityDeficit: URIRef  # Difference in absolute humidity in greenhouse air and maximum absolute humidity in air at the observed temperaure
    HybridSystem: URIRef  # Combines different energy sources for heat. For example: Geothermal energy and fuel.
    HybridSystemPart: URIRef  #
    Hydrogen: URIRef  # Hydrogen is a component of the organic compounds where we find C. Hydrogen ions are involved in electrochemical reactions to maintain charge balances across cell. membranes.
    InnerFoundation: URIRef  # The inner greenhouse foundation is to transfer the loads from the steel post to the ground or, if necessary, the drivepiles. Pre-fabricated concrete or steel dollies are used for the inner foundation. These dollies are made with a steel strip on top for seamless connection with the greenhouse posts. The dollies are placed in boreholes with a calculated diameter and filled with concrete. Underneath the cross brace columns, the borehole is always carried out lareger than at the rest of the inner columns, because more load is being transferred.
    InnerWall: URIRef  #
    Iron: URIRef  # Iron is used in the biochemical reactions that form chlorophyll and is a part of one of the enzymes that is responsible for the reduction of nitrate nitrogen to ammoniacal nitrogen. Other enzyme systems such as catalase and peroxidase also require Fe. This is the level of iron in a sample of water measured in µmol/l
    IrrigationFeedPump: URIRef  #
    IrrigationFlowrateSensor: URIRef  # It measures the amount of water that is supplied to the greenhouse. For a certain amount of water it gives a pulse to the climate computer such that the climate computer can calculate how much water is supplied to the greenhouse. For example for 10 pulses = 10x100l = the right amount so it should stop
    IrrigationPump: URIRef  #
    IrrigationSupplyPump: URIRef  #
    IrrigationSystem: URIRef  #
    IrrigationSystemPart: URIRef  #
    IrrigationValve: URIRef  # An irrigation valve is a switch that steers the amount of water in a zone
    IrrigationWater: URIRef  #
    Juice: URIRef  #
    KaliumCalciumRatio: URIRef  #
    LED: URIRef  #
    Laborer: URIRef  #
    Leaf: URIRef  # This class represents the leaf of a plant
    Length: URIRef  #
    Level: URIRef  #
    Light: URIRef  #
    LightingSystem: URIRef  #
    Lisianthus: URIRef  # This class represents flowers that are named Lisianthus, officially known as Eustoma.
    LiterCounterSensor: URIRef  #
    Location: URIRef  #
    LowerCircuit: URIRef  #
    Magnesium: URIRef  # Magnesium plays an important role in plant cells since it appears in the center of the chlorophyll molecule. Certain enzymatic reactions require Mg as a cofactor. This is the level of magnesium in a sample of water measured in mmol/l of mg/l
    Manganese: URIRef  # Manganese functions in several enzymatic reactions that involve the energy compound adenosine triphosphate (ATP). Manganese also activates several enzymes and is involved with the processes in the electron transport system in photosynthesis. This is the level of manganese in a sample of water measured in µmol/l
    Measurement: URIRef  # A kind of observation which is specifically made with instruments in a Greenhouse
    MechanicalRefrigeration: URIRef  # An example of such a cooling system is an absorption refrigerator Een voorbeeld van mechanische koeling is een absorptiekoelmachine
    MechanicalRefrigerationPart: URIRef  #
    Methane: URIRef  #
    MixingTank: URIRef  # The tank in which the water is mixed with the fertilizer/nutrition The tank where the concentrated fertilizer solutions from fertilizer tanks are mixed with clean water from the water tank This class is part of the WHC use case
    Molybdenum: URIRef  # Molybdenum is a constituent of two enzymes involved in nitrogen metabolism. The most important of these is nitrate reductase. This is the level of molybdenum in a sample of water measured in µmol/l
    MorphologicalTrait: URIRef  # All traits related to anatomical (internal) and morphological (external) structure of the plant, its organs and tissues.
    MultiPurposeTubeRailHeatingSystem: URIRef  #
    Natrium: URIRef  # Sodium is commonly present in water, but only small quantities are taken up by plants. An excess of sodium causes salinity problems. If the sodium concentration in the root zone is too high, it will be detrimental to the crop. If Na accumulates above the maximum acceptable concentration in the root zone, growers must discharge a fraction of the recirculated nutrient solution in order to prevent yield reduction or a decline in product quality. This is the level of natrium in a sample of water measured in mmol/l of mg/l
    Net: URIRef  # This class represents different kind of nets that are used in greenhouses
    Nitrate: URIRef  # This is the level of nitrate in a sample of water measured in mmol/l of mg/l
    Nitrogen: URIRef  # Nitrogen is a very important element for plant growth and is found in many compounds. These include chlorophyll (the green pigment in plants), amino acids, proteins, nucleic acids, and organic acids. This is the level of nitrogen as part of nitrate in a sample of a fluid measured in mmol/l or mg/l
    NitrogenTotalLevel: URIRef  # This is the total level of nitrogen in a sample of a fluid measured in mg/year
    Nokschot: URIRef  # A plastic screen in the ridge of the roof of the greenhouse that precents airflows in the upper regions of the greenhouse
    Nozzle: URIRef  # Are located above the crop and fixed onto a water pipe. They have really small openings to ensure the water is misted.
    NumberOfLeaves: URIRef  #
    NutritionProperty: URIRef  #
    Oxygen: URIRef  # Oxygen is the third element in typical organic molecules such as simple sugars. The presence of O is important for many plant biochemical reactions.
    PAR: URIRef  # Photosynthetically active radiation, often abbreviated PAR, designates the spectral range (wave band) of solar radiation from 400 to 700 nanometers that photosynthetic organisms are able to use in the process of photosynthesis. This spectral region corresponds more or less with the range of light visible to the human eye. Photons at shorter wavelengths tend to be so energetic that they can be damaging to cells and tissues, but are mostly filtered out by the ozone layer in the stratosphere. Photons at longer wavelengths do not carry enough energy to allow photosynthesis to take place.
    PH: URIRef  #
    PHCheckSensor: URIRef  #
    PHDoseSensor: URIRef  #
    PadAndFanSystem: URIRef  # "The Pad & Fan cooling method is a widely applicable cooling system due to it’s simplicity. As the name indicates, it uses a combination of wet-pads and ventilators. A set of large fans blow air out of the greenhouse, causing a suction-draught through the greenhouse. On the opposite sides of the fans, pad-walls are installed which are kept wet. The suction-movement caused by the fans, forces hot outside air to be pulled into the greenhouse through the wet pads. Water from the pads evaporates into the hot air, increasing its humidity whilst lowering the temperature." Can also be used as forced ventilation and is part of a semi-closed greenhouse system, can also be a independent system
    PadAndFanSystemPart: URIRef  #
    Part: URIRef  # Model-technical term This class represents parts of wholes
    PassiveHeatStorageSystem: URIRef  # system where you store energy without any device. An example is a thick wall to store warmth
    PerimeterFoundation: URIRef  # The foundation for the perimeter of the greenhouse differs from that of the inner foundation. The perimeter foundation is a continuous concrete beam with a minimum height of 30 cm. This outer perimeter can be pre-fabricated or can be custom made on the construction site. Similar to the inner foundation, the pre-fabricated beam is connected to dollies, which are casted into a borehole that is filled with concrete.
    Pest: URIRef  # This class represents pests
    Petal: URIRef  # This class represents the petal of a flower
    PhenologicalTrait: URIRef  # All traits related to growth/developmental stages and periods of crop/plants.
    Phosphorus: URIRef  # Phosphorus is used in several energy transfer compounds in the plants. A very important function for P is its role in nucleic acids, the building blocks for the genetic code material in plant cells. This is the level of phosphorus in a sample of water measured in mmol/l or mg/l
    Photosynthesis: URIRef  # The rate of photosynthesis gives the amount of CO2 that's consumed by the crops. example unit: kg/m2/s. This means x kilograms of CO2 is consumed by a square meter per second.
    PhysiologicalTrait: URIRef  # All traits related to functioning of the crop/plant and its response/adaptation to the environment.
    PhytotoxicProperty: URIRef  #
    Picker: URIRef  #
    Pipe: URIRef  # This class represents different kind of pipes that are used in and around a greenhouse
    Pistil: URIRef  # This class represents the pistil of a flower
    Plant: URIRef  # A plant, multiple plants, or plant parts can be crops. Plants are mainly multicellular, predominantly photosynthetic eukaryotes of the kingdom Plantae. Historically, plants were treated as one of two kingdoms including all living things that were not animals, and all algae and fungi were treated as plants. However, all current definitions of Plantae exclude the fungi and some algae, as well as the prokaryotes (the archaea and bacteria). By one definition, plants form the clade Viridiplantae (Latin name for "green plants"), a group that includes the flowering plants, conifers and other gymnosperms, ferns and their allies, hornworts, liverworts, mosses and the green algae, but excludes the red and brown algae.
    PlantPart: URIRef  # Model-technical term This class represents the different parts of a plant
    Position: URIRef  # De window position wordt gegeven met een percentage. 100% betekent dat het raam compleet open is, 0% dat het raam compleet dicht is.  De window position wordt periodiek gemeten, en verschilt ook iedere keer.
    PotableWater: URIRef  #
    Potassium: URIRef  # Potassium is used as an activator in many enzymatic reactions in the plant. Another role for K in plants occurs in special leaf cells called guard cells found around the stomata. Guard cell turgor (or lack of turgor) controls the degree of opening of the stomata and thus controls the level of gas and water vapor exchange through the stomata. Turgor is largely controlled by K movement in and out of the guard cells. This is the level of kalium in a sample of water measured in mmol/l or mg/l
    PowerSource: URIRef  #
    PressureAdjustingValve: URIRef  # Can adjust the pressure to compensate differences in the pump
    PressurePump: URIRef  #
    PrimaryHeatingPipe: URIRef  # The Primary Heating Pipe is used inside the greenhouse compartment to distribute the heated water. This pipe is around 60 degrees Celcius.
    PullWireSystem: URIRef  # has minimal light interception and requires minimal maintenance during the years of operation. The screening system is partially integrated into the greenhouse steel frame. Proper fixation points are provided in the greenhouse design to ensure trouble free installation.
    PushPullMechanism: URIRef  # When it comes to Venlo greenhouses, the push-pull mechanism is the mechanism of choice. The push-pull-tube slides above the upperside of the tellis. The push-pull-tube is connected to the lower aluminium profile of the ventilation-window section by means of push-rods. The amount of push-rods that are required is dependent of the ventilation window size and the windspeeds that are taken into account. Drive motors allow the push-pull-tube to move back and forward and with that, regulating the opening of the vents.
    QualityTrait: URIRef  # All traits related to key characteristics that influence end-use quality of crop/plant products (seed, fruit, leaf, root/tuber, etc.) and subproducts (flour, dough, pulp, etc.)
    Radiation: URIRef  # unit: watt or µmol/m2/s
    RailPipeSystem: URIRef  #
    Rain: URIRef  #
    RainWater: URIRef  #
    Receiver: URIRef  # As a temporary storage and a surge tank for liquid refrigerant, the receiver acts as a vapour seal. With a primary purpose of preserving the vapour moving down the liquid line to the expansion valve, receivers can be made for both horizontal and vertical installation.
    RelativeHumidity: URIRef  # The amount of moisture in the air is generally expressed as relative humidity (RH), which is the ratio between the weight of moisture actually present in the air and the total moisture-holding capacity of a unit volume of air at a specific temperature and pressure. This term can sometimes be misleading, because it is temperature-dependent. Warm air has a higher moisture-holding capacity than cooler air; therefore as the temperature of air increases, the relative humidity decreases even though the amount of water remains constant. Air at 70° F will hold twice as much moisture as air at 50°F. In the range of temperatures encountered in a greenhouse, for every 20° F rise in dry bulb temperature, the water-holding capacity of the air doubles, and the relative humidity is reduced by one-half. This relationship is important in managing humidity in the greenhouse.
    Reservoir: URIRef  #
    ReturnManifold: URIRef  # component that measures the overall temperature of the water coming back from the greenhouse
    Ridge: URIRef  #
    Rod: URIRef  #
    Roof: URIRef  #
    RoofRod: URIRef  #
    RoofSprinklingSystem: URIRef  # Used for cooling the outside of the glass roof
    Root: URIRef  #
    RootDevelopmentLevel: URIRef  # The preception of the level of development of the root of a plant as a number between 1 and 10 from bad to good
    Rose: URIRef  #
    SON: URIRef  # SON-E is elliptical (bulbous), and SON-T is tubular.
    Screen: URIRef  # This class represents different kind of screens that are used in greenhouses
    ScreeningSystem: URIRef  # Energy is one of the largest operational expenditures for all greenhouse operations. To improve the energy efficiency of a greenhouse, horizontal screens have been installed in greenhouses for decades now. The horizontal screening system forms an insulating layer suspended over the crop. Depending on the type of screening fabric installed, the screening system can have energy saving-, diffusing-, shading- and also black-out properties. Due to the impact on the climate the screens have, they are also referred to as climate screens.
    SeaWater: URIRef  #
    SecondaryBranch: URIRef  #
    Section: URIRef  #
    Seed: URIRef  #
    SemiClosedGreenhouse: URIRef  # "Semi-closed greenhouses make use of a so-called climate chamber, where the air is either cooled or heated. With large ventilators this treated air is blown into the greenhouse in polyethylene tubes underneath the hanging gutters."
    ShadeScreen: URIRef  # Some times to increase the isolation of the greenhouse (to reduce the heat losses) we apply both screens during the night. In this case we use both energy and shading screen for saving energy purposes. Most of modern greenhouse controllers have this option, to use both screens for both options. From a climate controller we can see that the shading screen has a value of 1 (which means closed or applied) at the same time when the energy screen is also 1. This depends on the configuration of the climate controller. This class represents shading screens in greenhouses
    ShadingCurtain: URIRef  #
    ShadingNet: URIRef  # This class represents shading nets that are used in greenhouses
    SideWall: URIRef  #
    Silicon: URIRef  # This is the level of silicon in a sample of water measured in µmol/l
    SolarPower: URIRef  #
    SolutionSensor: URIRef  # This class represents sensors that measure properties of a solution
    Source: URIRef  #
    Speed: URIRef  #
    Status: URIRef  #
    SteelStructure: URIRef  # The steel structure of a Dutch Venlo greenhouse consists out of the following primary construction elements: columns, trusses, beams, purlins and braces. Together, these elements deal with the forces applied to them by means of the weight of the greenhouse, wind, snow, the crop and the installation loads. Due to the importance of light in the greenhouse, all steel structural elements are carried out as light as possible whilst complying with the constructual regulations.
    Stem: URIRef  # This class represents the stem of a plant
    SubstrateTemperatureSensor: URIRef  #
    Sugar: URIRef  # This is the concentration of sugar in a sample of a fluid measured in a percentage
    Sulfur: URIRef  # Sulfur is a component of sulfur-containing amino acids such as methionine. Sulfur also is contained in the sulfhydryl group of certain enzymes. This is the level of sulfur in a sample of water measured in mmol/l or mg/l
    Sunlight: URIRef  #
    SupplyManifold: URIRef  # Regulates homogeneous water temperature component that measures the overall temperature of the water going to the greenhouse
    SurfaceWaterHeatPump: URIRef  #
    Surroundings: URIRef  # Surroundings of the greenhouse
    SystemPart: URIRef  # Model-technical term This class represents the different kind of parts found in systems
    Tank: URIRef  #
    TapWater: URIRef  #
    Temperature: URIRef  #
    TemperatureSensor: URIRef  # This class represents sensors that measure a temperature
    ThermalScreen: URIRef  # This class represents thermal screens in greenhouses
    ThermostaticExpansionValve: URIRef  # Before the evaporator, this is located at the end of the liquid line. TXV is a device that controls the amount of refrigerant that flows to the evaporator. There you will find the floodback that is essential to maximise the productivity of the evaporator, while stopping the extra liquid refrigerant from going back to the compressor. This device also helps to separate the high pressure and the low pressure sides of an air conditioning system. Through the system’s liquid line, high pressured liquid refrigerant enters the valve but with the TVX’s presence, the amount of liquid refrigerant entering the evaporator will be abridged.
    Tomatoplant: URIRef  #
    Trait: URIRef  # The trait is a combination of entities and attributes CO defines a trait as a character of an individual plant or of a group of plants that can be observed and that results from the expression of its genes and their interaction with the environment. This trait definition can be summarized by “what is observed”. Examples of traits are “plant height’, “pod color”, “grain yield”, “seed germination rate”, “plant flowering time”, “panicle shape”, “plant resistance to blight”, etc. Traits can be formalized by a meaningful combination of entities and attributes. The entity is the observed plant part. The entity can be defined at the level of the cell, the tissue, the organ, the whole organism or the sub-product of the crop. The attribute is the feature of an entity. Attributes can be states or processes. Examples of states are weight, length, area, color, chemical content, while examples of processes are vegetative period duration, photosynthesis rate, senescence rate. A direct consequence of the trait decomposition into entity and attribute is that two traits that share the same combination of attributes are identical even though they are named differently. Thus, decomposing a trait into entity/attribute is a good practice to prevent trait duplication. Table 3 shows examples of trait breakdown into entity/attribute. A trait can be described by a general entity or as a specimen, something that obviously belongs to an entity but is noticed by reason of an individual distinguishing characteristic. Examples of specimen are primary branch, first flower, first grade commercial fruit, flag leaf, third leaf, main stem, fertile stem, mature fruit, immature fruit.
    TransportHeatingPipe: URIRef  # Heating pipe that transports the heated water from the main heating system to the greenhouse compartment
    Tuber: URIRef  #
    UnderfloorHeatingSystem: URIRef  #
    UniformityLevel: URIRef  # The preception of the uniformity of a plant as a number between 1 and 10 from bad to good
    VPD: URIRef  # Vapour-pressure deficit, or VPD, is the difference (deficit) between the amount of moisture in the air and how much moisture the air can hold when it is saturated. Once air becomes saturated, water will condense out to form clouds, dew or films of water over leaves. It is this last instance that makes VPD important for greenhouse regulation. If a film of water forms on a plant leaf, it becomes far more susceptible to rot. On the other hand, as the VPD increases, the plant needs to draw more water from its roots. In the case of cuttings, the plant may dry out and die. For this reason the ideal range for VPD in a greenhouse is from 0.45 kPa to 1.25 kPa, ideally sitting at around 0.85 kPa. As a general rule, most plants grow well at VPDs of between 0.8 and 0.95 kPa.
    Valve: URIRef  # This class represents different kind of valves of greenhouses
    VenloGreenhouse: URIRef  #
    VentilationSystem: URIRef  # Ventilation is a crucial tool for growers to create a good growing climate in their greenhouses. Opening from the ridge, the ventilation vents are positioned at the highest place of the Dutch Venlo greenhouse, making it the best position to discharge hot air from the greenhouse. There are several options regarding the ventilation capacity of a Venlo greenhouse, choices can be made between 1 pane-, 2 pane, 3 pane- and 4 pane-ventialtion. The depth of the windows also largely influence the ventilation capacity of the greenhouse. Ventilation system could use fans too.
    VentilationSystemPart: URIRef  #
    VentilationVent: URIRef  # Ventilation is a crucial tool for growers to create a good growing climate in their greenhouses. Opening from the ridge, the ventilation vents are positioned at the highest place of the Dutch Venlo greenhouse, making it the best position to discharge hot air from the greenhouse.
    VentilationWindow: URIRef  #
    VerticalPipe: URIRef  # Vertical pipes can reach a depth of several tens of metres. They do not occupy space horizontally, but they require the boring of suitable deep wells.
    Wall: URIRef  #
    WallRod: URIRef  #
    Water: URIRef  #
    WaterBuffer: URIRef  #
    WaterDistributionPad: URIRef  #
    WaterFilter: URIRef  #
    WaterPower: URIRef  #
    WaterQuality: URIRef  # Water can be classified in three levels of quality according to the levels of sodium and chloride.
    WaterSoftener: URIRef  #
    WaterStorageSystem: URIRef  #
    WaterStorageSystemPart: URIRef  #
    WaterSupplyPadPump: URIRef  # Used to pump water towards the evaporative cooling pad.
    WaterSystem: URIRef  # This class represents the systems in the greenhouse that deal with water. This includes the infrastructure of the systems as well as the management functionality.
    WaterSystemPart: URIRef  # This class represents the parts found in heating systems
    WaterTemperatureReturnManifoldSensor: URIRef  #
    WaterTemperatureSupplyManifoldSensor: URIRef  #
    WaterTreatmentSystem: URIRef  # System to clean the water before sending it to the nozzles. Usually we use reverse osmosis, but we can also have ultrafiltration. Used for filtering and cleaning the water such that you can create a mist.
    Weather: URIRef  # The weather is a direct, day-to-day state of temperature, air pressure, moisture, and more factors outside of the greenhouse.
    WeatherCircumstance: URIRef  #
    WellWater: URIRef  #
    WhitewashSolution: URIRef  #
    WidespanGreenhouse: URIRef  # The steel support halfway up the rod is typical for a widespan greenhouse Typisch is de stalen ondersteuning halverwege de roede
    Wind: URIRef  #
    WindEnergy: URIRef  #
    Zinc: URIRef  # This is the level of zinc in a sample of water measured in µmol/l Zinc is involved in the activation of several enzymes in the plant and is required for the synthesis of indoleacetic acid, a growth regulator.
    Zone: URIRef  # A zone is an area in which the same irrigation and fertilization strategy is applied A zone is located inside a compartment. Therefore the climate is controlled in the same way. Inside a zone, the irrigation and fertilization is also controlled in the same way.
    competencyQuestion: URIRef  #
    contains: URIRef  #
    hasActualPositionRatio: URIRef  #
    hasAltitude: URIRef  #
    hasAngularDeflection: URIRef  #
    hasApplicationDate: URIRef  #
    hasArea: URIRef  #
    hasBlock: URIRef  #
    hasCapacity: URIRef  #
    hasCatchFactor: URIRef  #
    hasConstructionType: URIRef  #
    hasCoolingCapacity: URIRef  # Representative values are 40-50W/m2 for cold areas where cooling is not needed  to more than 200 W/m2 for hot areas. Please notice that when we have a mechanical cooling in SIOM this value represents the electrical power and not the cooling power. The cooling power is related to the performance (COP) of the cooling system and for simplicity we can assume that is 3 times more than the cooling power. So if we have 150 W/m2 electrical cooling power and COP=3, the max cooling power applied in the greenhouse is 150 * 3 = 450 W/m2.
    hasCoverMaterialType: URIRef  #
    hasDate: URIRef  #
    hasDepth: URIRef  #
    hasDrainFactor: URIRef  #
    hasEnergyScreenUsage: URIRef  # Some times to increase the isolation of the greenhouse (to reduce the heat losses) we apply both screens during the night. In this case we use both energy and shading screen for saving energy purposes. Most of modern greenhouse controllers have this option, to use both screens for both options. From a climate controller we can see that the shading screen has a value of 1 (which means closed or applied) at the same time when the energy screen is also 1. This depends on the configuration of the climate controller.
    hasHeight: URIRef  #
    hasHortispotLocationX: URIRef  # De locatie van een element in de kas ten opzichte van de hortispot: de X-richting staat daar loodrecht op in het horizontale vlak
    hasHortispotLocationY: URIRef  # De locatie van een element in de kas ten opzichte van de hortispot: De Y-richting loopt parallel aan de kasgoot.
    hasHortispotLocationZ: URIRef  # De locatie van een element in de kas ten opzichte van de hortispot: de Z-richting staat loodrecht op het X-Y-vlak
    hasHortispotX: URIRef  # van het midden van de breedte (= X) van de afdeling
    hasHortispotY: URIRef  # het midden van de lengte (= Y) van de afdeling
    hasHortispotZ: URIRef  # en de onderkant van de kasgoot als de hoogte (=Z) van de afdeling
    hasLatitude: URIRef  #
    hasLeafAreaIndex: URIRef  #
    hasLength: URIRef  #
    hasLightingType: URIRef  #
    hasLocation: URIRef  #
    hasLongitude: URIRef  #
    hasMaxHeatingPower: URIRef  # It is the max heating power applied in the greenhouse in units of W/m2. It is not measured. It is a value calculated according to the specifications / characteristics of the heating system. This is a max value which means that for example the boiler can not provide more that this. For example for a greenhouse of 10000m2 (1ha) if this value is 120W/m2, and the combinded efficiency of the boiler + distribution system is 85%, the max heating power can be provided by the boiler is 120*10000/85% = 1.41MW. This is a simple example without any heat storage. If we have a heat storage, which is very common, then the max heating power from the boiler can be different than 1.41MW. Heating capacity depends strongly from the area. There are areas where there are small heating needs and then this value can be even less than 50W/m2 and areas with high needs, this value can be even higher than 200W/m2.
    hasOrientation: URIRef  #
    hasPart: URIRef  #
    hasPlantingDate: URIRef  #
    hasPower: URIRef  #
    hasPrimaryWaterSource: URIRef  #
    hasRemovalDate: URIRef  #
    hasSecondaryWaterSource: URIRef  #
    hasSoilType: URIRef  #
    hasSpanWidth: URIRef  #
    hasSurroundings: URIRef  #
    hasSurroundingsType: URIRef  #
    hasTypeName: URIRef  #
    hasWidth: URIRef  #
    hasZone: URIRef  #
    isApplicated: URIRef  #
    isPreventedBy: URIRef  #
    lucht1: URIRef  #
    observatie1: URIRef  #
    pHSensor: URIRef  # The fertigation unit has at least 1, in the Netherlands usually 2, measures the pH value in the water
    partOf: URIRef  #
    prevents: URIRef  #
    result1: URIRef  #
    temperature1: URIRef  #
