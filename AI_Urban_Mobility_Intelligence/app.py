import json,sys
from pathlib import Path
import numpy as np,pandas as pd,streamlit as st,plotly.express as px
from streamlit_folium import st_folium
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT))
from config.config import PROCESSED_DATA,MODEL_PATH,METADATA_PATH
from src.hotspot_analysis import hotspot_scores
from src.prediction import load_model,predict_one
from dashboard.styles import inject_css,kpi
from dashboard.charts import hourly_heatmap,scatter_speed,location_bar
from dashboard.maps import traffic_map
st.set_page_config(page_title='AI Urban Mobility Intelligence',page_icon='🚦',layout='wide'); inject_css()
@st.cache_data
def load_data():
    if not PROCESSED_DATA.exists():
        from src.data_generation import generate_data; from src.data_cleaning import clean_data; generate_data(); d=clean_data(pd.read_csv(ROOT/'data/raw/traffic_raw.csv')); PROCESSED_DATA.parent.mkdir(parents=True,exist_ok=True); d.to_csv(PROCESSED_DATA,index=False)
    d=pd.read_csv(PROCESSED_DATA); d['timestamp']=pd.to_datetime(d.timestamp); return d
@st.cache_resource
def get_model():
    if not MODEL_PATH.exists():
        from src.train_model import train; train()
    return load_model()
@st.cache_data
def get_meta(): return json.loads(METADATA_PATH.read_text()) if METADATA_PATH.exists() else {}
df=load_data(); meta=get_meta()
st.sidebar.markdown('## 🚦 Mobility AI'); page=st.sidebar.radio('Navigate',['🏠 Overview','📈 Traffic Analytics','🔥 Hotspot Intelligence','🤖 Congestion Prediction','🧠 Model Insights','🎯 What-If Simulator','ℹ️ About Project']); st.sidebar.caption('🟢 System Online'); st.sidebar.caption('Academic / Simulated Traffic Intelligence Platform')
with st.sidebar.expander('🎛️ Global Filters',expanded=True):
    loc=st.multiselect('Location',sorted(df.location.unique())); weather=st.multiselect('Weather',sorted(df.weather_condition.unique())); road=st.multiselect('Road type',sorted(df.road_type.unique())); cong=st.multiselect('Congestion',['Low','Medium','High']); hours=st.slider('Hour range',0,23,(0,23)); dates=st.date_input('Date range',(df.timestamp.min().date(),df.timestamp.max().date()))
fdf=df.copy()
if loc:fdf=fdf[fdf.location.isin(loc)]
if weather:fdf=fdf[fdf.weather_condition.isin(weather)]
if road:fdf=fdf[fdf.road_type.isin(road)]
if cong:fdf=fdf[fdf.congestion_level.isin(cong)]
fdf=fdf[fdf.hour.between(*hours)]
if isinstance(dates,tuple) and len(dates)==2:fdf=fdf[fdf.timestamp.dt.date.between(dates[0],dates[1])]
def hero(): st.markdown('<div class="hero"><h1>🚦 AI Urban Mobility Intelligence</h1><p>Data-Driven Traffic Analysis • Hotspot Detection • Congestion Prediction</p></div>',unsafe_allow_html=True)
def empty():
    if fdf.empty: st.warning('No traffic records match the selected filters. Try adjusting the filters.'); return True
    return False
