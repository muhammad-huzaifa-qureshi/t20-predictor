"""Constants and model specifications for T20 prediction models."""

MODEL_RANGES = {
    "batting": {
        "balls": {"min": 1, "max": 100},
        "fours": {"min": 0, "max": 25},
        "sixes": {"min": 0, "max": 25},
        "strike_rate": {"min": 0.0, "max": 500.0},
    },
    "bowling": {
        "fours": {"min": 0, "max": 16},
        "sixes": {"min": 0, "max": 12},
        "balls": {"min": 1, "max": 24},
        "economy": {"min": 0.0, "max": 36.0},
    },
    "win": {
        "target": {"min": 40, "max": 400},
        "score": {"min": 0, "max": 350},
        "wickets": {"min": 0, "max": 9},
        "balls_bowled": {"min": 0, "max": 119},
    },
}

# API field -> (training column name, minimum, maximum).
# The order inside each "inputs" dict must match the training column order.
SPECS = {
    "batting": {
        "file": "batting_model.json",
        "target": "Runs",
        "inputs": {
            "balls": ("Balls", MODEL_RANGES["batting"]["balls"]["min"], MODEL_RANGES["batting"]["balls"]["max"]),
            "fours": ("Fours", MODEL_RANGES["batting"]["fours"]["min"], MODEL_RANGES["batting"]["fours"]["max"]),
            "sixes": ("Sixes", MODEL_RANGES["batting"]["sixes"]["min"], MODEL_RANGES["batting"]["sixes"]["max"]),
            "strike_rate": (
                "Strike Rate",
                MODEL_RANGES["batting"]["strike_rate"]["min"],
                MODEL_RANGES["batting"]["strike_rate"]["max"],
            ),
        },
    },
    "bowling": {
        "file": "bowling_model.json",
        "target": "Conceded",
        "inputs": {
            "fours": ("Fours", MODEL_RANGES["bowling"]["fours"]["min"], MODEL_RANGES["bowling"]["fours"]["max"]),
            "sixes": ("Sixers", MODEL_RANGES["bowling"]["sixes"]["min"], MODEL_RANGES["bowling"]["sixes"]["max"]),
            "balls": ("Balls", MODEL_RANGES["bowling"]["balls"]["min"], MODEL_RANGES["bowling"]["balls"]["max"]),
            "economy": (
                "Economy",
                MODEL_RANGES["bowling"]["economy"]["min"],
                MODEL_RANGES["bowling"]["economy"]["max"],
            ),
        },
    },
    "win": {
        "file": "win_model.json",
        "target": "Win probability",
        "task": "classifier",
        "unit": "%",
        "inputs": {
            "target": ("Target Score", MODEL_RANGES["win"]["target"]["min"], MODEL_RANGES["win"]["target"]["max"]),
            "score": ("Innings Runs", MODEL_RANGES["win"]["score"]["min"], MODEL_RANGES["win"]["score"]["max"]),
            "wickets": ("Innings Wickets", MODEL_RANGES["win"]["wickets"]["min"], MODEL_RANGES["win"]["wickets"]["max"]),
            "balls_bowled": (
                "Balls Bowled",
                MODEL_RANGES["win"]["balls_bowled"]["min"],
                MODEL_RANGES["win"]["balls_bowled"]["max"],
            ),
        },
    },
}
