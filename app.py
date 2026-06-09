import streamlit as st
import pandas as pd

# --- CONFIG & CSS ---
st.set_page_config(page_title="Recovery Specs", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4, p, label { color: #ffffff !important; }
    input { background-color: #1c1c1c !important; color: white !important; border: 1px solid #333 !important; }
    div.stButton > button { background-color: #f6782a !important; color: white !important; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    return pd.read_excel("Vehicle_Library_Populated.xlsx")

df = load_data()

# --- NAVIGATION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'search'
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = df

# --- PAGE 1: SEARCH ---
if st.session_state.page == 'search':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("641c5719-41d0-40ec-adc9-eb3a3e763903.png", width=200)
        st.caption("FIELD LOOKUP // VEHICLE LIBRARY")
    
    st.subheader("Search Specs")
    make = st.text_input("MAKE", placeholder="e.g. Ford")
    model = st.text_input("MODEL", placeholder="e.g. Focus")
    year = st.text_input("YEAR", placeholder="e.g. 2018")

    if st.button("🔍 SEARCH SPECS"):
        temp_df = df
        if make: temp_df = temp_df[temp_df['Make'].str.contains(make, case=False, na=False)]
        if model: temp_df = temp_df[temp_df['Model'].str.contains(model, case=False, na=False)]
        
        st.session_state.filtered_df = temp_df
        st.session_state.page = 'results'
        st.rerun()

# --- PAGE 2: RESULTS ---
elif st.session_state.page == 'results':
    if st.button("⬅ Back to Search"):
        st.session_state.page = 'search'
        st.rerun()
    
    st.subheader(f"Results ({len(st.session_state.filtered_df)})")
    
    # This displays them exactly as they are in your Excel file
    st.dataframe(st.session_state.filtered_df, use_container_width=True)
