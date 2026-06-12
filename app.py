import streamlit as st
import pandas as pd
import re

# --- CONFIG ---
st.set_page_config(page_title="Recovery Specs", layout="centered")

# --- DATA HANDLER ---
@st.cache_data(ttl=600)
def load_data():
    # Direct CSV export URL from your Google Sheet
    url = "https://docs.google.com/spreadsheets/d/1dTq4EZmYsfl4C8zsNYsT1dRwB37Os9RW/gviz/tq?tqx=out:csv&sheet=Sheet1"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

# --- MAIN APP ---
def main():
    # Logo Display
    col1, col2, col3 = st.columns([1, 4, 1]) 
    with col2:
        try:
            st.image("WhatsApp Image 2026-06-09 at 15.53.35.jpeg", use_container_width=True)
        except:
            st.warning("Logo image not found in repository.")

    # Data Loading
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return

    # Clean Model for search logic
    if 'Model' in df.columns:
        df['Clean_Model'] = df['Model'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', str(x)).strip())
    
    # State Management
    if 'show_results' not in st.session_state: st.session_state.show_results = False

    # Search Logic
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

    # Results Logic
    else:
        results = st.session_state.results
        if len(results) == 1:
            st.subheader("Vehicle Details")
            record = results.iloc[0]
            for col in results.columns:
                if col in ['Clean_Model', 'Model', 'Make']: continue
                st.markdown(f"**{col}:**")
                st.write(str(record[col]))
        else:
            st.subheader(f"Found {len(results)} Results")
            for idx, row in results.iterrows():
                if st.button(f"{row['Make']} | {row['Model']} | {row['Year Range']}", key=str(idx)):
                    st.session_state.results = results.loc[[idx]]
                    st.rerun()
        
        if st.button("⬅ Back to Search"):
            st.session_state.show_results = False
            st.rerun()

if __name__ == "__main__":
    main()
