from pathlib import Path
import pandas as pd

def load_matches():

    base_path = Path(__file__).resolve().parent.parent
    path = base_path / "data" / "raw" / "allsvenskan.csv"

    matches = pd.read_csv(path)

    return matches