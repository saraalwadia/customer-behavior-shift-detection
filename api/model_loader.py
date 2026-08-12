from pathlib import Path
import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "xgboost"
    / "v1"
    / "model.joblib"
)


def load_model():
    """Load the versioned XGBoost model."""
    return joblib.load(MODEL_PATH)