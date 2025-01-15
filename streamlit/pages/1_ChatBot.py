import os
import json
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from streamlit_lottie import st_lottie_spinner

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
url = os.getenv("backend_url") + "/api_chat"


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










############################################################### DATA ###############################################################




with st.container():

    # Add buttons for possible questions
    if language == "English":
        possible_questions = [
            "What is the total power usage for each region in the last 30 days?",
            "What is the average usage for each region over the last week?",
            "What building types that has the highest total usage for the current month?",
            "For device with id 11, what were the minimum, maximum, and average usage from 2025-01-01 to 2025-01-10?",
            "Which 5 devices consumed the most power during the last month?",
            "For customer with id 7, how is the daily usage distributed across all devices for the current week?",
            "What date was the highest usage recorded for device id 5 this month?",
            "Show bottom 5 customers with the lowest usage for the last 30 days? Show the region and building type."
        ]
    else:
        possible_questions = [
            "Berapa total penggunaan daya untuk setiap wilayah dalam 30 hari terakhir?",
            "Berapa rata-rata penggunaan untuk setiap wilayah dalam 7 hari terakhir?",
            "Jenis bangunan apa saja yang memiliki penggunaan daya tertinggi untuk bulan ini?",
            "Untuk perangkat dengan id 11, berapa penggunaan minimum, maksimum, dan rata-rata dari 2025-01-01 hingga 2025-01-10?",
            "Tunjukkan 5 perangkat yang paling banyak menggunakan daya dalam 1 bulan terakhir?",
            "Untuk pelanggan dengan id 7, bagaimana distribusi penggunaan daya harian di semua perangkat untuk minggu ini?",
            "Pada tanggal berapa penggunaan daya tertinggi tercatat untuk perangkat id 5 bulan ini?",
            "Tampilkan 5 pelanggan terbawah dengan penggunaan terendah untuk 30 hari terakhir? Tampilkan juga wilayah dan jenis bangunannya."
        ]

    # Create a column layout for the buttons
    button_cols = st.columns(4)  # Adjust the number of columns as needed

    for i, question in enumerate(possible_questions):
        if button_cols[i % 4].button(question):
            # Store the question and process it immediately
            prompt = question
            if prompt:
                # Update the payload with the history
                payload = { "query": prompt, "language": language}

                # Initialize messages if not exists
                if 'messages' not in st.session_state:
                    st.session_state.messages = []

                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    # Rest of your API call code...
                    message_placeholder = st.empty()

                    with st_lottie_spinner(lottie, height=60):
                        with requests.post(url, json=payload, stream=True) as response:
                            # Check if the request was successful
                            if response.status_code == 200:
                                # Initialize an empty string to accumulate the response
                                accumulated_response = ""

                                for chunk in response.iter_content(chunk_size=1024):
                                    if chunk:
                                        # Decode the chunk
                                        decoded_chunk = chunk.decode('utf-8')  # Ensure the chunk is decoded to a string

                                        # Process non-JSON lines for display (normal text part)
                                        accumulated_response += decoded_chunk

                                        # Add a blinking cursor to simulate typing
                                        message_placeholder.markdown(accumulated_response + "▌", unsafe_allow_html=True)

                                # Remove the cursor after the full response is received
                                message_placeholder.markdown(accumulated_response, unsafe_allow_html=True)

                                st.session_state.messages.append({"role": "assistant", "content": accumulated_response})

                            else:
                                st.error(f"Error: {response.status_code}")

# Fix chat input handling at the bottom
if prompt := st.chat_input("Question?"):

    # Update the payload with the history
    payload = {
        "query": prompt,
        "language": language,
    }

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
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
                    st.session_state.messages.append({"role": "assistant", "content": accumulated_response})
                else:
                    st.error(f"Error: {response.status_code}")