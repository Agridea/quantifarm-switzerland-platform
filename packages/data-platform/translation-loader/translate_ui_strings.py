"""One-off utility: translate a fixed list of toolkit-dashboard UI strings (labels,
placeholders, section headers, result descriptions - mostly from tool2.html, the
Cost & Benefit Calculators) into de-CH/fr/it via DeepL, and print a ready-to-paste
JS dictionary object (packages/toolkit-dashboard/js/uistrings.js style).

This is a one-time content-generation helper, not part of the regular data
pipeline - unlike translation-loader, it doesn't touch the triple store at all.

Usage:
    DEEPL_API_KEY=... python translate_ui_strings.py > output.js
"""

import json
import os
import sys
import time

import deepl

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
_DEEPL_TARGET_LANG = {"de": "DE-CH", "fr": "FR", "it": "IT"}
_MAX_TEXTS_PER_REQUEST = 50

# Deduplicated English source strings from tool2.html / tool2.js. Some contain
# embedded "<br>" - these are used with .innerHTML in the frontend, so DeepL
# translates the surrounding text while these HTML tags are preserved as literal
# text within the string DeepL sees (harmless: DeepL leaves untranslatable inline
# markup mostly untouched, and we verify the count of "<br>" occurrences matches
# afterwards).
STRINGS = [
    # Headers / titles
    "Cost and Benefit Calculators", "Login needed", "Search", "Description",
    "DATSs for Crop Farming", "DATSs for Livestock Farming",
    "Test Cases' DATSs for Crop Farming", "Test Cases' DATSs for Livestock Farming",
    "Crop Calculator Modules", "Livestock Calculator Modules",
    "Crop Calculator Modules based on Test Cases' data",
    "Livestock Calculator Modules based on Test Cases' data",
    "Recalculate", "INVESTMENT COST", "YIELD", "FERTILIZER USE", "WATER USE",
    "PESTICIDE USE", "LABOR COST", "FUEL COST", "INVESTMENT DECISION",
    "MILK YIELD", "ENERGY COST", "PROFIT PER ANIMAL", "FEED COST",
    "FEED WASTE COST", "ANTIBIOTICS COST", "MORTALITY COST", "PROFITABILITY",
    "WORKING TIME COST", "ELECTRICITY COST", "MEAT PRODUCTIVITY", "OYSTER",
    "HONEY", "Parameters", "Result", "DATSs for Crop", "DATSs for Livestock",
    # Dropdown options
    "Arable", "Fruits", "Vineyards", "Vegetables", "Orchards", "Cattle", "Pigs",
    "Poultry", "Small Ruminants",
    # Labels / placeholders
    "Years of usage", "Total area (ha)", "Number of Units (sensors etc.)",
    "Current yield (tons/ha)", "Market price (CHF/ton)",
    "Fertilizer usage (kg/ha)", "Fertilizer cost (CHF/kg)",
    "Water usage (m3/ha)", "Water cost (CHF/m3)",
    "Pesticide usage (kg or lt/ha)", "Pesticide cost (CHF/kg or lt)",
    "Labor cost (CHF/year)", "Fuel cost (CHF/year)", "Number of animals",
    "Average milk price (CHF/l)", "Average liters of milk per cow per day (l)",
    "Labor Cost (CHF in 1 year)", "Energy Consumption (kWh)",
    "Cost of Energy per kWh (CHF)", "Water Cost (CHF in 1 year)",
    "Feed Cost (CHF in 1 year)", "Feed Waste Cost (CHF in 1 year)",
    "Antibiotics Cost (CHF in 1 year)", "Mortality Cost (CHF in 1 year)",
    "Current Profitability (CHF in 1 year)", "Working Time Cost (CHF/year)",
    "Electricity cost (CHF/year)", "Average meat price per kg",
    "Average meat produced per year (kg/year)", "Average oyster price (CHF/kg)",
    "Oysters produced per year (kg/year)", "Average honey price (CHF/kg)",
    "Honey produced per year (kg/year)", "Cost of Electricity per kWh (CHF)",
    # Result descriptions (some with embedded <br>)
    "Total Initial cost of DATS Purchase (CHF)<br>Includes purchase price, installation or setup costs, and any other INITIAL expenses.",
    "Maintainance Costs (CHF/year)",
    "Depreciation (CHF/year)<br>(i.e. the annual reduction in the intial value of a tangible fixed asset)",
    "Current revenue (CHF in 1 year)", "Increased yield (tons/ha)",
    "Price of increased yield (CHF/ha)", "Increased revenue (CHF in 1 year)",
    "Current fertilization cost (CHF/ha)", "Reduced fertilizer usage (kg/ha)",
    "Fertilizer cost savings (CHF/ha)", "Fertilization cost savings (CHF in 1 year)",
    "Current irrigation cost (CHF/ha)", "Reduced water usage (m3/ha)",
    "Water cost savings (CHF/ha)", "Water cost savings (CHF in 1 year)",
    "Current pesticide cost (CHF/ha)", "Reduced pesticide usage (kg or lt/ha)",
    "Pesticide cost savings (CHF/ha)", "Pesticide cost savings (CHF in 1 year)",
    "Labor cost savings (CHF in 1 year)", "Fuel cost savings (CHF in 1 year)",
    "Annual change in Net Income  (CHF)<br>This shows how much more or less money you earn each year after using the equipment.<br>(annual total Impact (including addtional annual OPEX [e.g., Subscriptions, Maintenance,etc.]) with DATS usage",
    "Annual ROI (%)<br>The net change in your income per year as a percentage of the equipment's initial cost.<br>(Annual change in Net Income / initial cost of the equipment) ",
    "Payback Period (years)<br>How many years it will take to earn back the money you spent on the equipment.<br>(N/A means that the investment does not recover its cost under current conditions)",
    "Is the DAT Beneficial?<br>(6 year payback period threshold) ",
    "Price of Milk Yield in one year (CHF)",
    "Price of Increased Milk Yield in one year (CHF)",
    "Increased Revenue (CHF in 1 year)", "Labor cost saving (CHF in 1 year)",
    "Cost of Energy (CHF in 1 year)", "Energy Cost Savings (CHF in 1 year)",
    "Water Cost Saving (CHF in 1 year)",
    "Profit per Animal Increase in 1 year (CHF)",
    "Feed Cost Saving (CHF in 1 year)", "Feed Waste Cost Saving (CHF in 1 year)",
    "Antibiotics Cost Saving (CHF in 1 year)",
    "Mortality Cost Saving (CHF in 1 year)", "Profit Increase in 1 year (CHF)",
    "Current revenue without DATS usage (CHF in 1 year)",
    "Yield with DATS usage (tons/ha)", "Price of Yield with DATS usage (CHF/ha)",
    "Revenue Impact with DATS usage (CHF in 1 year)",
    "Current Fertilization Cost without DATS usage (CHF/ha)",
    "Fertilizer usage with DATS (kg/ha)",
    "Fertilizer Cost with DATS usage (CHF/ha)",
    "Fertilization Cost with DATS usage (CHF in 1 year)",
    "Current Irrigation Cost without DATS usage (CHF/ha)",
    "Water usage with DATS (m3/ha)", "Water Cost with DATS usage (CHF/ha)",
    "Water Cost with DATS usage (CHF in 1 year)",
    "Current pesticide cost without DATS  usage (CHF/ha)",
    "Pesticide usage with DATS (kg or lt/ha)",
    "Pesticide Cost with DATS usage (CHF/ha)",
    "Pesticide Cost with DATS usage (CHF in 1 year)",
    "Working Time Cost with DATS usage (CHF/year)",
    "Fuel cost with DATS usage (CHF/year)",
    "Electricity cost with DATS usage (CHF/year)",
    "Current Revenue without DATS (CHF in 1 year)",
    "Meat Productivity with DATS usage (kg/year)",
    "Meat price with DATS usage in one year (CHF)",
    "Oysters Productivity with DATS usage (kg/year)",
    "Oyster price with DATS usage in one year (CHF)",
    "Honey Productivity with DATS usage (kg/year)",
    "Honey price with DATS usage in one year (CHF)",
    "Average liters of milk produced per animal per day with DATS (l)",
    "Price of Milk Yield with DATS usage (CHF in 1 year)",
    "Labor cost with DATS usage (CHF in 1 year)",
    "Cost of Electricity without DATS usage (CHF in 1 year)",
    "Elecricity Cost  with DATS usage (CHF in 1 year)",
    "Feed Cost with DATS usage (CHF in 1 year)",
    "Fuel cost with DATS usage (CHF in 1 year)",
    "Drug Cost with DAT S usage  (CHF in 1 year)",
    "Mortality Cost with DATS usage (CHF in 1 year)",
    # tool2.js hardcoded result strings
    "YES", "NO", "DATS is free", "N/A",
]


def main() -> None:
    if not DEEPL_API_KEY:
        print("DEEPL_API_KEY is not set", file=sys.stderr)
        sys.exit(1)

    unique_strings = list(dict.fromkeys(STRINGS))
    translator = deepl.Translator(DEEPL_API_KEY)

    result: dict[str, dict[str, str]] = {}
    for lang, target in _DEEPL_TARGET_LANG.items():
        translated: dict[str, str] = {}
        for i in range(0, len(unique_strings), _MAX_TEXTS_PER_REQUEST):
            chunk = unique_strings[i : i + _MAX_TEXTS_PER_REQUEST]
            for attempt in range(5):
                try:
                    results = translator.translate_text(chunk, target_lang=target)
                    break
                except Exception as e:
                    print(f"attempt {attempt} failed: {e}", file=sys.stderr)
                    time.sleep(3 * (attempt + 1))
            else:
                raise RuntimeError(f"Giving up on chunk starting at {i} for {lang}")
            for source, res in zip(chunk, results):
                translated[source] = res.text
        result[lang.upper()] = translated

    print("const costBenefitStrings = " + json.dumps(result, indent=4, ensure_ascii=False) + ";")


if __name__ == "__main__":
    main()
