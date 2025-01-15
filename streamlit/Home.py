import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="BadrAI Demo",
    page_icon="images/badr-small-logo.jpg",
    layout="wide"
)

col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.image("images/Logo-Badr-Interactive.png", width=300) 

st.write("""
We are excited to introduce our new application featuring both a chatbot and an automatic report generator powered by Generative AI (GenAI). 
By harnessing the capabilities of GenAI, we aim to elevate the user experience and provide a more engaging, interactive environment that goes beyond the traditional dashboard. 
With deeper, personalized insights and a dynamic flow of information, users can explore data in fresh and intuitive ways while saving time and effort.
""")