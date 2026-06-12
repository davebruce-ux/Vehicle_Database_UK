import streamlit as st
import pandas as pd
import re
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURATION BLOCK ---
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

# --- 2. DATA HANDLER BLOCK ---
@st.cache_data(ttl=600)
def load_data():
    # Establishes connection to your Google Sheet
    conn = st.connection("gsheets", type=GSheetsConnection)
    url = "https://docs.google.com/spreadsheets/d/1dTq4EZmYsfl4C8zsNYsT1dRwB37Os9RW/edit"
    df = conn.read(spreadsheet=url, usecols=None)
    
    # Ensures 'Clean_Model' is created for search functionality
    if 'Model' in df.columns:
        df['Clean_Model'] = df['Model'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', str(x)).strip())
    return df

# --- 3. UI BLOCKS ---
def show_search_page():
    st.subheader("Search Specs")
    df = st.session_state.df
    
    # Search Filters
    selected_make = st.selectbox("MAKE", options=[""] + sorted(df['Make'].dropna().unique().astype(str)))
    filtered_by_make = df if not selected_make else df[df['Make'] == selected_make]
    
    selected_model = st.selectbox("MODEL", options=[""] + sorted(filtered_by_make['Clean_Model'].unique().astype(str)))
    filtered_by_model = filtered_by_make if not selected_model else filtered_by_make[filtered_by_model['Clean_Model'] == selected_model]
    
    selected_year = st.selectbox("YEAR RANGE", options=[""] + sorted(filtered_by_model['Year Range'].unique().astype(str)))

    if st.button("🔍 SEARCH SPECS", use_container_width=True):
        st.session_state.results = filtered_by_model[filtered_by_model['Year Range'] == selected_year] if selected_year else filtered_by_model
        st.session_state.show_results = True
        st.rerun()

def show_vehicle_details(final_df):
    record = final_df.iloc[0]
    st.subheader(f"{record['Make']} {record['Model']}")
    
    # Dynamic display of all columns (No edit access for drivers)
    for col in final_df.columns:
        if col in ['Clean_Model', 'Make', 'Model']: continue
        val = str(record[col])
        st.markdown(f'<p class="result-header">{col}:</p>', unsafe_allow_html=True)
        
        # Display image link or text
        if val.startswith("http"): 
            st.link_button("View Official Source", val)
        elif val.lower() != 'nan':
            st.write(val)
        else:
            st.write("No data available.")

    if st.button("⬅ Back to Search"):
        st.session_state.show_results = False
        st.rerun()

# --- 4. MAIN CONTROL ROOM ---
def main():
    if 'df' not in st.session_state: st.session_state.df = load_data()
    if 'show_results' not in st.session_state: st.session_state.show_results = False

    # Logo Placeholder
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2: st.image("WhatsApp Image 2026-06-09 at 15.53.35.jpeg", use_container_width=True)

    if not st.session_state.show_results:
        show_search_page()
    else:
        show_vehicle_details(st.session_state.results)

if __name__ == "__main__":
    main()
