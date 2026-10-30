from fastapi.testclient import TestClient

from src.app import app
from src.config import Settings, get_settings
from src.models import FarmerProfileEntry, FarmerProfileInfo
from src.recommendation.algorithms import RecomAlgoType

client_without_data = TestClient(app)

TOTAL_NUMBER_OF_DATS_IN_STORE = 537


def test_hello_world():
    response = client_without_data.get("/hello_world/")
    assert response.status_code == 200
    assert response.json() == "Hello, World! App is online!"
    return


def test_initialize_dats_correct_total():
    with TestClient(app) as client:
        response = client.get("/initialize")
        assert response.status_code == 200
        result = response.json()
        assert len(result["recommendation_list"]) == TOTAL_NUMBER_OF_DATS_IN_STORE
        return

        
def test_all_dats_correct_total():
    with TestClient(app) as client:
        response = client.get("/dats/all")
        assert response.status_code == 200
        result = response.json()
        assert len(result["recommendation_list"]) == TOTAL_NUMBER_OF_DATS_IN_STORE
        return


def test_filter_list_not_empty():
    with TestClient(app) as client:
        response = client.get("/filters")
        assert response.status_code == 200
        result = response.json()
        assert result["filter_list"]["benefits"][0]["count"] > 0
        return


def test_no_farmer_profile():
    with TestClient(app) as client:
        response = client.post("/dats/recommend?algorithm_type=exact")
        assert response.status_code == 200
        result = response.json()
        assert len(result["recommendation_list"]) == TOTAL_NUMBER_OF_DATS_IN_STORE

    with TestClient(app) as client:
        response = client.post(
            "/dats/recommend?algorithm_type=exact",
            json={"farmer_profile": {"economic_preference": 0.5}},
        )
        assert response.status_code == 200
        result = response.json()
        assert len(result["recommendation_list"]) == TOTAL_NUMBER_OF_DATS_IN_STORE


def test_empty_farmer_profile():
    with TestClient(app) as client:
        response = client.post("/dats/recommend", json={})
        assert response.status_code == 200
        result = response.json()
        assert len(result["recommendation_list"]) == TOTAL_NUMBER_OF_DATS_IN_STORE
        return


def test_recommendation_only_country():
    with TestClient(app) as client:
        data = {
            "farmer_profile": FarmerProfileInfo(
                country=FarmerProfileEntry(value="Germany", requireExactMatch=True)
            ).model_dump()
        }
        response = client.post("/dats/recommend", json=data)
        assert response.status_code == 200
        result = response.json()
        assert len(result["recommendation_list"]) > 0
        assert (
            "Germany"
            in result["recommendation_list"][0]["filterable_properties"]["countries"]
        )
        return


def test_recommendation_complex_profile_A():
    with TestClient(app) as client:
        profile = FarmerProfileInfo(
            country=FarmerProfileEntry(value="Ireland", requireExactMatch=True),
            functionalities=[
                FarmerProfileEntry(value="Strategic planning", requireExactMatch=True),
                FarmerProfileEntry(
                    value="Finance and budgeting", requireExactMatch=True
                ),
            ],
            digital_forms=FarmerProfileEntry(
                value="Computer software", requireExactMatch=True
            ),
        ).model_dump()
        data = {"farmer_profile": profile, "algorithm_type": "exact"}
        response = client.post("/dats/recommend", json=data)
        assert response.status_code == 200
        result = response.json()
        assert len(result["recommendation_list"]) > 0

        data = {"farmer_profile": profile, "algorithm_type": "metapath"}
        response = client.post("/dats/recommend", json=data)
        assert response.status_code == 200
        result = response.json()
        assert len(result["recommendation_list"]) > 0
        return


def test_recommendation_complex_profile_B():
    with TestClient(app) as client:
        profile = FarmerProfileInfo(
            farm_type=FarmerProfileEntry(value="Arable farm", requireExactMatch=False),
            country=FarmerProfileEntry(value="France", requireExactMatch=True),
            functionalities=[
                FarmerProfileEntry(value="Strategic planning", requireExactMatch=True),
                FarmerProfileEntry(
                    value="Finance and budgeting", requireExactMatch=True
                ),
            ],
            benefits=[
                FarmerProfileEntry(
                    value="Optimization of resources use", requireExactMatch=True
                )
            ],
        ).model_dump()
        data = {"farmer_profile": profile, "algorithm_type": "exact"}
        response = client.post("/dats/recommend", json=data)
        assert response.status_code == 200
        result = response.json()
        assert len(result["recommendation_list"]) > 0

        data = {"farmer_profile": profile, "algorithm_type": "metapath"}
        response = client.post("/dats/recommend", json=data)
        assert response.status_code == 200
        result = response.json()
        assert len(result["recommendation_list"]) > 0
        return


