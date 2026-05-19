import os

SERVICE_NAME = "Tech Challenge 4"
VERSION = "1.0.0"
DESCRIPTION = "LSTM model disney close price prediction"

USE_REDIS = os.getenv("USE_REDIS", "False").lower() == "true"
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_USER = os.getenv("REDIS_USER", "")
REDIS_PASS = os.getenv("REDIS_PASS", "")

MODEL_PATH = os.getenv("MODEL_PATH", "/app/SavedModels/model.pth")
X_SCALER_PATH = os.getenv("X_SCALER_PATH", "/app/SavedModels/scaler_x.pkl")
Y_SCALER_PATH = os.getenv("Y_SCALER_PATH", "/app/SavedModels/scaler_y.pkl")

REDIS_PREFIX = ""
if REDIS_USER != "" and REDIS_PASS != "":
    REDIS_PREFIX = f"{REDIS_USER}:{REDIS_PASS}@"
elif REDIS_PASS != "":
    REDIS_PREFIX = f"{REDIS_PASS}@"

REDIS_URL = f"redis://{REDIS_PREFIX}{REDIS_HOST}:{REDIS_PORT}"