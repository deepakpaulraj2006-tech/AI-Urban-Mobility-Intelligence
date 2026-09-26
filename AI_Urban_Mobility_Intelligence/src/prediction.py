import joblib,pandas as pd
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from config.config import MODEL_PATH
from src.train_model import FEATURES
def load_model(): return joblib.load(MODEL_PATH)
def predict_one(model,values):
    x=pd.DataFrame([values])[FEATURES]; pred=model.predict(x)[0]; probs=model.predict_proba(x)[0] if hasattr(model,'predict_proba') else None; return pred,probs
