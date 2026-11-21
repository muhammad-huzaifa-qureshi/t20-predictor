"""Flask API that serves the batting, bowling and win probability XGBoost models."""

import math
from pathlib import Path

import pandas as pd
import xgboost as xgb
from flask import Flask, jsonify, request
from xgboost import XGBClassifier, XGBRegressor



MODEL_DIR = Path(__file__).resolve().parent / "models"

# API field -> (training column name, minimum, maximum).
# The order inside each "inputs" dict must match the training column order.
SPECS = {
    "batting": {
        "file": "batting_model.json",
        "target": "Runs",
        "inputs": {
            "balls": ("Balls", 1, 120),
            "fours": ("Fours", 0, 60),
            "sixes": ("Sixes", 0, 60),
            "strike_rate": ("Strike Rate", 0, 720),
        },
    },
    "bowling": {
        "file": "bowling_model.json",
        "target": "Conceded",
        "inputs": {
            "fours": ("Fours", 0, 24),
            "sixes": ("Sixers", 0, 24),
            "balls": ("Balls", 1, 24),
            "economy": ("Economy", 0, 60),
        },
    },
    # Chase win probability. The four inputs are turned into the five model
    # features by chase_features() below. "task" and "unit" are optional and
    # default to a regressor measured in runs.
    "win": {
        "file": "win_model.json",
        "target": "Win probability",
        "task": "classifier",
        "unit": "%",
        "inputs": {
            "target": ("Target Score", 1, 350),
            "score": ("Innings Runs", 0, 349),
            "wickets": ("Innings Wickets", 0, 9),
            "balls_bowled": ("Balls Bowled", 0, 119),
        },
    },
}



def chase_features(row):
    # Must stay identical to make_features() in the notebook.
    runs_needed = row["Target Score"] - row["Innings Runs"]
    balls_left = 120 - row["Balls Bowled"]
    balls_bowled = row["Balls Bowled"]
    return {
        "Runs Needed": runs_needed,
        "Balls Remaining": balls_left,
        "Wickets In Hand": 10 - row["Innings Wickets"],
        "Current Run Rate": row["Innings Runs"] * 6 / balls_bowled if balls_bowled > 0 else 0.0,
        "Required Run Rate": runs_needed * 6 / max(balls_left, 1),
    }


def load_models():
    models = {}
    for name, spec in SPECS.items():
        model = XGBClassifier() if spec.get("task") == "classifier" else XGBRegressor()
        model.load_model(str(MODEL_DIR / spec["file"]))
        models[name] = model
    return models


def explain(model, frame, task):
    # XGBoost returns SHAP values itself: one per feature, plus the base value last.
    raw = model.get_booster().predict(xgb.DMatrix(frame), pred_contribs=True)[0]
    values, bias = [float(v) for v in raw[:-1]], float(raw[-1])

    if task == "classifier":
        # Raw values are in log odds. Rescale them into win probability points.
        sigmoid = lambda z: 1 / (1 + math.exp(-z))
        total = sum(values)
        p, base = sigmoid(bias + total), sigmoid(bias)
        scale = (p - base) / total if abs(total) > 1e-9 else p * (1 - p)
        values = [v * scale * 100 for v in values]
        bias = base * 100

    contributions = [
        {"label": name, "input": round(float(frame[name].iloc[0]), 2), "value": round(v, 1) + 0.0}
        for name, v in zip(frame.columns, values)
    ]
    contributions.sort(key=lambda c: abs(c["value"]), reverse=True)
    return round(bias, 1), contributions



MODELS = load_models()

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok", models=list(SPECS))


@app.post("/predict/<kind>")
def predict(kind):
    spec = SPECS.get(kind)

    if spec is None:
        return jsonify(error=f"Unknown model '{kind}'"), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="Expected a JSON object"), 400

    inputs = spec["inputs"]

    missing = [key for key in inputs if key not in data]
    extra = [key for key in data if key not in inputs]

    if missing or extra:
        return jsonify(
            error="Input mismatch",
            missing=missing,
            extra=extra,
        ), 400

    row = {}

    for key, (column, low, high) in inputs.items():
        value = data[key]

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return jsonify(error=f"'{key}' must be a number"), 400

        if not low <= value <= high:
            return jsonify(
                error=f"'{key}' must be between {low} and {high}"
            ), 400

        row[column] = float(value)

    task = spec.get("task", "regressor")
    if kind == "win":
        if row["Innings Runs"] >= row["Target Score"]:
            return jsonify(error="'score' must be below the target"), 400
        row = chase_features(row)

    frame = pd.DataFrame([row])
    model = MODELS[kind]
    if task == "classifier":
        prediction = float(model.predict_proba(frame)[0][1]) * 100
    else:
        prediction = max(float(model.predict(frame)[0]), 0.0)

    base, contributions = explain(model, frame, task)
    return jsonify(
        model=kind,
        target=spec["target"],
        prediction=round(prediction, 1),
        unit=spec.get("unit", "runs"),
        base=base,
        contributions=contributions,
    )



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)