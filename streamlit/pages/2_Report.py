import os
import json
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from streamlit_lottie import st_lottie_spinner
from report_queries import list_of_queries

import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*FigureCanvasAgg is non-interactive.*")


############################################################### SETUP ###############################################################

# Set page configuration
st.set_page_config(
    page_title="BadrAI Demo",
    page_icon="images/badr-small-logo.jpg",
    layout="wide"
)

# URL for the API endpoint
load_dotenv()
url = os.getenv("backend_url")


# Function to load Lottie animation from a JSON file
@st.cache_data
def get_lottie():
    with open('lottie/electric.json', 'r') as f:
        return json.load(f)

# Load the Lottie animation
lottie = get_lottie()


# Initialize session state variables at the beginning
if 'messages' not in st.session_state:
    st.session_state.messages = []

# header layout
col1, _, col2, col3 = st.columns([1, 1, 3, 1])
with col1:
    st.image("images/Logo-Badr-Interactive.png", width=150)
with col2:
    st.subheader("BadrAI Demo (PLN Use Case)")
with col3:
    language = st.selectbox("Language", ["English", "Bahasa Indonesia"])










############################################################### Generate Report ###############################################################




with st.container():
    # Single Generate Report button
    if st.button("Generate Report"):

        for query in list_of_queries:

            # Update the payload
            payload = {"query": query, "language": language, "response_type": "report", "number_of_sections": len(list_of_queries)}

            message_placeholder = st.empty()

            with st_lottie_spinner(lottie, height=60):
                with requests.post(url, json=payload, stream=True) as response:
                    if response.status_code == 200:
                        accumulated_response = ""
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                decoded_chunk = chunk.decode('utf-8')
                                accumulated_response += decoded_chunk
                                message_placeholder.markdown(accumulated_response + "▌", unsafe_allow_html=True)
                        
                        message_placeholder.markdown(accumulated_response, unsafe_allow_html=True)
                    else:
                        st.error(f"Error: {response.status_code}")