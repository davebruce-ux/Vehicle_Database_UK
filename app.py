import streamlit as st
import pandas as pd

# --- CONFIG & CSS ---
st.set_page_config(page_title="Recovery Specs", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4, p, label { color: #ffffff !important; }
    div.stSelectbox > label { font-weight: bold; }
    div.stButton > button { background-color: #f6782a !important; color: white !important; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    return pd.read_excel("Vehicle_Library_Populated.xlsx")

df = load_data()

# --- INITIALIZE SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 'search'

# --- PAGE: SEARCH ---
if st.session_state.page == 'search':
    # Logo (Ensure file is in repo)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("641c5719-41d0-40ec-adc9-eb3a3e763903.png", width=200)
        st.caption("FIELD LOOKUP // VEHICLE LIBRARY")

    st.subheader("Search Specs")

    # 1. Dynamic Make Dropdown
    makes = sorted(df['Make'].dropna().unique())
    selected_make = st.selectbox("MAKE", options=[""] + makes)

    # 2. Dynamic Model Dropdown (depends on Make)
    models = []
    if selected_make:
        models = sorted(df[df['Make'] == selected_make]['Model'].dropna().unique())
    selected_model = st.selectbox("MODEL", options=[""] + models, disabled=not selected_make)

    # 3. Dynamic Year Display (depends on Model)
    selected_year = ""
    if selected_model:
        years = df[(df['Make'] == selected_make) & (df['Model'] == selected_model)]['Year Range'].unique()
        selected_year = st.selectbox("YEAR RANGE", options=years)

    if st.button("🔍 SEARCH SPECS"):
        if selected_make and selected_model:
            st.session_state.filtered_df = df[(df['Make'] == selected_make) & 
                                              (df['Model'] == selected_model)]
            st.session_state.page = 'results'
            st.rerun()
        else:
            st.warning("Please select a Make and Model.")

# --- PAGE: RESULTS ---
elif st.session_state.page == 'results':
    if st.button("⬅ Back to Search"):
        st.session_state.page = 'search'
        st.rerun()
    
    st.subheader("Vehicle Specifications")
    st.dataframe(st.session_state.filtered_df, use_container_width=True)
