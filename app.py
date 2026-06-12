import streamlit as st
import pandas as pd
import re

# --- CONFIG ---
st.set_page_config(page_title="Recovery Specs", layout="centered")

# --- DATA HANDLER ---
@st.cache_data(ttl=600)
def load_data():
    # Use native Streamlit connection for Google Sheets
    conn = st.connection("gsheets", type="gsheets")
    url = "https://docs.google.com/spreadsheets/d/1dTq4EZmYsfl4C8zsNYsT1dRwB37Os9RW/edit"
    df = conn.read(spreadsheet=url, usecols=None)
    
    # Clean column names
    df.columns = df.columns.str.strip()
    return df

# --- UI & LOGIC ---
def main():
    # Load data
    try:
        df = load_data()
        # Debugging: show columns if they don't match expected names
        if not all(col in df.columns for col in ['Make', 'Model', 'Year Range']):
            st.error(f"Column Mismatch! Expected 'Make', 'Model', 'Year Range'. Found: {df.columns.tolist()}")
            return
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return

    # Clean Model logic
    df['Clean_Model'] = df['Model'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', str(x)).strip())
    
    # Session State
    if 'show_results' not in st.session_state: st.session_state.show_results = False

    # Search Interface
    if not st.session_state.show_results:
        st.subheader("Search Specs")
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
        # Results Interface
        if len(st.session_state.results) == 1:
            st.subheader("Vehicle Details")
            record = st.session_state.results.iloc[0]
            for col in st.session_state.results.columns:
                if col in ['Clean_Model', 'Model', 'Make']: continue
                st.markdown(f"**{col}:**")
                st.write(str(record[col]))
        else:
            st.subheader(f"Found {len(st.session_state.results)} Results")
            for idx, row in st.session_state.results.iterrows():
                if st.button(f"{row['Make']} | {row['Model']} | {row['Year Range']}", key=str(idx)):
                    st.session_state.results = st.session_state.results.loc[[idx]]
                    st.rerun()
        
        if st.button("⬅ Back to Search"):
            st.session_state.show_results = False
            st.rerun()

if __name__ == "__main__":
    main()
