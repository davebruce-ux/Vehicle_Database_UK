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
all_makes = sorted(df['Make'].dropna().unique())
selected_make = st.selectbox("MAKE", options=[""] + all_makes)

filtered_by_make = df if not selected_make else df[df['Make'] == selected_make]
available_models = sorted(filtered_by_make['Clean_Model'].unique())
selected_model = st.selectbox("MODEL", options=[""] + available_models)

filtered_by_model = filtered_by_make if not selected_model else filtered_by_make[filtered_by_model['Clean_Model'] == selected_model]
available_years = sorted(filtered_by_model['Year Range'].unique())
selected_year = st.selectbox("YEAR RANGE", options=[""] + available_years)

# --- SEARCH BUTTON ---
# The results will only trigger when this button is clicked
if st.button("🔍 SEARCH SPECS"):
    if selected_make and selected_model and selected_year:
        st.divider()
        final_df = filtered_by_model[filtered_by_model['Year Range'] == selected_year]
        st.subheader("Results")
        st.dataframe(final_df.drop(columns=['Clean_Model']), use_container_width=True)
    else:
        st.warning("Please select a Make, Model, and Year Range to search.")
