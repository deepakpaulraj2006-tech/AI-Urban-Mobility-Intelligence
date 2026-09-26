from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DATA = ROOT_DIR/'data/raw/traffic_raw.csv'
PROCESSED_DATA = ROOT_DIR/'data/processed/traffic_cleaned.csv'
MODEL_PATH = ROOT_DIR/'models/congestion_model.pkl'
METADATA_PATH = ROOT_DIR/'models/model_metadata.json'
RANDOM_STATE = 42
N_RECORDS = 15000
LOCATIONS = {
    'Central Junction': (13.0827,80.2707), 'Airport Road': (13.0102,80.2150),
    'Tech Park Road': (13.0378,80.2341), 'Market Street': (13.0878,80.2785),
    'Railway Station Road': (13.0820,80.2750), 'University Road': (13.0105,80.2350),
    'Industrial Area': (13.0900,80.2000), 'Hospital Junction': (13.0600,80.2500),
    'Bus Stand Road': (13.0750,80.2600), 'Ring Road': (13.0300,80.1800),
}
CONGESTION_CLASSES=['Low','Medium','High']
