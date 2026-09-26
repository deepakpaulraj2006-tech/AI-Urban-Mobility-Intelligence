import streamlit as st
def section(title,subtitle=None): st.subheader(title); st.caption(subtitle) if subtitle else None
