import streamlit as st
import pandas as pd
import re
from streamlit_gsheets import GSheetsConnection

# --- CONFIG ---
st.set_page_config(page_title="Recovery Specs", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4, p, label { color: #ffffff !important; }
    div[data-testid="stVerticalBlock"] div.stButton > button { background-color: #f6782a !important; color: white !important; width: 100%; font-weight: bold; }
    div[data-testid="stButton"] button { background-color: #333333 !important; color: white !important; border: 1px solid #555555; }
    .result-header { font-size: 1.25em !important; color: #f6782a !important; font-weight: bold; margin-bottom: -5px !important; }
    </style>
""", unsafe_allow_html=True)

# --- DATA HANDLER ---
@st.cache_data(ttl=600)
def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    url = "https://docs.google.com/spreadsheets/d/1dTq4EZmYsfl4C8zsNYsT1dRwB37Os9RW/edit"
    df = conn.read(spreadsheet=url, usecols=None)
    df.columns = df.columns.str.strip() # Remove accidental spaces in headers
    
    # Create Clean_Model for search
    if 'Model' in df.columns:
        df['Clean_Model'] = df['Model'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', str(x)).strip())
    return df

# --- STATE ---
if 'df' not in st.session_state:
    st.session_state.df = load_data()
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# --- UI ---
col1, col2, col3 = st.columns([1, 4, 1]) 
with col2:
    st.image("WhatsApp Image 2026-06-09 at 15.53.35.jpeg", use_container_width=True)

if not st.session_state.show_results:
    st.subheader("Search Specs")
    df = st.session_state.df
    
    # Search Inputs
    selected_make = st.selectbox("MAKE", options=[""] + sorted(df['Make'].dropna().unique().astype(str)))
    filtered_by_make = df if not selected_make else df[df['Make'] == selected_make]
    
    selected_model = st.selectbox("MODEL", options=[""] + sorted(filtered_by_make['Clean_Model'].unique().astype(str)))
    filtered_by_model = filtered_by_make if not selected_model else filtered_by_make[filtered_by_make['Clean_Model'] == selected_model]
    
    selected_year = st.selectbox("YEAR RANGE", options=[""] + sorted(filtered_by_model['Year Range'].unique().astype(str)))

    if st.button("🔍 SEARCH SPECS", use_container_width=True):
        st.session_state.results = filtered_by_model[filtered_by_model['Year Range'] == selected_year] if selected_year else filtered_by_model
        st.session_state.show_results = True
        st.rerun()

else:
    final_df = st.session_state.results
    if len(final_df) == 1:
        st.subheader("Vehicle Details")
        record = final_df.iloc[0]
        for col in final_df.columns:
            if col in ['Clean_Model', 'Model', 'Make']: continue
            val = str(record[col])
            st.markdown(f'<p class="result-header">{col}:</p>', unsafe_allow_html=True)
            st.write(val if val.lower() != 'nan' else "No data available.")
            
        if st.button("⬅ Back to Search"):
            st.session_state.show_results = False
            st.rerun()
    else:
        st.subheader(f"Found {len(final_df)} Results")
        for idx, row in final_df.iterrows():
            if st.button(f"{row['Make']} | {row['Model']} | {row['Year Range']}", key=str(idx), use_container_width=True):
                st.session_state.results = final_df.loc[[idx]]
                st.rerun()
        if st.button("⬅ Back to Search"):
            st.session_state.show_results = False
            st.rerun()
