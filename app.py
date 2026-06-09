import streamlit as st
import pandas as pd

# --- CONFIG (Must be the first Streamlit command) ---
st.set_page_config(page_title="Recovery Specs Pro", layout="wide")

# --- ADD LOGO ---
# st.image("641c5719-41d0-40ec-adc9-eb3a3e763903.png", width=300)

st.title("🚗 Recovery Specs - Field Operations")

# --- LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    # This reads the file currently in your repository
    df = pd.read_excel("Vehicle_Library_Populated.xlsx")
    return df

try:
    df = load_data()
    
    # --- SEARCH ---
    search_term = st.text_input("🔍 Search for a vehicle (Make or Model):", "")
    
    if search_term:
        # Filters the dataframe based on Make or Model
        filtered_df = df[df['Make'].str.contains(search_term, case=False, na=False) | 
                         df['Model'].str.contains(search_term, case=False, na=False)]
    else:
        filtered_df = df

    st.write(f"Showing {len(filtered_df)} results:")
    st.dataframe(filtered_df)

    # --- ADD CONTRIBUTION ---
    st.divider()
    st.subheader("📝 Add Field Notes/Photos")
    st.write("Use this section to record details for future reference.")
    
    # Check if results exist before creating selectbox
    if not filtered_df.empty:
        selected_vehicle = st.selectbox("Select Vehicle to update:", filtered_df['Make'].astype(str) + " " + filtered_df['Model'].astype(str))
        comment = st.text_area("Technician Comments:")
        photo_url = st.text_input("Photo Link (or notes):")

        if st.button("Submit Update"):
            st.success(f"Update submitted for {selected_vehicle}!")
            st.info("Note: To save this data permanently to your Master Sheet, ensure your app is connected to a live Google Sheet via 'gspread'.")
    else:
        st.warning("No vehicles found to update.")

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.write("Please ensure 'Vehicle_Library_Populated.xlsx' is in the same folder as 'app.py'.")
