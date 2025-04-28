Invoice Extractor Application
Link:https://invoiceextractor-ig9shxgboixqxnujh9yml6.streamlit.app/
This is a simple Streamlit web application that allows users to upload a single-page invoice (image or PDF) and extract specific information based on a user prompt.

It uses Google's Gemini 2.5 Flash model to smartly understand the invoice content and fetch only the details you ask for.

🚀 Features
Upload invoice images (.jpg, .jpeg, .png) or PDF invoices (only the first page is processed).

Extract only requested information based on user input.

Handles missing fields gracefully with "Not Found" responses.

Easy-to-use Streamlit interface.

Fast and efficient using Google Generative AI.

🛠️ Technologies Used
Python

Streamlit

Google Generative AI (gemini-2.5-flash-preview-04-17)

PyPDF2 (for reading PDFs)

PIL (for image processing)

dotenv (for securely managing API keys)

