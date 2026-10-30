import time;
import datetime;
from datetime import timedelta;
from typing import Optional , List;
from enum import Enum;
from pydantic import BaseModel , Field , create_model;

class get_userdata_generic( BaseModel ):
				id     : Optional[ str ] = Field( None , description = "" );
				limit  : Optional[ int ] = Field( None , description = "" );
				offset : Optional[ int ] = Field( None , description = "" );


class get_userdata_generic_livestock( BaseModel ):
				id     : Optional[ str ] = Field( None , description = "" );
				limit  : Optional[ int ] = Field( None , description = "" );
				offset : Optional[ int ] = Field( None , description = "" );


class get_dat( BaseModel ):
				id     : Optional[ str ] = Field( None , description = "" );
				limit  : Optional[ int ] = Field( None , description = "" );
				offset : Optional[ int ] = Field( None , description = "" );
				crop_or_livestock_test_case : Optional[ str ] = Field( None , description = "Type" );
				dats_category : Optional[ str ] = Field( None , description = "DAT category" );
				test_case_number : Optional[ str ] = Field( None , description = "TC Number" );
				tc_name_title : Optional[ str ] = Field( None , description = "TC Name" );
				tc_country : Optional[ str ] = Field( None , description = "TC Country" );
				crop_or_animal_type : Optional[ str ] = Field( None , description = "TC Animal Type" );


class get_crop( BaseModel ):
				id     : Optional[ str ] = Field( None , description = "" );
				limit  : Optional[ int ] = Field( None , description = "" );
				offset : Optional[ int ] = Field( None , description = "" );
				crop_or_livestock_test_case : Optional[ str ] = Field( None , description = "Type" );
				dats_category : Optional[ str ] = Field( None , description = "DAT category" );
				test_case_number : Optional[ str ] = Field( None , description = "TC Number" );
				tc_name_title : Optional[ str ] = Field( None , description = "TC Name" );
				tc_country : Optional[ str ] = Field( None , description = "TC Country" );
				crop_or_animal_type : Optional[ str ] = Field( None , description = "TC Animal Type" );
				datss_name : Optional[ str ] = Field( None , description = "DAT name" );


class get_livestock( BaseModel ):
				id     : Optional[ str ] = Field( None , description = "" );
				limit  : Optional[ int ] = Field( None , description = "" );
				offset : Optional[ int ] = Field( None , description = "" );
				crop_or_livestock_test_case : Optional[ str ] = Field( None , description = "Type" );
				dats_category : Optional[ str ] = Field( None , description = "DAT category" );
				test_case_number : Optional[ str ] = Field( None , description = "TC Number" );
				tc_name_title : Optional[ str ] = Field( None , description = "TC Name" );
				tc_country : Optional[ str ] = Field( None , description = "TC Country" );
				crop_or_animal_type : Optional[ str ] = Field( None , description = "TC Animal Type" );
				datss_name : Optional[ str ] = Field( None , description = "DAT name" );


class userdata_generic( BaseModel ):
				total_area_ha : Optional[ float ] = Field( None , description = "Total Area (ha)" );
				years_of_usage : Optional[ float ] = Field( None , description = "YEARS OF USAGE" );
				current_yield_tonsha : Optional[ float ] = Field( None , description = "Current Yield (tons/ha)" );
				market_priceoneton : Optional[ float ] = Field( None , description = "Market Price (€/ 1ton)" );
				current_fertilizer_usage_kg_ha : Optional[ float ] = Field( None , description = "Current fertilizer usage (Kg/ ha)" );
				current_fertilizer_cost_one_kg : Optional[ float ] = Field( None , description = "Current Fertilizer Cost (€/ 1 Kg)" );
				current_water_usage_m3ha : Optional[ float ] = Field( None , description = "Current water usage (m3/ha)" );
				current_water_costm3 : Optional[ float ] = Field( None , description = "Current water cost (€/ m3)" );
				current_pestcide_usage_kg_or_lt_ha : Optional[ float ] = Field( None , description = "Current pestcide usage (kg or lt/ ha)" );
				current_pesticide_costkg_or_lt : Optional[ float ] = Field( None , description = "Current pesticide cost (€/ kg or lt)" );
				current_labor_costin_one_year : Optional[ float ] = Field( None , description = "Current Labor Cost (€ in 1 year)" );
				current_fuel_costin_one_year : Optional[ float ] = Field( None , description = "Current Fuel Cost (€ in 1 year)" );
				current_electricity_costin_one_year : Optional[ float ] = Field( None , description = "Current Electricity Cost (€ in 1 year)" );
				user_id : Optional[ str ] = Field( None , description = "User ID" );


