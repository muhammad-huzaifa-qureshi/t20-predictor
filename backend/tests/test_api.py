import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app  # noqa: E402

client = app.test_client()

BATTING = {
    "balls": 20,
    "fours": 3,
    "sixes": 2,
    "strike_rate": 150,
}

BOWLING = {
    "fours": 3,
    "sixes": 1,
    "balls": 24,
    "economy": 8,
}

WIN = {"target": 180, "score": 95, "wickets": 2, "balls_bowled": 66}



def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_batting_prediction():
    response = client.post("/predict/batting", json=BATTING)

    assert response.status_code == 200

    body = response.get_json()

    assert body["target"] == "Runs"
    assert 20 <= body["prediction"] <= 40


def test_bowling_prediction():
    response = client.post("/predict/bowling", json=BOWLING)

    assert response.status_code == 200

    body = response.get_json()

    assert body["target"] == "Conceded"
    assert 24 <= body["prediction"] <= 40


def test_missing_field_returns_400():
    payload = dict(BATTING)
    payload.pop("balls")

    response = client.post("/predict/batting", json=payload)

    assert response.status_code == 400


def test_out_of_range_returns_400():
    response = client.post(
        "/predict/batting",
        json={**BATTING, "balls": 0},
    )

    assert response.status_code == 400


def test_unknown_model_returns_404():
    response = client.post("/predict/fielding", json=BATTING)

    assert response.status_code == 404

def test_win_prediction_and_explanation():
    response = client.post("/predict/win", json=WIN)
    assert response.status_code == 200
    body = response.get_json()
    assert body["unit"] == "%"
    assert 0 <= body["prediction"] <= 100
    # base value plus the contributions rebuilds the prediction (rounding allowed)
    total = body["base"] + sum(c["value"] for c in body["contributions"])
    assert abs(total - body["prediction"]) < 0.5


def test_win_score_at_target_returns_400():
    response = client.post("/predict/win", json={**WIN, "score": 180})
    assert response.status_code == 400
