import streamlit as st
import pandas as pd
import re
import os

# --- CONFIG ---
st.set_page_config(page_title="Recovery Specs", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4, p, label { color: #ffffff !important; }
    
    /* Main Search Button */
    div[data-testid="stVerticalBlock"] div.stButton > button { 
        background-color: #f6782a !important; 
        color: white !important; 
        width: 100%; 
        font-weight: bold; 
    }
    
    /* List View Buttons */
    div[data-testid="stButton"] button { 
        background-color: #333333 !important; 
        color: white !important;
        border: 1px solid #555555;
    }

    .result-header {
        font-size: 1.25em !important;
        color: #f6782a !important;
        font-weight: bold;
        margin-bottom: -5px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- HELPERS ---
def save_new_vehicle_request(data_dict):
    df_new = pd.DataFrame([data_dict])
    file_path = "New_Vehicle_Requests.xlsx"
    if os.path.exists(file_path):
        df_existing = pd.read_excel(file_path)
        df_new = pd.concat([df_existing, df_new], ignore_index=True)
    df_new.to_excel(file_path, index=False)

@st.cache_data(ttl=60)
def load_data():
    if not os.path.exists("Vehicle_Library_Populated.xlsx"):
        st.error("Excel file not found!")
        return pd.DataFrame()
    df = pd.read_excel("Vehicle_Library_Populated.xlsx")
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
    selected_make = st.selectbox("MAKE", options=[""] + sorted(df['Make'].dropna().unique()))
    
    filtered_by_make = df if not selected_make else df[df['Make'] == selected_make]
    selected_model = st.selectbox("MODEL", options=[""] + sorted(filtered_by_make['Clean_Model'].unique()))
    
    filtered_by_model = filtered_by_make if not selected_model else filtered_by_make[filtered_by_make['Clean_Model'] == selected_model]
    selected_year = st.selectbox("YEAR RANGE", options=[""] + sorted(filtered_by_model['Year Range'].unique()))

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
            details = st.text_area("Details (e.g. jacking points, battery location)")
            if st.form_submit_button("Send Request"):
                save_new_vehicle_request({"Make": make, "Model": model, "Year": year, "Details": details})
                st.success("Request sent to management!")

else:
    final_df = st.session_state.results
    if len(final_df) == 1:
        st.subheader("Vehicle Details")
        record = final_df.iloc[0]
        row_id = record.name 
        updated = False
        
        for col in final_df.columns:
            if col != 'Clean_Model':
                val = str(record[col])
                if val.lower() == 'nan' or val.strip() == "":
                    st.markdown(f'<p class="result-header">{col}:</p>', unsafe_allow_html=True)
                    if "Photo" in col or "Jacking" in col:
                        choice = st.radio(f"Action for {col}:", ["---", "Upload Photo", "Take New Photo"], key=f"radio_{row_id}_{col}")
                        photo_file = None
                        if choice == "Upload Photo":
                            photo_file = st.file_uploader(f"Choose file", type=['jpg', 'png'], key=f"up_{row_id}_{col}")
                        elif choice == "Take New Photo":
                            photo_file = st.camera_input(f"Camera", key=f"cam_{row_id}_{col}")
                        if photo_file:
                            os.makedirs("uploads", exist_ok=True)
                            path = f"uploads/{row_id}_{col}.jpg"
                            with open(path, "wb") as f: f.write(photo_file.getbuffer())
                            st.session_state.df.at[row_id, col] = path
                            updated = True
                    else:
                        new_val = st.text_input(f"Add note for {col}", key=f"inp_{col}")
                        if new_val:
                            st.session_state.df.at[row_id, col] = new_val
                            updated = True
                else:
                    st.markdown(f'<p class="result-header">{col}:</p>', unsafe_allow_html=True)
                    if str(val).startswith("uploads/"): st.image(val, use_container_width=True)
                    else: st.write(val)
        
        if updated and st.button("💾 Save Changes"):
            st.session_state.df.to_excel("Vehicle_Library_Populated.xlsx", index=False)
            st.success("Database updated!")
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
