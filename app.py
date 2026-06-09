import streamlit as st
import pandas as pd
import re

# --- CONFIG ---
st.set_page_config(page_title="Recovery Specs", layout="centered")
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
    # Clean models: remove text in parentheses (e.g., "Focus (Mk3)" -> "Focus")
    df['Clean_Model'] = df['Model'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', str(x)).strip())
    return df

df = load_data()

if 'page' not in st.session_state: st.session_state.page = 'search'

# --- PAGE: SEARCH ---
if st.session_state.page == 'search':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("641c5719-41d0-40ec-adc9-eb3a3e763903.png", width=200)
    
    st.subheader("Search Specs")

    # 1. Select Make
    makes = sorted(df['Make'].dropna().unique())
    selected_make = st.selectbox("MAKE", options=[""] + makes)

    # 2. Select Cleaned Model
    selected_model = ""
    if selected_make:
        models = sorted(df[df['Make'] == selected_make]['Clean_Model'].unique())
        selected_model = st.selectbox("MODEL", options=[""] + models)

    # 3. Select Year Range
    selected_year = ""
    if selected_model:
        years = df[(df['Make'] == selected_make) & (df['Clean_Model'] == selected_model)]['Year Range'].unique()
        selected_year = st.selectbox("YEAR RANGE", options=[""] + sorted(years))

    if st.button("🔍 SEARCH SPECS"):
        if selected_make and selected_model and selected_year:
            st.session_state.filtered_df = df[(df['Make'] == selected_make) & 
                                              (df['Clean_Model'] == selected_model) & 
                                              (df['Year Range'] == selected_year)]
            st.session_state.page = 'results'
            st.rerun()
        else:
            st.warning("Please select Make, Model, and Year Range.")

# --- PAGE: RESULTS ---
elif st.session_state.page == 'results':
    if st.button("⬅ Back to Search"):
        st.session_state.page = 'search'
        st.rerun()
    st.dataframe(st.session_state.filtered_df.drop(columns=['Clean_Model']), use_container_width=True)
