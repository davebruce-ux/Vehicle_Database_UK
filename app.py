import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Recovery Specs", layout="centered")

# --- CUSTOM CSS FOR BRANDING ---
st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: white; }
    div.stButton > button { background-color: #f6782a; color: white; width: 100%; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
# Note: Ensure your logo file is in the repository!
try:
    st.image("641c5719-41d0-40ec-adc9-eb3a3e763903.png", width=200)
except:
    st.title("RECOVERY SPECS")

st.caption("FIELD LOOKUP // VEHICLE LIBRARY")

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
