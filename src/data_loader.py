
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

FILES = {
    "orders": "orders.csv",
    "products": "products.csv",
    "customers": "customer_behavior.csv",
    "campaigns": "marketing_campaigns.csv",
    "returns": "returns.csv",
    "delivery": "delivery (1).csv",
}

def load_data(data_dir=DATA_DIR):
    data_dir = Path(data_dir)
    return {k: pd.read_csv(data_dir / f) for k, f in FILES.items()}
