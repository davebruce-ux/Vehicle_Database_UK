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
    # Clean models to show just the name (e.g., "Focus")
    df['Clean_Model'] = df['Model'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', str(x)).strip())
    return df

df = load_data()

# --- HEADER ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("641c5719-41d0-40ec-adc9-eb3a3e763903.png", width=200)

st.subheader("Search Specs")

# --- SEARCH BOXES (All visible immediately) ---
# We use sorted unique values, including an empty string for "All"
all_makes = sorted(df['Make'].dropna().unique())
selected_make = st.selectbox("MAKE", options=[""] + all_makes)

all_models = sorted(df['Clean_Model'].dropna().unique())
selected_model = st.selectbox("MODEL", options=[""] + all_models)

all_years = sorted(df['Year Range'].dropna().unique())
selected_year = st.selectbox("YEAR RANGE", options=[""] + all_years)

# --- FILTER LOGIC ---
filtered_df = df.copy()

if selected_make:
    filtered_df = filtered_df[filtered_df['Make'] == selected_make]
if selected_model:
    filtered_df = filtered_df[filtered_df['Clean_Model'] == selected_model]
if selected_year:
    filtered_df = filtered_df[filtered_df['Year Range'] == selected_year]

# --- RESULTS DISPLAY ---
st.divider()
st.subheader(f"Results ({len(filtered_df)})")
st.dataframe(filtered_df.drop(columns=['Clean_Model']), use_container_width=True)