class userdata_generic_livestock( BaseModel ):
				years_of_usage : Optional[ float ] = Field( None , description = "YEARS OF USAGE" );
				number_of_animals : Optional[ float ] = Field( None , description = "Number of cows" );
				average_meat_price_euro_per_kg : Optional[ float ] = Field( None , description = "Average meat price  (€/ kg)" );
				average_meat_produced_per_year_kg : Optional[ float ] = Field( None , description = "Average meat produced per year (kg/year)" );
				average_oyster_price_euro_per_kg : Optional[ float ] = Field( None , description = "Average oyster price  (€/ kg)" );
				average_oysters_produced_per_year_kg : Optional[ float ] = Field( None , description = "Average oyster produced per year (kg/year)" );
				average_honey_price_euro_per_kg : Optional[ float ] = Field( None , description = "Average honey price  (€/ kg)" );
				average_honey_produced_per_year_kg : Optional[ float ] = Field( None , description = "Average honey produced per year (kg/year)" );
				average_milk_price_per_liter_euro_per_liter : Optional[ float ] = Field( None , description = "Average milk price per liter (€/ liter)" );
				average_liters_of_milk_produced_per_animal_per_day_with_dat_s_l : Optional[ float ] = Field( None , description = "Average liters of milk produced per cow per day (l)" );
				current_electricity_consumption_without_dats_usage_in_kwh : Optional[ float ] = Field( None , description = "Current electricity Consumption  (in kWh)" );
				cost_of_electricity_per_kwh_euro : Optional[ float ] = Field( None , description = "Cost of electricity per kWh (€)" );
				current_labor_cost_without_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Current Labor Cost (€ in 1 year)" );
				current_feed_cost_without_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Current Feed Waste Cost (€ in 1 year)" );
				current_mortality_cost_without_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Current Mortality Cost (€ in 1 year)" );
				current_fuel_cost_without_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Current Fuel Cost (€ in 1 year)" );
				current_drug_cost_without_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Current Drugs Cost (€ in 1 year)" );
				current_water_cost_euro_in_one_year : Optional[ float ] = Field( None , description = "Current Water Cost (€ in 1 year)" );
				user_id : Optional[ str ] = Field( None , description = "User ID" );


class dat( BaseModel ):
				crop_or_livestock_test_case : Optional[ str ] = Field( None , description = "Type" );
				dats_category : Optional[ str ] = Field( None , description = "DAT category" );
				test_case_number : Optional[ str ] = Field( None , description = "TC Number" );
				tc_name_title : Optional[ str ] = Field( None , description = "TC Name" );
				tc_country : Optional[ str ] = Field( None , description = "TC Country" );
				crop_or_animal_type : Optional[ str ] = Field( None , description = "TC Animal Type" );
				datss_name : Optional[ str ] = Field( None , description = "DAT name" );
				datss_short_description : Optional[ str ] = Field( None , description = "DAT short Description" );
				datss_provider_website : Optional[ str ] = Field( None , description = "DAT provider website" );
				dats_cost_structure_infoi : Optional[ str ] = Field( None , description = "DATS Cost structure info" );
				kpi_info_outcomes_used : Optional[ str ] = Field( None , description = "KPI Info / Outocmes Used" );