if page=='🏠 Overview':
    hero()
    if not empty():
        high=(fdf.congestion_level=='High').mean()*100; hs=hotspot_scores(fdf); cols=st.columns(5); vals=[(f'{len(fdf):,}','Total Records','📊'),(f'{fdf.vehicle_count.mean():.0f}','Average Vehicles','🚗'),(f'{fdf.average_speed.mean():.1f} km/h','Average Speed','⚡'),(f'{high:.1f}%','High Congestion','🚦'),(str((hs.risk.astype(str)=='High Risk').sum()),'High-Risk Locations','🔥')]
        for c,(v,l,i) in zip(cols,vals):
            with c:kpi(l,v,i)
        st.markdown('### Traffic Status'); status='High' if high>=45 else ('Medium' if high>=20 else 'Low'); st.markdown(f"## {'🔴' if status=='High' else '🟡' if status=='Medium' else '🟢'} {status}")
        a,b=st.columns(2); 
        with a: st.plotly_chart(px.line(fdf.groupby('timestamp',as_index=False).vehicle_count.mean(),x='timestamp',y='vehicle_count',title='Traffic Volume Over Time'),use_container_width=True)
        with b: st.plotly_chart(px.histogram(fdf,x='congestion_level',color='congestion_level',category_orders={'congestion_level':['Low','Medium','High']},color_discrete_map={'Low':'#22c55e','Medium':'#f59e0b','High':'#ef4444'},title='Congestion Distribution'),use_container_width=True)
        a,b=st.columns(2)
        with a: st.plotly_chart(location_bar(fdf,'vehicle_count'),use_container_width=True)
        with b: st.plotly_chart(px.line(fdf.groupby('hour',as_index=False).vehicle_count.mean(),x='hour',y='vehicle_count',markers=True,title='Hourly Traffic Pattern'),use_container_width=True)
        peak=int(fdf.groupby('hour').vehicle_count.mean().idxmax()); busiest=fdf.groupby('location').vehicle_count.mean().idxmax(); slowest=fdf.groupby('location').average_speed.mean().idxmin(); st.markdown('### 💡 Automated Traffic Insights'); st.info(f'Peak average traffic occurs around **{peak}:00**. **{busiest}** has the highest average vehicle volume in the current filter. **{slowest}** has the lowest average speed in the current filter.')
elif page=='📈 Traffic Analytics':
    hero(); st.title('📈 Traffic Analytics')
    if not empty():
        st.plotly_chart(hourly_heatmap(fdf),use_container_width=True); st.plotly_chart(scatter_speed(fdf),use_container_width=True); a,b=st.columns(2)
        with a:
            w=fdf.groupby('weather_condition',as_index=False).average_speed.mean(); st.plotly_chart(px.bar(w,x='weather_condition',y='average_speed',title='Average Speed by Weather'),use_container_width=True)
        with b:
            r=fdf.groupby('road_type',as_index=False).vehicle_count.mean(); st.plotly_chart(px.bar(r,x='road_type',y='vehicle_count',title='Average Vehicles by Road Type'),use_container_width=True)
elif page=='🔥 Hotspot Intelligence':
    hero(); st.title('🔥 Hotspot Intelligence')
    if not empty():
        scores=hotspot_scores(fdf); n={'Top 5':5,'Top 10':10,'All':len(scores)}[st.selectbox('Show locations',['Top 5','Top 10','All'])]; top=scores.head(n); st.plotly_chart(px.bar(top.sort_values('hotspot_score'),x='hotspot_score',y='location',orientation='h',color='risk',color_discrete_map={'Low Risk':'#22c55e','Moderate Risk':'#f59e0b','High Risk':'#ef4444'},title='Project-Defined Hotspot Score'),use_container_width=True); st.dataframe(top,use_container_width=True,hide_index=True); st.caption('Academic indicator; not an official traffic authority formula.'); st_folium(traffic_map(fdf,scores),use_container_width=True,height=500)
elif page=='🤖 Congestion Prediction':
    hero(); st.title('🤖 Congestion Prediction'); model=get_model(); a,b,c=st.columns(3)
    with a: loc=st.selectbox('Location',sorted(df.location.unique())); hour=st.slider('Hour',0,23,8); day=st.selectbox('Day',['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']); vehicle=st.number_input('Vehicle Count',80,3000,900)
    with b: road=st.selectbox('Road Type',sorted(df.road_type.unique())); speed=st.number_input('Average Speed',5.,100.,40.); density=st.number_input('Traffic Density',1.,150.,60.); capacity=st.number_input('Road Capacity',300.,2500.,1300.)
    with c: weather=st.selectbox('Weather',sorted(df.weather_condition.unique())); rain=st.number_input('Rainfall',0.,50.,2.); vis=st.number_input('Visibility',1.,10.,8.); accidents=st.number_input('Accident Count',0,10,0)
    if st.button('🚦 PREDICT CONGESTION',use_container_width=True):
        values={'location':loc,'road_type':road,'day_of_week':day,'road_capacity':capacity,'vehicle_count':vehicle,'average_speed':speed,'traffic_density':density,'occupancy_rate':min(1,density/100),'weather_condition':weather,'temperature':29.,'rainfall':rain,'visibility':vis,'accident_count':accidents,'hour':hour}; pred,probs=predict_one(model,values); st.markdown(f"## {'🟢' if pred=='Low' else '🟡' if pred=='Medium' else '🔴'} Predicted Congestion: **{pred.upper()}**")
        if probs is not None: st.plotly_chart(px.bar(pd.DataFrame({'Class':model.classes_,'Probability':probs}),x='Class',y='Probability',color='Class',color_discrete_map={'Low':'#22c55e','Medium':'#f59e0b','High':'#ef4444'},title='Prediction Probabilities'),use_container_width=True)
