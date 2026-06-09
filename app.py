import streamlit as st
import pandas as pd
import re

# --- CONFIG ---
st.set_page_config(page_title="Recovery Specs", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4, p, label { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_excel("Vehicle_Library_Populated.xlsx")
    df['Clean_Model'] = df['Model'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', str(x)).strip())
    return df

df = load_data()

# --- HEADER (Visible) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("641c5719-41d0-40ec-adc9-eb3a3e763903.png", width=200)

st.subheader("Search Specs")

# --- SEARCH BOXES (Always Visible) ---
makes = sorted(df['Make'].dropna().unique())
selected_make = st.selectbox("MAKE", options=[""] + makes)

selected_model = ""
if selected_make:
    models = sorted(df[df['Make'] == selected_make]['Clean_Model'].unique())
    selected_model = st.selectbox("MODEL", options=[""] + models)

selected_year = ""
if selected_model:
    years = df[(df['Make'] == selected_make) & (df['Clean_Model'] == selected_model)]['Year Range'].unique()
    selected_year = st.selectbox("YEAR RANGE", options=[""] + sorted(years))

# --- RESULTS (Always Visible Below) ---
if selected_make and selected_model and selected_year:
    st.divider()
    filtered_df = df[(df['Make'] == selected_make) & 
                     (df['Clean_Model'] == selected_model) & 
                     (df['Year Range'] == selected_year)]
    
    st.subheader("Vehicle Details")
    st.dataframe(filtered_df.drop(columns=['Clean_Model']), use_container_width=True)
