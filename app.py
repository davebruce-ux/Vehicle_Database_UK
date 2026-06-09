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

# Initialize session state for navigation
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# --- HEADER (Always visible) ---
col1, col2, col3 = st.columns([1, 4, 1]) 
with col2:
    st.image("WhatsApp Image 2026-06-09 at 15.53.35.jpeg", use_container_width=True)

# --- PAGE LOGIC ---
if not st.session_state.show_results:
    # SEARCH SCREEN
    st.subheader("Search Specs")
    all_makes = sorted(df['Make'].dropna().unique())
    selected_make = st.selectbox("MAKE", options=[""] + all_makes)
    
    filtered_by_make = df if not selected_make else df[df['Make'] == selected_make]
    available_models = sorted(filtered_by_make['Clean_Model'].unique())
    selected_model = st.selectbox("MODEL", options=[""] + available_models)
    
    filtered_by_model = filtered_by_make if not selected_model else filtered_by_make[filtered_by_model['Clean_Model'] == selected_model]
    available_years = sorted(filtered_by_model['Year Range'].unique())
    selected_year = st.selectbox("YEAR RANGE", options=[""] + available_years)

    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        if st.button("🔍 SEARCH SPECS"):
            st.session_state.results = filtered_by_model[filtered_by_model['Year Range'] == selected_year] if selected_year else filtered_by_model
            st.session_state.show_results = True
            st.rerun()

else:
    # --- RESULTS SCREEN ---
else:
    # Logic to filter data before showing results
    final_df = st.session_state.results

    if len(final_df) == 1:
        # VERTICAL VIEW for single result
        st.subheader("Vehicle Details")
        record = final_df.iloc[0]
        # Display all columns except Clean_Model
        for col in final_df.columns:
            if col != 'Clean_Model':
                st.write(f"**{col}:** {record[col]}")
        
    else:
        # LIST VIEW for multiple results
        st.subheader(f"Found {len(final_df)} Results")
        st.write("Select a vehicle to view details:")
        
        # Display clickable list using buttons
        for idx, row in final_df.iterrows():
            label = f"{row['Make']} | {row['Model']} | {row['Year Range']}"
            if st.button(label, key=f"btn_{idx}"):
                # Update session state to show ONLY this specific row
                st.session_state.results = final_df.loc[[idx]]
                st.rerun()

    # Back button
    st.divider()
    if st.button("⬅ Back to Search"):
        st.session_state.show_results = False
        st.rerun()
        
