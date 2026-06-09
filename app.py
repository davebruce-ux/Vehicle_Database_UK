import streamlit as st
import pandas as pd
import re

# --- CONFIG ---
st.set_page_config(page_title="Recovery Specs", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4, p, label { color: #ffffff !important; }
    
    /* Main Search Button - Bright Orange */
    div[data-testid="stVerticalBlock"] div.stButton > button { 
        background-color: #f6782a !important; 
        color: white !important; 
        width: 100%; 
        font-weight: bold; 
    }
    
    /* Results List Buttons - Dark Gray */
    div[data-testid="stButton"] button { 
        background-color: #333333 !important; 
        color: white !important;
        border: 1px solid #555555;
    }

    /* Enlarged Header Style for Detail View */
    .result-header {
        font-size: 1.25em !important;
        color: #f6782a !important;
        font-weight: bold;
        margin-bottom: -10px !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_excel("Vehicle_Library_Populated.xlsx")
    df['Clean_Model'] = df['Model'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', str(x)).strip())
    return df

df = load_data()

# Initialize session state
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# --- HEADER ---
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
    
    filtered_by_model = filtered_by_make if not selected_model else filtered_by_make[filtered_by_make['Clean_Model'] == selected_model]
    available_years = sorted(filtered_by_model['Year Range'].unique())
    selected_year = st.selectbox("YEAR RANGE", options=[""] + available_years)

    # Centralized Search Button
    spacer_left, col_mid, spacer_right = st.columns([1, 2, 1])
    with col_mid:
        if st.button("🔍 SEARCH SPECS", use_container_width=True):
            st.session_state.results = filtered_by_model[filtered_by_model['Year Range'] == selected_year] if selected_year else filtered_by_model
            st.session_state.show_results = True
            st.rerun()

else:
    # --- RESULTS SCREEN ---
    final_df = st.session_state.results

    if len(final_df) == 1:
        # VERTICAL VIEW
        st.subheader("Vehicle Details")
        record = final_df.iloc[0]
        for col in final_df.columns:
            if col != 'Clean_Model':
                val = str(record[col])
                if val.lower() != 'nan':
                    st.markdown(f'<p class="result-header">{col}:</p> {val}', unsafe_allow_html=True)
                    st.write("") # Add a little breathing room
        
    else:
        # LIST VIEW
        st.subheader(f"Found {len(final_df)} Results")
        st.write("Select a vehicle to view details:")
        
        for idx, row in final_df.iterrows():
            label = f"{row['Make']} | {row['Model']} | {row['Year Range']}"
            if st.button(label, key=str(idx), use_container_width=True):
                st.session_state.results = final_df.loc[[idx]]
                st.rerun()

    # Back button
    st.divider()
    if st.button("⬅ Back to Search"):
        st.session_state.show_results = False
        st.rerun()
