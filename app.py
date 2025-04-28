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
def get_image_details(uploaded_file, page_number=None):
    mime_type = uploaded_file.type
    file_bytes = uploaded_file.getvalue()

    if mime_type == "application/pdf":
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        
        # Handle multi-page PDF case
        num_pages = len(reader.pages)
        
        if page_number is None:
            # Extract text from all pages
            pdf_text = ""
            for i in range(num_pages):
                pdf_text += reader.pages[i].extract_text()
        else:
            # Extract text from the specified page
            if 0 <= page_number < num_pages:
                pdf_text = reader.pages[page_number].extract_text()
            else:
                pdf_text = "Page not found."

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
    return image_part, mime_type, file_bytes, num_pages

# Function to get response
def get_resp(user_input, image_part, prompt):
    response = model.generate_content([user_input, image_part, prompt])
    return response.text

st.set_page_config(page_title="Invoice Extractor")
st.header("🧾 Invoice Extractor Application")

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
        st.warning("⚠️ Please upload an invoice file.")
    elif user_input.strip() == "":
        st.warning("⚠️ Please enter what information you want to extract.")
    else:
        page_number = st.number_input("Select the page number (0 for first page)", min_value=0, step=1)
        
        image_part, mime_type, file_bytes, num_pages = get_image_details(uploaded_file, page_number)

        # If uploaded file is an image, display it
        if mime_type.startswith("image/"):
            st.image(io.BytesIO(file_bytes), caption="Uploaded Invoice", use_column_width=True)
        else:
            st.info(f"📄 PDF Uploaded: Extracted text from page {page_number+1} of {num_pages}.")

        with st.spinner("Extracting information..."):
            response_text = get_resp(user_input, image_part, system_prompt)

        st.subheader("Extracted Information:")
        st.write(response_text)