class crop( BaseModel ):
				crop_or_livestock_test_case : Optional[ str ] = Field( None , description = "Type" );
				dats_category : Optional[ str ] = Field( None , description = "DAT category" );
				test_case_number : Optional[ str ] = Field( None , description = "TC Number" );
				tc_name_title : Optional[ str ] = Field( None , description = "TC Name" );
				tc_country : Optional[ str ] = Field( None , description = "TC Country" );
				crop_or_animal_type : Optional[ str ] = Field( None , description = "TC Animal Type" );
				datss_name : Optional[ str ] = Field( None , description = "DAT name" );
				datss_short_description : Optional[ str ] = Field( None , description = "DAT short Description" );
				datss_provider_website : Optional[ str ] = Field( None , description = "DAT provider website" );
				dats_cost_structure_infoi : Optional[ str ] = Field( None , description = "DATS Cost structure info" );
				kpi_info_outcomes_used : Optional[ str ] = Field( None , description = "KPI Info / Outocmes Used" );
				total_area_ha : Optional[ float ] = Field( None , description = "Total Area (ha)" );
				years_of_usage : Optional[ float ] = Field( None , description = "YEARS OF USAGE" );
				initial_cost_of_investment_euro : Optional[ float ] = Field( None , description = "Initial cost of Investment (€)" );
				initial_cost_of_investment_euro_ha : Optional[ float ] = Field( None , description = "Initial cost of Investment (€)/ha" );
				maintainance_costs_euro_year : Optional[ float ] = Field( None , description = "Maintainance Costs (€)/year" );
				maintainance_costs_euro_ha_year : Optional[ float ] = Field( None , description = "Maintainance Costs (€)/ha/year" );
				depreciation_euro_year : Optional[ float ] = Field( None , description = "Depreciation (€)/year" );
				total_initial_cost_of_dat_purchase : Optional[ float ] = Field( None , description = "Total Initial cost of DAT Purchase" );
				yield_impact_with_dats_usage_percentage : Optional[ float ] = Field( None , description = "Yield Impact with DATS usage (%)" );
				current_yield_tonsha : Optional[ float ] = Field( None , description = "Current Yield (tons/ha)" );
				market_priceoneton : Optional[ float ] = Field( None , description = "Market Price (€/ 1ton)" );
				current_revenue_without_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Current Revenue without DATS usage (€ in 1 year)" );
				yield_with_dats_usage_tons_ha : Optional[ float ] = Field( None , description = "Yield with DATS usage (tons/ha)" );
				price_of_yield_with_dats_usage_euro_ha : Optional[ float ] = Field( None , description = "Price of Yield with DATS usage (€/ ha)" );
				revenue_impact_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Revenue Impact with DATS usage (€ in 1 year)" );
				fertilization_impact_with_dats_usage_precentage_n_applied : Optional[ float ] = Field( None , description = "Fertilization Impact with DATS usage (%)- N applied (%)" );
				current_fertilizer_usage_kg_ha : Optional[ float ] = Field( None , description = "Current fertilizer usage (Kg/ ha)" );
				current_fertilizer_cost_one_kg : Optional[ float ] = Field( None , description = "Current Fertilizer Cost (€/ 1 Kg)" );
				current_fertilization_cost_without_dats_usage_euro_ha : Optional[ float ] = Field( None , description = "Current Fertilization Cost without DATS usage (€/ ha)" );
				fertilizer_usage_with_dats_kg_ha : Optional[ float ] = Field( None , description = "Fertilizer usage with DATS (kg/ha)" );
				fertilizer_cost_with_dats_usage_euro_ha : Optional[ float ] = Field( None , description = "Fertilizer Cost with DATS usage  (€/ ha)" );
				fertilization_cost_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Fertilization Cost with DATS usage  (€ in 1 year)" );
				pesticides_impact_with_dats_usage_precentage : Optional[ float ] = Field( None , description = "Pesticides Impact with DATS usage (%)" );
				current_pestcide_usage_kg_or_lt_ha : Optional[ float ] = Field( None , description = "Current pestcide usage (kg or lt/ ha)" );
				current_pesticide_costkg_or_lt : Optional[ float ] = Field( None , description = "Current pesticide cost (€/ kg or lt)" );
				current_pesticide_cost_without_dats_usage_europer_ha : Optional[ float ] = Field( None , description = "Current pesticide cost without DATS  usage (€/ ha)" );
				pesticide_usage_with_dats_kg_or_lt_perha : Optional[ float ] = Field( None , description = "Pesticide usage with DATS (kg or lt /ha)" );
				pesticide_cost_with_dats_usage_europer_ha : Optional[ float ] = Field( None , description = "Pesticide Cost with DATS usage (€/ ha)" );
				pesticide_cost_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Pesticide Cost with DATS usage (€ in 1 year)" );
				water_consumption_impact_with_dats_usage_percentage : Optional[ float ] = Field( None , description = "water consumption  impact with dats usage (%)" );
				current_water_usage_m3ha : Optional[ float ] = Field( None , description = "Current water usage (m3/ha)" );
				current_water_costm3 : Optional[ float ] = Field( None , description = "Current water cost (€/ m3)" );
				current_irrigation_cost_without_dats_usage_europer_ha : Optional[ float ] = Field( None , description = "Current Irrigation Cost without DATS usage (€/ ha)" );
				water_usage_with_dats_m3perha : Optional[ float ] = Field( None , description = "Water usage  with DATS (m3/ha)" );
				water_cost_with_dats_usage_europer_ha : Optional[ float ] = Field( None , description = "Water Cost with DATS usage (€/ ha)" );
				water_cost_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Water Cost with DATS usage  (€ in 1 year)" );
				working_time_impact_with_dats_usage_percentage : Optional[ float ] = Field( None , description = "Working Time Impact with DATS usage (%)" );
				current_labor_costin_one_year : Optional[ float ] = Field( None , description = "Current Labor Cost (€ in 1 year)" );
				working_time_cost_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Working Time Cost with DATS usage  (€ in 1 year)" );
				fuel_consumption_impact_with_dats_usage_percentage : Optional[ float ] = Field( None , description = "Fuel Consumption Impact with DATS usage (%)" );
				current_fuel_costin_one_year : Optional[ float ] = Field( None , description = "Current Fuel Cost (€ in 1 year)" );
				fuel_cost_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Fuel cost with DATS usage  (€ in 1 year)" );
				electricity_consumption_impact_with_dats_usage_percentage : Optional[ float ] = Field( None , description = "Electricity consumption Impact with DATS usage (%)" );
				current_electricity_costin_one_year : Optional[ float ] = Field( None , description = "Current Electricity Cost (€ in 1 year)" );
				electricity_cost_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Electricity cost Cost (€ in 1 year)" );
				annual_change_in_net_income_euro : Optional[ float ] = Field( None , description = "Annual change in Net Income  (€)" );
				annual_roi_percentage : Optional[ str ] = Field( None , description = "Annual ROI (%)" );
				payback_period_years : Optional[ str ] = Field( None , description = "Payback Period (years)" );
				is_the_dat_beneficial : Optional[ str ] = Field( None , description = "Is the DAT Beneficial?" );


