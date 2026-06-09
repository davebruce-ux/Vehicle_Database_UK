import streamlit as st
import pandas as pd
import re

# --- CONFIG ---
st.set_page_config(page_title="Recovery Specs", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4, p, label { color: #ffffff !important; }
    div.stButton > button { background-color: #f6782a !important; color: white !important; width: 100%; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_excel("Vehicle_Library_Populated.xlsx")
    df['Clean_Model'] = df['Model'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', str(x)).strip())
    return df

df = load_data()

# --- SIDEBAR (Always Visible) ---
with st.sidebar:
    st.image("641c5719-41d0-40ec-adc9-eb3a3e763903.png", width=150)
    st.subheader("Search Specs")
    
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

    search_clicked = st.button("🔍 SEARCH SPECS")

# --- MAIN CONTENT ---
st.title("Vehicle Specifications")

if search_clicked and selected_make and selected_model and selected_year:
    filtered_df = df[(df['Make'] == selected_make) & 
                     (df['Clean_Model'] == selected_model) & 
                     (df['Year Range'] == selected_year)]
    st.dataframe(filtered_df.drop(columns=['Clean_Model']), use_container_width=True)
else:
    st.info("Select a vehicle from the sidebar to view specifications.")
