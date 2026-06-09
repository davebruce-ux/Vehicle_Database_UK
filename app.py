import streamlit as st
import pandas as pd
import re

# ... (Include your existing config and load_data function here)

# --- SEARCH BUTTON MODAL ---
if st.button("🔍 SEARCH SPECS"):
    # Filter the data
    results = df.copy()
    if selected_make: results = results[results['Make'] == selected_make]
    if selected_model: results = results[results['Clean_Model'] == selected_model]
    if selected_year: results = results[results['Year Range'] == selected_year]
    
    # Store results in session state
    st.session_state.results = results
    st.session_state.show_results = True

# --- MODAL DISPLAY ---
if st.session_state.get("show_results"):
    @st.dialog("Search Results")
    def show_modal():
        if not st.session_state.results.empty:
            st.dataframe(st.session_state.results.drop(columns=['Clean_Model']), use_container_width=True)
        else:
            st.error("No results found.")
        if st.button("Close"):
            st.session_state.show_results = False
            st.rerun()

    show_modal()
