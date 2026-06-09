import streamlit as st
import pandas as pd
import re

# --- CONFIG ---
st.set_page_config(page_title="Recovery Specs", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4, p, label { color: #ffffff !important; }
    div.stButton > button { background-color: #f6782a !important; color: white !important; width: 100%; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_excel("Vehicle_Library_Populated.xlsx")
    df['Clean_Model'] = df['Model'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', str(x)).strip())
    return df

df = load_data()

# --- HEADER ---
col1, col2, col3 = st.columns([1, 4, 1]) 
with col2:
    st.image("WhatsApp Image 2026-06-09 at 15.53.35.jpeg", use_container_width=True)

st.subheader("Search Specs")

# --- SEARCH BOXES ---
# 1. MAKE
all_makes = sorted(df['Make'].dropna().unique())
selected_make = st.selectbox("MAKE", options=[""] + all_makes)

# 2. MODEL (Filtered by Make)
filtered_by_make = df if not selected_make else df[df['Make'] == selected_make]
available_models = sorted(filtered_by_make['Clean_Model'].unique())
selected_model = st.selectbox("MODEL", options=[""] + available_models)

# 3. YEAR RANGE (Filtered by Make and Model)
filtered_by_model = filtered_by_make if not selected_model else filtered_by_make[filtered_by_make['Clean_Model'] == selected_model]
available_years = sorted(filtered_by_model['Year Range'].unique())
selected_year = st.selectbox("YEAR RANGE", options=[""] + available_years)

# --- SEARCH BUTTON ---
# We use columns [1, 2, 1] to create a centered block for the button
_, col_mid, _ = st.columns([1, 2, 1])

with col_mid:
    search_clicked = st.button("🔍 SEARCH SPECS", use_container_width=True)

if search_clicked:
    # Filter the data based on whatever is selected
    results = df.copy()
    if selected_make:
        results = results[results['Make'] == selected_make]
    if selected_model:
        results = results[results['Clean_Model'] == selected_model]
    if selected_year:
        results = results[results['Year Range'] == selected_year]
    
    st.divider()
    if not results.empty:
        st.subheader(f"Found {len(results)} Result(s)")
        st.dataframe(results.drop(columns=['Clean_Model']), use_container_width=True)
    else:
        st.error("No results found for that combination.")
