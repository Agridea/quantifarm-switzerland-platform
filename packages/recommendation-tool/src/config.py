import logging
from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from src.models.rdf import ValidatedURIRef
from src.recommendation.algorithms import RecomAlgoType
from src.recommendation.metapath import MetaPath
from src.recommendation.recommender import CompositionTypes


class ToolFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = f"{(record.levelname + ':'):<9}"
        record.name = f"{record.name:<14.14}"
        return super().format(record)


def config_app_logger(logger: logging.Logger) -> None:
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = ToolFormatter(
        fmt="%(levelname)s |%(asctime)s| %(name)s -> %(message)s",
        datefmt="%d/%m %H:%M:%S",
        style="%",
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False
    return


# region:    -- Settings


class SingleGraphSettings(BaseModel):
    name: str
    uri: ValidatedURIRef


class GraphSettings(BaseModel):
    dats: SingleGraphSettings
    dats_translations: SingleGraphSettings
    test_cases: list[SingleGraphSettings]
    testcase_translations: SingleGraphSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    sparql_query_endpoint: str
    port: int = 8000
    default_recom_algo_types: list[tuple[RecomAlgoType, CompositionTypes]] = [
        # HACK: First composition type is set to union, basically creating a union 
        # between an empty list of recommendations and the list of recommendations 
        # from the first algorithm.
        (RecomAlgoType.EXACT_MATCH, "union"),
        # (RecomAlgoType.BY_SOURCE, "set_a"),
        (RecomAlgoType.SUSTAINABILITY_SCORING, "set_a"),
    ]
    country_data_file_path: str = "data/ISO3166-country-code-name.json"
    literals_mapping_file_path: str = "data/literals-mapping.json"
    graphs: GraphSettings
    metapaths: list[MetaPath]

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            JsonConfigSettingsSource(settings_cls, json_file="config/graphs.json"),
            JsonConfigSettingsSource(settings_cls, json_file="config/meta-paths.json"),
        )


@lru_cache
def get_settings():
    return Settings()


# endregion: -- Settings
