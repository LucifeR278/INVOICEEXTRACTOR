from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configure Google Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("GOOGLE_API_KEY not found in environment variables.")
    st.stop()

# Initialize the Gemini Vision Model
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error initializing Gemini model: {e}")
    st.stop()

# Function to get response from Gemini
def get_gemini_response(input_text, image, user_prompt):
    try:
        response = model.generate_content([input_text, image[0], user_prompt])
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Function to process uploaded image
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        try:
            # Convert the file into bytes
            bytes_data = uploaded_file.getvalue()

            image_parts = [
                {
                    "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                    "data": bytes_data
                }
            ]
            return image_parts
        except Exception as e:
            st.error(f"Error processing image: {e}")
            return None
    else:
        st.error("No file uploaded.")
        return None

# Initialize the Streamlit app
st.set_page_config(page_title="MultiLanguage Invoice Extractor")

st.header("MultiLanguage Invoice Extractor")

# Input text prompt from the user
input_text = st.text_input("Input Prompt:", key="input")

# Image uploader for the invoice image
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])

# Display the uploaded image if available
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to submit and process the request
submit = st.button("Tell me about the invoice")

# Initial input prompt for the AI model
input_prompt = """
You are an expert in understanding invoices. We will upload an image as an invoice
and you will have to answer any questions based on the uploaded invoice image.
"""

# If the submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)

    if image_data:
        response = get_gemini_response(input_prompt, image_data, input_text)
        if response:
            st.subheader("The Response is:")
            st.write(response)
