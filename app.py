import streamlit as st
import pandas as pd
import re
import os

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
@st.cache_data(ttl=60)
def load_data():
    if not os.path.exists("Vehicle_Library_Populated.xlsx"):
        return pd.DataFrame()
    df = pd.read_excel("Vehicle_Library_Populated.xlsx")
    df['Clean_Model'] = df['Model'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', str(x)).strip())
    return df

def save_to_main_db(df):
    df.to_excel("Vehicle_Library_Populated.xlsx", index=False)

# --- 3. UI BLOCKS ---
def show_search_page():
    st.subheader("Search Specs")
    df = st.session_state.df
    selected_make = st.selectbox("MAKE", options=[""] + sorted(df['Make'].dropna().unique()))
    filtered_by_make = df if not selected_make else df[df['Make'] == selected_make]
    selected_model = st.selectbox("MODEL", options=[""] + sorted(filtered_by_make['Clean_Model'].unique()))
    filtered_by_model = filtered_by_make if not selected_model else filtered_by_make[filtered_by_make['Clean_Model'] == selected_model]
    selected_year = st.selectbox("YEAR RANGE", options=[""] + sorted(filtered_by_model['Year Range'].unique()))

    if st.button("🔍 SEARCH SPECS", use_container_width=True):
        st.session_state.results = filtered_by_model[filtered_by_model['Year Range'] == selected_year] if selected_year else filtered_by_model
        st.session_state.show_results = True
        st.rerun()

def show_vehicle_details(final_df):
    record = final_df.iloc[0]
    row_id = record.name
    st.subheader(f"{record['Make']} {record['Model']}")
    
    # Logic to display data dynamically based on columns
    for col in final_df.columns:
        if col == 'Clean_Model': continue
        val = str(record[col])
        st.markdown(f'<p class="result-header">{col}:</p>', unsafe_allow_html=True)
        
        # Display image or text
        if val.startswith("uploads/"): 
            st.image(val, use_container_width=True)
        else: 
            st.write(val if val.lower() != 'nan' else "No data available.")

    if st.button("⬅ Back to Search"):
        st.session_state.show_results = False
        st.rerun()

# --- 4. MAIN CONTROL ROOM ---
def main():
    if 'df' not in st.session_state: st.session_state.df = load_data()
    if 'show_results' not in st.session_state: st.session_state.show_results = False

    # Logo
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2: st.image("WhatsApp Image 2026-06-09 at 15.53.35.jpeg", use_container_width=True)

    if not st.session_state.show_results:
        show_search_page()
    else:
        show_vehicle_details(st.session_state.results)

if __name__ == "__main__":
    main()
