import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="BadrAI Demo",
    page_icon="images/badr-small-logo.jpg",
    layout="wide"
)

col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.image("images/Logo-Badr-Interactive.png", width=400) 