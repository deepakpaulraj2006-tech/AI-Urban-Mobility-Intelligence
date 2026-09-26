import numpy as np, pandas as pd
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from config.config import RAW_DATA, RANDOM_STATE, N_RECORDS, LOCATIONS

def generate_data(n=N_RECORDS, seed=RANDOM_STATE):
    rng=np.random.default_rng(seed)
    ts=pd.Series(pd.Timestamp('2025-01-01')+pd.to_timedelta(rng.integers(0,90*24*60,n),unit='m')).sort_values().reset_index(drop=True)
    location=rng.choice(list(LOCATIONS),n)
    road_map={'Central Junction':'Junction','Airport Road':'Highway','Tech Park Road':'Main Road','Market Street':'Main Road','Railway Station Road':'Main Road','University Road':'Residential Road','Industrial Area':'Industrial Road','Hospital Junction':'Junction','Bus Stand Road':'Main Road','Ring Road':'Highway'}
    cap_map={'Highway':1800,'Main Road':1300,'Junction':1000,'Industrial Road':1200,'Residential Road':700}
    road_type=np.array([road_map[x] for x in location]); capacity=np.array([cap_map[x] for x in road_type],float)
    hour=ts.dt.hour.to_numpy(); dow=ts.dt.dayofweek.to_numpy(); weekend=dow>=5
    peak=((hour>=7)&(hour<=10))|((hour>=17)&(hour<=20))
    lf=np.array([{'Central Junction':1.35,'Airport Road':1.15,'Tech Park Road':1.25,'Market Street':1.30,'Railway Station Road':1.20,'University Road':.85,'Industrial Area':1.00,'Hospital Junction':1.10,'Bus Stand Road':1.25,'Ring Road':1.05}[x] for x in location])
    weather=rng.choice(['Clear','Cloudy','Rainy','Heavy Rain'],n,p=[.55,.22,.17,.06])
    rainfall=np.where(weather=='Clear',rng.gamma(1,.3,n),np.where(weather=='Cloudy',rng.gamma(1.2,1,n),np.where(weather=='Rainy',rng.gamma(2,4,n),rng.gamma(2.5,8,n))))
    visibility=np.clip(10-rainfall*.35+rng.normal(0,.7,n),1,10)
    temp=29+3*np.sin((hour-6)/24*2*np.pi)+rng.normal(0,1.5,n)
    accidents=rng.poisson(.08+.10*peak+.03*(weather=='Heavy Rain'),n)
    base=420*lf+300*peak+100*(~weekend)-80*weekend
    vehicles=np.clip(base+rng.normal(0,120,n)+45*accidents-20*rainfall,80,None)
    density=np.clip(vehicles/capacity*100+rng.normal(0,5,n)+3*accidents,5,150)
    speed=np.clip(68-density*.30-2.2*rainfall-4*accidents+rng.normal(0,5,n),8,80)
    occupancy=np.clip(density/100+rng.normal(0,.04,n),.05,1)
    risk_score=(0.45*density + 18*(vehicles/capacity) + 0.12*(80-speed) + 2.0*accidents + 0.7*rainfall + 4*peak + rng.normal(0,5.0,n))
    q50,q80=np.quantile(risk_score,[0.50,0.80])
    congestion=np.select([risk_score<=q50,risk_score<=q80],['Low','Medium'],default='High')
    df=pd.DataFrame({'record_id':np.arange(1,n+1),'timestamp':ts,'date':ts.dt.date.astype(str),'time':ts.dt.strftime('%H:%M'),'day_of_week':ts.dt.day_name(),'hour':hour,'location':location,'latitude':[LOCATIONS[x][0] for x in location],'longitude':[LOCATIONS[x][1] for x in location],'road_type':road_type,'road_capacity':capacity,'vehicle_count':np.round(vehicles,1),'average_speed':np.round(speed,1),'traffic_density':np.round(density,1),'occupancy_rate':np.round(occupancy,3),'weather_condition':weather,'temperature':np.round(temp,1),'rainfall':np.round(rainfall,2),'visibility':np.round(visibility,2),'accident_count':accidents,'congestion_level':congestion})
    RAW_DATA.parent.mkdir(parents=True,exist_ok=True); df.to_csv(RAW_DATA,index=False); return df
if __name__=='__main__': print(f'Generated {len(generate_data()):,} records at {RAW_DATA}')
