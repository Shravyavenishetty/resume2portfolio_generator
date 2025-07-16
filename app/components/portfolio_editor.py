import streamlit as st
import json

def portfolio_editor(parsed_data):
    st.header("Edit Resume Data")
    code = st.text_area("Resume Data (JSON)", json.dumps(parsed_data, indent=2), height=400)
    try:
        return json.loads(code)
    except json.JSONDecodeError:
        st.error("Invalid JSON format")
        return parsed_data