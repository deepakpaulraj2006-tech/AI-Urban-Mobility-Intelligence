import streamlit as st
def inject_css():
    css = '<style>.stApp{background:linear-gradient(135deg,#07111f 0%,#0c1630 55%,#10172d 100%)}.block-container{max-width:1450px;padding-top:1.4rem}.hero{padding:24px 28px;border-radius:22px;background:linear-gradient(135deg,#182650,#30255e);border:1px solid #384574;margin-bottom:22px}.hero h1{margin:0;font-size:2.35rem}.hero p{color:#bac6e8}.kpi{padding:18px;border-radius:18px;background:#121b33;border:1px solid #2b385f;min-height:112px}.kpi .label{color:#aab6d6;font-size:.88rem}.kpi .value{font-size:1.75rem;font-weight:750;margin-top:8px}</style>'
    st.markdown(css, unsafe_allow_html=True)
def kpi(label,value,icon):
    st.markdown(f'<div class="kpi"><div class="label">{icon} {label}</div><div class="value">{value}</div></div>',unsafe_allow_html=True)
