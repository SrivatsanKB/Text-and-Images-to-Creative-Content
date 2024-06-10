import sys
from exception import CustomException
from logger import logging  # Import the configured logger
import streamlit as st
import os
from pathlib import Path 
import textwrap
from PIL import Image
import google.generativeai as genai
import pyttsx3
from dotenv import load_dotenv

# Load environment variables
env_loaded = load_dotenv() 
if env_loaded:
    logging.info("Environment variables loaded.")
else:
    logging.error("Environment variables not loaded.")

# Configure generative AI API
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    logging.error("API key not found or empty.")

def to_markdown(text):
    text = textwrap.dedent(text)
    text = "#" "\n" + text.replace("•", "*")
    return text

def get_gemini_response(text_prompt, images):
    try:
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([text_prompt] + images)
        response.resolve()
        final_response = to_markdown(response.text)
        logging.info("Response generated.")
        return final_response
    except Exception as e:
        raise CustomException(e, sys)

def generate_audio_pyttsx3(text, filename):
    try:
        engine = pyttsx3.init()
        engine.save_to_file(text, filename)
        engine.runAndWait()
        logging.info("Audio generated using pyttsx3.")
    except Exception as e:
        raise CustomException(e, sys)

# Initialize Streamlit app
st.set_page_config(page_title="Re-Imagine")
logging.info("Streamlit app initialized.")

st.header("Welcome to Re-imagine App")
st.write("An app that transforms your photos and texts into creative content.")
st.warning("This project is done by SRIVATSAN K B")

# Create a sidebar
sidebar = st.sidebar

# Get the text prompt from the user
input_text = sidebar.text_input("Text Prompt: ", key="input")
logging.info(f"User input: {input_text}")

# Get multiple images from the user
uploaded_files = sidebar.file_uploader("Choose Images: ", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
images = []
if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            image = Image.open(uploaded_file)
            images.append(image)
            sidebar.image(image, caption="Uploaded Image", use_column_width=True)
        except IOError as e:
            logging.error(e)
            sidebar.error(f"An error occurred: {e}")

# Get the output format from the user
output_format = sidebar.radio("Output Format: ", options=["Markdown", "Plain Text"], index=0)

# Create an animated button with an emoji
button_css = st.markdown("""
<style>
@keyframes pulse {
  0% { transform: scale(0.95); }
  70% { transform: scale(1.05); }
  100% { transform: scale(0.95); }
}
.stButton>button {
  animation: pulse 2s infinite;
  font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

submit = st.button("👉 Tell me..", key="submit")

if submit:
    try:
        with st.spinner('Generating response...'):
            response_text = get_gemini_response(input_text, images)
            st.subheader("The Response is")
            if output_format == "Markdown":
                st.markdown(response_text)
            else:
                st.text(response_text)

            response_file = "response.md"
            with open(response_file, "w") as file:
                file.write(response_text)

            audio_file = "response.mp3"
            generate_audio_pyttsx3(response_text, audio_file)

            st.download_button(label="Download the response", data=open(response_file).read(), file_name=response_file, mime="text/markdown")
            st.audio(audio_file, format="audio/mp3", start_time=0)
    except CustomException as e:
        logging.error(e)
        st.error(f"An error occurred: {e.message}")
    except Exception as e:
        logging.error(e)
        st.error(f"An error occurred: {e}")

footer_css = st.markdown("""
<style>
.footer {
  position: fixed;
  bottom: 0;
  right: 0;
  padding: 10px;
  color: white;
  font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

footer = st.markdown("""
<div class="footer">
Created by : Srivatsan K B
</div>
""", unsafe_allow_html=True)
