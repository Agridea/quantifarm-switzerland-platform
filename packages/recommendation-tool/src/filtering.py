import re

from src.models import *
from src.data_sources import DATSGraphClient


def apply_property_filters(recommendation_list: list[DAT], selected_filters: SelectedFilters) -> list[DAT]:
    if not selected_filters:
        return recommendation_list

    new: list[DAT] = list()
    for dat in recommendation_list:
        # AND logic: DAT must match all non-empty filter categories (OR within each category)
        if all([not set(filt).isdisjoint(prop or []) for (_, filt), (_, prop) in zip(selected_filters, dat.filterable_properties) if filt]):
            new.append(dat)
    return new


def apply_searchbar_filter(recommendation_list: list[DAT], search_bar_filter: SearchBarFilter) -> list[DAT]:
    if not search_bar_filter:
        return recommendation_list

    terms = [t.strip().casefold() for t in re.split(r"[,;]", search_bar_filter.query_string) if t.strip()]
    if not terms:
        return recommendation_list

    def term_matches(dat: DAT, term: str) -> bool:
        return (search_bar_filter.search_title and term in dat.description.title.casefold()) or \
               (search_bar_filter.search_description and term in dat.description.description.casefold()) or \
               (search_bar_filter.search_keywords and any(term in keyword.casefold() for keyword in dat.description.keywords))

    # AND across comma/semicolon-separated terms; each term may match any enabled field
    return [dat for dat in recommendation_list if all(term_matches(dat, t) for t in terms)]


def create_filter_list(dat_graph: DATSGraphClient) -> FiltersCount:
    filter_list = FiltersCount()
    all_dats = [dat_graph.to_dat_model(node) for node in dat_graph.all_dats_nodes]
    for dat in all_dats:
        for (_, filt), (_, prop) in zip(filter_list, dat.filterable_properties):
            filt: list[OptionCount]
            prop: list[str]
            for prop_option in prop:
                if prop_option not in [opt.option for opt in filt]:
                    filt.append(OptionCount(option=prop_option, count=1))
                    continue
                for filt_option in filt:
                    if filt_option.option == prop_option:
                        filt_option.count += 1
    return filter_list


def update_filter_list(recommendation_list: list[DAT] = list(), filters_count: FiltersCount = FiltersCount()) -> FiltersCount:
    # Reset counter for each option
    for _, filter in filters_count:
        filter: list[OptionCount]
        for option in filter:
            option.count = 0

    for dat in recommendation_list:
        for (_, filt), (_, prop) in zip(filters_count, dat.filterable_properties):
            filt: list[OptionCount]
            prop: list[str]
            for option in filt:
                if option.option in prop:
                    option.count += 1

    return filters_count


# def update_match(recommended_list: RecommendationList, farmer_profile: FarmerProfileInfo):
#     if not farmer_profile or not recommended_list.items:
#         return recommended_list
#     for item in recommended_list.items:
#         if farmer_profile.farm_type:
#             for x in item.info.agricultural_sectors:
#                 x.match = (x.item == farmer_profile.farm_type.value or x.item in farmer_profile.farm_type.value)

#         if farmer_profile.country:
#             for x in item.info.countries:
#                 x.match = (x.item == farmer_profile.country.value or x.item in farmer_profile.country.value)

#         if farmer_profile.language:
#             for x in item.info.languages:
#                 x.match = (x.item == farmer_profile.language.value or x.item in farmer_profile.language.value)

#     return recommended_list

