import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Recovery Specs", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4, p, label { color: #ffffff !important; }
    input { background-color: #1c1c1c !important; color: white !important; border: 1px solid #333 !important; }
    div.stButton > button { background-color: #f6782a !important; color: white !important; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
# Ensure your logo file is uploaded to the root of your repo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("641c5719-41d0-40ec-adc9-eb3a3e763903.png", width=200)
    st.caption(        "VEHICLE LIBRARY")

# --- LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    return pd.read_excel("Vehicle_Library_Populated.xlsx")

df = load_data()

# --- SEARCH UI ---
st.subheader("Search Specs")
make = st.text_input("MAKE", placeholder="e.g. Ford, BMW, Toyota")
model = st.text_input("MODEL", placeholder="e.g. Focus, 3 Series, Corolla")
year = st.text_input("YEAR", placeholder="e.g. 2018")

if st.button("🔍 SEARCH SPECS"):
    filtered_df = df
    if make:
        filtered_df = filtered_df[filtered_df['Make'].str.contains(make, case=False, na=False)]
    if model:
        filtered_df = filtered_df[filtered_df['Model'].str.contains(model, case=False, na=False)]
    
    st.write(f"### Results ({len(filtered_df)})")
    if not filtered_df.empty:
        st.dataframe(filtered_df)
    else:
        st.warning("No vehicles found.")
