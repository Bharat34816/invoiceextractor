from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
import io
from PIL import Image
import PyPDF2

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

# Function to get image details properly (Image/PDF)
def get_image_details(uploaded_file):
    mime_type = uploaded_file.type
    file_bytes = uploaded_file.getvalue()

    if mime_type == "application/pdf":
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        # Extract text from the first page
        first_page = reader.pages[0]
        pdf_text = first_page.extract_text()
        image_part = {
            "mime_type": "text/plain",
            "data": pdf_text.encode("utf-8")
        }
    else:
        # For images (jpg/png/jpeg)
        image_part = {
            "mime_type": mime_type,
            "data": file_bytes
        }
    return image_part, mime_type, file_bytes

# Function to get response
def get_resp(user_input, image_part, prompt):
    response = model.generate_content([user_input, image_part, prompt])
    return response.text

st.set_page_config(page_title="Invoice Extractor")
st.header(" Invoice Extractor Application")

user_input = st.text_input("What do you want to extract from the invoice?", key="input")
uploaded_file = st.file_uploader("Upload an invoice (Image or PDF)...", type=["jpg", "jpeg", "png", "pdf"])

submit = st.button("Submit Invoice")

system_prompt = """
You are highly skilled at reading invoices and extracting requested information based on user input.
Answer only from the uploaded file.
If data is missing, say 'Not Found'.
"""

if submit:
    if uploaded_file is None:
        st.warning(" Please upload an invoice file.")
    elif user_input.strip() == "":
        st.warning(" Please enter what information you want to extract.")
    else:
        image_part, mime_type, file_bytes = get_image_details(uploaded_file)

        # If uploaded file is an image, display it
        if mime_type.startswith("image/"):
            st.image(io.BytesIO(file_bytes), caption="Uploaded Invoice", use_column_width=True)
        else:
            st.info("PDF Uploaded: Extracted text from first page.")

        with st.spinner("Extracting information..."):
            response_text = get_resp(user_input, image_part, system_prompt)

        st.subheader("Extracted Information:")
        st.write(response_text)