elif page=='🧠 Model Insights':
    hero(); st.title('🧠 Model Insights')
    if meta:
        st.info(f"Deployment model: **{meta['selected_model']}**. Selection rule: highest weighted F1, then accuracy."); rows=[{'Model':n,**{k:v for k,v in m.items() if k in ['accuracy','precision','recall','f1']}} for n,m in meta['metrics'].items()]; res=pd.DataFrame(rows); st.dataframe(res.style.format({c:'{:.3f}' for c in res.columns[1:]}),use_container_width=True,hide_index=True); st.plotly_chart(px.bar(res.melt('Model'),x='Model',y='value',color='variable',barmode='group',range_y=[0,1],title='Model Metrics'),use_container_width=True); cm=np.array(meta['metrics'][meta['selected_model']]['confusion_matrix']); st.plotly_chart(px.imshow(cm,x=['Low','Medium','High'],y=['Low','Medium','High'],text_auto=True,color_continuous_scale='Blues',title='Selected Model Confusion Matrix'),use_container_width=True)
        if meta.get('feature_importance'):
            fi=pd.DataFrame({'Feature':list(meta['feature_importance']),'Importance':list(meta['feature_importance'].values())}).sort_values('Importance',ascending=False).head(10); st.plotly_chart(px.bar(fi.sort_values('Importance'),x='Importance',y='Feature',orientation='h',title='Top Model Feature Importance'),use_container_width=True)
elif page=='🎯 What-If Simulator':
    hero(); st.title('🎯 Traffic Scenario Simulator'); st.caption('Model-based what-if simulation; not a guaranteed real-world intervention forecast.'); model=get_model(); base=st.selectbox('Base location',sorted(df.location.unique())); s=df[df.location==base].iloc[0]; a,b=st.columns(2)
    with a: st.markdown('### Current Scenario'); bv=st.number_input('Current vehicles',100.,3000.,float(s.vehicle_count)); bs=st.number_input('Current speed',5.,100.,float(s.average_speed)); bd=st.number_input('Current density',1.,150.,float(s.traffic_density)); br=st.number_input('Current rainfall',0.,50.,float(s.rainfall))
    with b: st.markdown('### Modified Scenario'); mv=st.number_input('Modified vehicles',100.,3000.,float(s.vehicle_count)*1.1); ms=st.number_input('Modified speed',5.,100.,float(s.average_speed)); md=st.number_input('Modified density',1.,150.,float(s.traffic_density)*1.1); mr=st.number_input('Modified rainfall',0.,50.,float(s.rainfall))
    common={'location':base,'road_type':s.road_type,'day_of_week':s.day_of_week,'road_capacity':s.road_capacity,'occupancy_rate':s.occupancy_rate,'weather_condition':s.weather_condition,'temperature':s.temperature,'visibility':s.visibility,'accident_count':s.accident_count,'hour':s.hour}; aa={**common,'vehicle_count':bv,'average_speed':bs,'traffic_density':bd,'rainfall':br}; bb={**common,'vehicle_count':mv,'average_speed':ms,'traffic_density':md,'rainfall':mr}
    if st.button('🔮 RUN SCENARIO COMPARISON',use_container_width=True):
        pa,qa=predict_one(model,aa); pb,qb=predict_one(model,bb); x,y=st.columns(2)
        with x: st.metric('Current Prediction',pa)
        with y: st.metric('Modified Prediction',pb)
        if qa is not None: st.plotly_chart(px.bar(pd.DataFrame({'Class':model.classes_,'Current':qa,'Modified':qb}).melt('Class'),x='Class',y='value',color='variable',barmode='group',title='Probability Shift'),use_container_width=True)
else:
    hero(); st.title('ℹ️ About Project')
    st.markdown("""### Prototype scope

**DATA → ANALYSIS → HOTSPOTS → AI PREDICTION → WHAT-IF SIMULATION**

This is an academic prototype using simulated traffic records and fictional locations. The hotspot score is project-defined, and model predictions are not traffic-authority forecasts.

**Technology:** Python • Pandas • NumPy • Plotly • Folium • Scikit-learn • Streamlit""")
