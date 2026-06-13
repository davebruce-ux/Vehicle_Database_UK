import streamlit as st
import pandas as pd
import re
import requests

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Recovery Specs", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    h1, h2, h3, h4, p, label { color: #ffffff !important; }
    
    /* Global Button Styling - Orange and Uniform */
    div.stButton > button { 
        background-color: #f6782a !important; 
        color: white !important; 
        font-weight: bold; 
        border: none !important;
    }
    
    /* Submit Form Button Styling */
    div[data-testid="stFormSubmitButton"] button { 
        background-color: #f6782a !important; 
        color: white !important; 
        font-weight: bold; 
        border: 2px solid #ffffff !important;
    }

    .result-header { font-size: 1.25em !important; color: #f6782a !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=600)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1dTq4EZmYsfl4C8zsNYsT1dRwB37Os9RW/gviz/tq?tqx=out:csv&sheet=Sheet1"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

def main():
    col1, col2, col3 = st.columns([1, 4, 1]) 
    with col2:
        st.image("WhatsApp Image 2026-06-09 at 15.53.35.jpeg", use_container_width=True)

    df = load_data()
    if 'Model' in df.columns:
        df['Clean_Model'] = df['Model'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', str(x)).strip())
    
    if 'show_results' not in st.session_state: st.session_state.show_results = False

    if not st.session_state.show_results:
        st.subheader("Search Specs")
        
        selected_make = st.selectbox("MAKE", options=[""] + sorted(df['Make'].dropna().unique().astype(str)))
        filtered_by_make = df if not selected_make else df[df['Make'] == selected_make]
        
        selected_model = st.selectbox("MODEL", options=[""] + sorted(filtered_by_make['Clean_Model'].unique().astype(str)))
        filtered_by_model = filtered_by_make if not selected_model else filtered_by_make[filtered_by_model['Clean_Model'] == selected_model]
        
        selected_year = st.selectbox("YEAR RANGE", options=[""] + sorted(filtered_by_model['Year Range'].unique().astype(str)))

        if st.button("🔍 SEARCH SPECS", use_container_width=True):
            st.session_state.results = filtered_by_model[filtered_by_model['Year Range'] == selected_year] if selected_year else filtered_by_model
            st.session_state.show_results = True
            st.rerun()
            
        st.divider()
        with st.expander("➕ Report a missing vehicle"):
            with st.form("new_vehicle_form", clear_on_submit=True):
                make = st.text_input("Make")
                model = st.text_input("Model")
                year = st.text_input("Year Range")
                details = st.text_area("Details")
                
                if st.form_submit_button("Send Request", use_container_width=True):
                    url = "https://script.google.com/macros/s/AKfycbwBAgimuEZD_reXRyS1YETk0Le2-6JiZyYNccQ4fC6RQoLcUwvzTFEAVBBWLH3-jbI6dQ/exec"
                    try:
                        payload = {"make": make, "model": model, "year": year, "details": details}
                        response = requests.post(url, json=payload, timeout=10)
                        if response.status_code == 200:
                            st.success("Request sent successfully!")
                        else:
                            st.error(f"Error: Server returned {response.status_code}")
                    except Exception as e:
                        st.error(f"Connection failed: {str(e)}")
    else:
        results = st.session_state.results
        if len(results) == 1:
            st.subheader("Vehicle Details")
            record = results.iloc[0]
            
            # --- Permanently Visible Info ---
            st.markdown(f"**Year Range:** {record.get('Year Range', 'N/A')}")
            st.markdown(f"**Fuel Type:** {record.get('Fuel Type', 'N/A')}")
            st.markdown(f"**Drivetrain:** {record.get('Drivetrain', 'N/A')}")
            
            # --- Expandable Sections with Uploads ---
            with st.expander("🔋 Battery Information"):
                st.markdown(f"**Location:** {record.get('Battery Location', 'N/A')}")
                st.write("**Photo:** " + str(record.get('Battery Photo', 'N/A')).replace('nan', 'No photo uploaded'))
                st.link_button("📸 Upload Battery Photo", "https://forms.gle/dCe6WGz9yiZmjsht8", use_container_width=True)

            with st.expander("🔌 OBD Port Information"):
                st.markdown(f"**Location:** {record.get('OBD Location', 'N/A')}")
                st.write("**Photo:** " + str(record.get('ODB Photo', 'N/A')).replace('nan', 'No photo uploaded'))
                st.link_button("📸 Upload OBD Photo", "https://forms.gle/dCe6WGz9yiZmjsht8", use_container_width=True)
                
            with st.expander("🚗 Jacking Points"):
                st.markdown(f"**Location:** {record.get('Jacking Points', 'N/A')}")
                st.write("**Photo:** " + str(record.get('Jacking point Photo', 'N/A')).replace('nan', 'No photo uploaded'))
                st.link_button("📸 Upload Jacking Photo", "https://forms.gle/dCe6WGz9yiZmjsht8", use_container_width=True)
            
        else:
            st.subheader(f"Found {len(results)} Results")
            for idx, row in results.iterrows():
                if st.button(f"{row['Make']} | {row['Model']} | {row['Year Range']}", key=str(idx), use_container_width=True):
                    st.session_state.results = results.loc[[idx]]
                    st.rerun()
        
        st.divider()
        if st.button("⬅ Back to Search", use_container_width=True):
            st.session_state.show_results = False
            st.rerun()

if __name__ == "__main__":
    main()
