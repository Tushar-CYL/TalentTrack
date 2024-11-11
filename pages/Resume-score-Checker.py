from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = 'AIzaSyAhPdM6jGrv-CTRuI6tqOrd4qXmyObJnpY'
genai.configure(api_key=GOOGLE_API_KEY)


def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            # Explicitly set the Poppler path
            poppler_path = r"C:\Users\tusha\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"  # Replace with your actual Poppler path
            images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)

            first_page = images[0]

            # Convert the first page to bytes
            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            # Prepare the base64-encoded image data
            pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
                }
            ]
            return pdf_parts

        except pdf2image.exceptions.PDFInfoNotInstalledError as e:
            raise FileNotFoundError("Poppler is not installed or not found in PATH. Please install it to proceed.")
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Input fields for job description and resume
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Define action buttons
submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

# Define prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage, then keywords missing, and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        except FileNotFoundError as e:
            st.write(e)

elif submit3:
    if uploaded_file is not None:
        try:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        except FileNotFoundError as e:
            st.write(e)
