import streamlit as st
import pandas as pd
import re

# --- CONFIG ---
st.set_page_config(page_title="Recovery Specs", layout="centered")

# --- DATA HANDLER ---
@st.cache_data(ttl=600)
def load_data():
    # This URL format is a direct CSV export from Google Sheets
    # It works perfectly with 'Anyone with the link can view'
    url = "https://docs.google.com/spreadsheets/d/1dTq4EZmYsfl4C8zsNYsT1dRwB37Os9RW/gviz/tq?tqx=out:csv&sheet=Sheet1"
    df = pd.read_csv(url)
    
    # Clean column names (removes hidden whitespace)
    df.columns = df.columns.str.strip()
    return df

# --- MAIN APP LOGIC ---
def main():
    # 1. Load data safely
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return

    # 2. Add 'Clean_Model' for searching if 'Model' exists
    if 'Model' in df.columns:
        df['Clean_Model'] = df['Model'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', str(x)).strip())
    
    # 3. Session State Management
    if 'show_results' not in st.session_state: st.session_state.show_results = False

    # 4. Search UI
    if not st.session_state.show_results:
        st.subheader("Search Specs")
        
        # Dropdowns
        make_options = [""] + sorted(df['Make'].dropna().unique().astype(str))
        selected_make = st.selectbox("MAKE", options=make_options)
        
        filtered_by_make = df if not selected_make else df[df['Make'] == selected_make]
        
        model_options = [""] + sorted(filtered_by_make['Clean_Model'].unique().astype(str))
        selected_model = st.selectbox("MODEL", options=model_options)
        
        filtered_by_model = filtered_by_make if not selected_model else filtered_by_make[filtered_by_model['Clean_Model'] == selected_model]
        
        year_options = [""] + sorted(filtered_by_model['Year Range'].unique().astype(str))
        selected_year = st.selectbox("YEAR RANGE", options=year_options)

        if st.button("🔍 SEARCH SPECS", use_container_width=True):
            st.session_state.results = filtered_by_model[filtered_by_model['Year Range'] == selected_year] if selected_year else filtered_by_model
            st.session_state.show_results = True
            st.rerun()

    # 5. Display Results
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
