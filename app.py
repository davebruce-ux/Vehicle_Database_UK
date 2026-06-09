import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Recovery Specs", layout="centered")

# --- CUSTOM CSS FOR BRANDING ---
st.markdown("""
    <style>
    /* Change main background to black */
    .stApp { 
        background-color: #000000; 
        color: #ffffff; 
    }
    
    /* Style headers to be white */
    h1, h2, h3, h4, p, label { 
        color: #ffffff !important; 
    }
    
    /* Make search boxes look better against black */
    input { 
        background-color: #1c1c1c !important; 
        color: white !important; 
        border: 1px solid #333 !important; 
    }
    
    /* Make the button orange and bold */
    div.stButton > button { 
        background-color: #f6782a !important; 
        color: white !important; 
        font-weight: bold;
        width: 100%; 
        border: none; 
    }
    </style>
""", unsafe_allow_html=True)

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
