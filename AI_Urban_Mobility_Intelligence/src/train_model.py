import json,joblib,pandas as pd
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from config.config import PROCESSED_DATA,MODEL_PATH,METADATA_PATH,RANDOM_STATE
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
FEATURES=['location','road_type','road_capacity','vehicle_count','average_speed','traffic_density','occupancy_rate','weather_condition','day_of_week','temperature','rainfall','visibility','accident_count','hour']; TARGET='congestion_level'; CAT=['location','road_type','weather_condition','day_of_week']; NUM=[x for x in FEATURES if x not in CAT]
def train():
    if not PROCESSED_DATA.exists():
        from src.data_generation import generate_data; from src.data_cleaning import clean_data; generate_data(); d=clean_data(pd.read_csv(ROOT/'data/raw/traffic_raw.csv')); PROCESSED_DATA.parent.mkdir(exist_ok=True,parents=True); d.to_csv(PROCESSED_DATA,index=False)
    df=pd.read_csv(PROCESSED_DATA); Xtr,Xte,ytr,yte=train_test_split(df[FEATURES],df[TARGET],test_size=.2,stratify=df[TARGET],random_state=RANDOM_STATE)
    def pipe(model):
        pre=ColumnTransformer([('num',Pipeline([('imp',SimpleImputer(strategy='median')),('scale',StandardScaler())]),NUM),('cat',Pipeline([('imp',SimpleImputer(strategy='most_frequent')),('ohe',OneHotEncoder(handle_unknown='ignore'))]),CAT)])
        return Pipeline([('preprocessor',pre),('model',model)])
    models={'Logistic Regression':LogisticRegression(max_iter=1500,random_state=RANDOM_STATE),'Decision Tree':DecisionTreeClassifier(max_depth=8,min_samples_leaf=5,random_state=RANDOM_STATE),'Random Forest':RandomForestClassifier(n_estimators=250,max_depth=12,min_samples_leaf=3,n_jobs=-1,random_state=RANDOM_STATE)}
    results={}; fitted={}
    for name,m in models.items():
        p=pipe(m); p.fit(Xtr,ytr); pred=p.predict(Xte); results[name]={'accuracy':accuracy_score(yte,pred),'precision':precision_score(yte,pred,average='weighted',zero_division=0),'recall':recall_score(yte,pred,average='weighted',zero_division=0),'f1':f1_score(yte,pred,average='weighted',zero_division=0),'confusion_matrix':confusion_matrix(yte,pred,labels=['Low','Medium','High']).tolist()}; fitted[name]=p
    selected=max(results,key=lambda k:(results[k]['f1'],results[k]['accuracy'])); selected_pipe=fitted[selected]; MODEL_PATH.parent.mkdir(parents=True,exist_ok=True); joblib.dump(selected_pipe,MODEL_PATH)
    perm=permutation_importance(selected_pipe,Xte,yte,n_repeats=3,random_state=RANDOM_STATE,scoring='f1_weighted',n_jobs=-1)
    importance={f:float(v) for f,v in zip(FEATURES,perm.importances_mean)}
    meta={'selected_model':selected,'features':FEATURES,'target':TARGET,'classes':['Low','Medium','High'],'metrics':results,'feature_importance':importance,'selection_rule':'Highest weighted F1; accuracy used as secondary criterion.','random_state':RANDOM_STATE}; METADATA_PATH.write_text(json.dumps(meta,indent=2)); return meta
if __name__=='__main__': print(json.dumps(train(),indent=2))