class livestock( BaseModel ):
				crop_or_livestock_test_case : Optional[ str ] = Field( None , description = "Type" );
				dats_category : Optional[ str ] = Field( None , description = "DAT category" );
				test_case_number : Optional[ str ] = Field( None , description = "TC Number" );
				tc_name_title : Optional[ str ] = Field( None , description = "TC Name" );
				tc_country : Optional[ str ] = Field( None , description = "TC Country" );
				crop_or_animal_type : Optional[ str ] = Field( None , description = "TC Animal Type" );
				datss_name : Optional[ str ] = Field( None , description = "DAT name" );
				datss_short_description : Optional[ str ] = Field( None , description = "DAT short Description" );
				datss_provider_website : Optional[ str ] = Field( None , description = "DAT provider website" );
				dats_cost_structure_infoi : Optional[ str ] = Field( None , description = "DATS Cost structure info" );
				kpi_info_outcomes_used : Optional[ str ] = Field( None , description = "KPI Info / Outocmes Used" );
				number_of_animals : Optional[ float ] = Field( None , description = "Number of animals" );
				years_of_usage : Optional[ float ] = Field( None , description = "years_of_usage" );
				initial_cost_of_investment_euro : Optional[ float ] = Field( None , description = "initial_cost_of_investment_euro" );
				annual_fee_peryear_euro : Optional[ float ] = Field( None , description = "annual fee/year (€)" );
				maintainance_cost_peryear_euro : Optional[ float ] = Field( None , description = "maintainance cost/year (€)" );
				initial_cost_of_investment_euro_peranimal_cow_for_the_sensor : Optional[ float ] = Field( None , description = "initial cost of investment (€)/animal-cow (for the sensor)" );
				annual_fee_per_animal_for_data_interpretationeuro : Optional[ float ] = Field( None , description = "annual fee per animal for data interpretation(€)" );
				maintainance_cost_per_animal_euro : Optional[ float ] = Field( None , description = "maintainance cost per animal (€)" );
				depreciation_euro_year : Optional[ float ] = Field( None , description = "depreciation_euro_year" );
				total_initial_cost_of_dat_purchase : Optional[ float ] = Field( None , description = "total_initial_cost_of_dat_purchase" );
				meat_productivity_impact_with_dats_usage_percentage : Optional[ float ] = Field( None , description = "meat productivity impact with dats usage  (%)" );
				average_meat_price_euro_per_kg : Optional[ float ] = Field( None , description = "average meat price  (€/ kg)" );
				average_meat_produced_per_year_kg_peryear : Optional[ float ] = Field( None , description = "average meat produced per year (kg/year)" );
				meat_current_revenue_without_dats_euro_in_one_year : Optional[ float ] = Field( None , description = "Meat current revenue without dats (€ in 1 year)" );
				meat_productivity_with_dats_usage_kg_peryear : Optional[ float ] = Field( None , description = "meat productivity with dats usage (kg/year)" );
				meat_price_with_dats_usage_in_one_year_euro : Optional[ float ] = Field( None , description = "meat price with dats usage in one year (€)" );
				meat_revenue_impact_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Meat revenue impact with dats usage (€ in 1 year)" );
				oyster_productivity_impact_with_dats_usage_percentage : Optional[ float ] = Field( None , description = "oyster productivity  impact with dats usage (%)" );
				average_oyster_price_euro_per_kg : Optional[ float ] = Field( None , description = "average oyster price  (€/ kg)" );
				average_oysters_produced_per_year_without_dats_usage_kg_peryear : Optional[ float ] = Field( None , description = "average oysters produced per year without dats usage (kg/year)" );
				oysters_current_revenue_without_dats_euro_in_one_year : Optional[ float ] = Field( None , description = "Oysters current revenue without dats (€ in 1 year)" );
				oysters_productivity_with_dats_usage_kg_peryear : Optional[ float ] = Field( None , description = "oysters productivity with dats usage (kg/year)" );
				oyster_price_with_dats_usage_in_one_year_euro : Optional[ float ] = Field( None , description = "oyster price with dats usage in one year (€)" );
				oysters_revenue_impact_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Oysters revenue impact with dats usage (€ in 1 year)" );
				honey_productivity_impact_with_dats_usage_percentage : Optional[ float ] = Field( None , description = "honey productivity impact with dats usage  (%)" );
				average_honey_price_euro_per_kg : Optional[ float ] = Field( None , description = "average honey price  (€/ kg)" );
				average_honey_produced_per_year_without_dats_usage_kg_peryear : Optional[ float ] = Field( None , description = "average honey produced per year without dats usage (kg/year)" );
				honey_current_revenue_without_dats_euro_in_one_year : Optional[ float ] = Field( None , description = "Honey current revenue without dats (€ in 1 year)" );
				honey_productivity_with_dats_usage_kg_peryear : Optional[ float ] = Field( None , description = "honey productivity with dats usage (kg/year)" );
				honey_price_with_dats_usage_in_one_year_euro : Optional[ float ] = Field( None , description = "honey price with dats usage in one year (€)" );
				honey_revenue_impact_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Honey revenue impact with dats usage (€ in 1 year)" );
				milk_productivity_impact_with_dats_usage_percentage : Optional[ float ] = Field( None , description = "milk productivity impact with dats usage  (%)" );
				average_milk_price_per_liter_euro_per_liter : Optional[ float ] = Field( None , description = "average milk price per liter (€/ liter)" );
				average_liters_of_milk_produced_per_animal_per_day_without_dats_usage_l : Optional[ float ] = Field( None , description = "average liters of milk produced per animal per day without dats usage (l)" );
				milk_current_revenue_without_dats_euro_in_one_year : Optional[ float ] = Field( None , description = "Milk current revenue without dats (€ in 1 year)" );
				average_liters_of_milk_produced_per_animal_per_day_with_dat_s_l : Optional[ float ] = Field( None , description = "average liters of milk produced per animal per day with dat s (l)" );
				price_of_milk_yield_with_dat_s_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "price of milk yield with dat s usage (€ in 1 year)" );
				milk_revenue_impact_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "Milk revenue impact with dats usage (€ in 1 year)" );
				electricity_consumption_impact_with_dat_s_usage_percentage : Optional[ float ] = Field( None , description = "electricity consumption impact with dat s usage (%)" );
				current_electricity_consumption_without_dats_usage_in_kwh : Optional[ float ] = Field( None , description = "current electricity consumption without dats usage (in kwh)" );
				cost_of_electricity_per_kwh_euro : Optional[ float ] = Field( None , description = "cost of electricity per kwh (€)" );
				current_cost_of_electricity_without_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "current  cost of electricity without dats usage (€ in 1 year)" );
				elecricity_cost_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "elecricity cost  with dats usage (€ in 1 year)" );
				working_time_impact_with_dat_s_usage_percentage : Optional[ float ] = Field( None , description = "working time impact with dat s usage (%)" );
				current_labor_cost_without_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "current labor cost without dats usage (€ in 1 year)" );
				labor_cost_with_dat_s_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "labor cost with dat s usage (€ in 1 year)" );
				feed_used_impact_with_dats_usage_percentage : Optional[ float ] = Field( None , description = "feed used impact with dats usage (%)" );
				current_feed_cost_without_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "current feed cost without dats usage (€ in 1 year)" );
				feed_cost_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "feed cost with dats usage (€ in 1 year)" );
				mortality_rate_impact_with_dats_usage_percentage : Optional[ float ] = Field( None , description = "mortality rate impact with dats usage (%)" );
				current_mortality_cost_without_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "current mortality cost without dats usage (€ in 1 year)" );
				mortality_cost_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "mortality cost with dats usage (€ in 1 year)" );
				livestock_fuel_consumption_impact_with_dats_usage_percentage : Optional[ float ] = Field( None , description = "livestock fuel consumption impact with dats usage (%)" );
				current_fuel_cost_without_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "current fuel cost without dats usage (€ in 1 year)" );
				fuel_cost_with_dat_s_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "fuel cost with dat s usage (€ in 1 year)" );
				drug_use_impact_with_dats_usage_percentage : Optional[ float ] = Field( None , description = "drug use impact with dats usage (%)" );
				current_drug_cost_without_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "current drug cost without dats usage (€ in 1 year)" );
				drug_cost_with_dat_s_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "drug cost with dat s usage  (€ in 1 year)" );
				water_consumption_impact_with_dats_usage_percentage : Optional[ float ] = Field( None , description = "water consumption impact with dats usage (%)" );
				current_water_cost_euro_in_one_year : Optional[ float ] = Field( None , description = "current water cost (€ in 1 year)" );
				water_cost_with_dats_usage_euro_in_one_year : Optional[ float ] = Field( None , description = "water cost with dats usage (€ in 1 year)" );
				annual_change_in_net_income_euro : Optional[ float ] = Field( None , description = "annual change in net income  (€)" );
				annual_roi_percentage_ : Optional[ str ] = Field( None , description = "annual roi (%) " );
				payback_period_years : Optional[ str ] = Field( None , description = "payback period (years)" );
				is_the_dat_beneficial : Optional[ str ] = Field( None , description = "is the dat beneficial?" );