def test_recommendation_complex_profile_C():
    with TestClient(app) as client:
        profile = FarmerProfileInfo(
            farm_type=FarmerProfileEntry(value="Egg farm", requireExactMatch=True),
            country=FarmerProfileEntry(value="Belgium", requireExactMatch=True),
            functionalities=[
                FarmerProfileEntry(value="Harvest prediction", requireExactMatch=True)
            ],
            benefits=[
                FarmerProfileEntry(
                    value="Optimization of resources use", requireExactMatch=True
                )
            ],
        ).model_dump()
        data = {"farmer_profile": profile, "algorithm_type": "exact"}
        response = client.post("/dats/recommend", json=data)
        assert response.status_code == 200
        result = response.json()
        assert len(result["recommendation_list"]) > 0

        data = {"farmer_profile": profile, "algorithm_type": "metapath"}
        response = client.post("/dats/recommend", json=data)
        assert response.status_code == 200
        result = response.json()
        assert len(result["recommendation_list"]) > 0
        return


def test_dats_main_by_name():
    with TestClient(app) as client:
        response = client.get(url="/dats/main?dats_name=CowVisiom")
        assert response.status_code == 200
        result = response.json()
        assert result["dats_info"]["description"]["name"] == "CowVisiom"
        return


def test_dats_main_no_test_case():
    with TestClient(app) as client:
        response = client.get(
            url="/dats/main?dats_uri=https%3A%2F%2Fquantifarm.eu%2Fdata%2Fdats%2Fbodemidee"
        )
        assert response.status_code == 200
        result = response.json()
        assert result["dats_info"]["description"]["name"] == "BodemIDee"
        assert len(result["test_cases"]) == 0
        return


def test_dats_main_with_test_case():
    with TestClient(app) as client:
        response = client.get(
            url="/dats/main/?dats_uri=https%3A%2F%2Fquantifarm.eu%2Fdata%2Fdats%2Fkathari_uf1"
        )
        assert response.status_code == 200
        result = response.json()
        assert result["dats_info"]["description"]["name"] == "Kathari UF1"
        assert len(result["test_cases"]) > 0
        assert len(result["test_cases"][0]["assessments"]) > 0
        return


def test_recommendation_sustainability_radix():
    def settings_override() -> Settings:
        return Settings(
            default_recom_algo_types=[(RecomAlgoType.SUSTAINABILITY_RADIX, "union")]
        )

    app.dependency_overrides[get_settings] = settings_override

    data = {
        "farmer_profile": FarmerProfileInfo(
            country=FarmerProfileEntry(value="Greece", requireExactMatch=True),
            environmental_preference=0.2,
            social_preference=0.4,
            economic_preference=1.0,
        ).model_dump()
    }

    with TestClient(app) as client:
        response = client.post("/dats/recommend", json=data)
        assert response.status_code == 200
        result = response.json()
        assert len(result["recommendation_list"][0]["description"]["test_cases"]) > 0

    app.dependency_overrides[get_settings] = get_settings
    return


def test_recommendation_sustainability_scoring():
    def settings_override() -> Settings:
        return Settings(
            default_recom_algo_types=[(RecomAlgoType.SUSTAINABILITY_SCORING, "union")]
        )

    app.dependency_overrides[get_settings] = settings_override

    data = {
        "farmer_profile": FarmerProfileInfo(
            country=FarmerProfileEntry(value="Greece", requireExactMatch=True),
            environmental_preference=1.0,
            social_preference=0.4,
            economic_preference=0.2,
        ).model_dump()
    }

    with TestClient(app) as client:
        response = client.post("/dats/recommend", json=data)
        assert response.status_code == 200
        result = response.json()
        assert len(result["recommendation_list"][0]["description"]["test_cases"]) > 0

    app.dependency_overrides[get_settings] = get_settings
    return
