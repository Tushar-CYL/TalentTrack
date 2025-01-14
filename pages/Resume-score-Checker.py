# from dotenv import load_dotenv

# load_dotenv()
# import base64
# import streamlit as st
# import os
# import io
# from PIL import Image 
# import pdf2image
# import google.generativeai as genai

# GOOGLE_API_KEY = 'AIzaSyAhPdM6jGrv-CTRuI6tqOrd4qXmyObJnpY'
# genai.configure(api_key=GOOGLE_API_KEY)

# def get_gemini_response(input,pdf_cotent,prompt):
#     model=genai.GenerativeModel('gemini-1.5-flash')
#     response=model.generate_content([input,pdf_content[0],prompt])
#     return response.text

# def input_pdf_setup(uploaded_file):
#     if uploaded_file is not None:
#         ## Convert the PDF to image
#         images=pdf2image.convert_from_bytes(uploaded_file.read())

#         first_page=images[0]

#         # Convert to bytes
#         img_byte_arr = io.BytesIO()
#         first_page.save(img_byte_arr, format='JPEG')
#         img_byte_arr = img_byte_arr.getvalue()

#         pdf_parts = [
#             {
#                 "mime_type": "image/jpeg",
#                 "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
#             }
#         ]
#         return pdf_parts
#     else:
#         raise FileNotFoundError("No file uploaded")

# ## Streamlit App

# st.set_page_config(page_title="ATS Resume EXpert")
# st.header("ATS Tracking System")
# input_text=st.text_area("Job Description: ",key="input")
# uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


# if uploaded_file is not None:
#     st.write("PDF Uploaded Successfully")


# submit1 = st.button("Tell Me About the Resume")

# #submit2 = st.button("How Can I Improvise my Skills")

# submit3 = st.button("Percentage match")

# input_prompt1 = """
#  You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
#   Please share your professional evaluation on whether the candidate's profile aligns with the role. 
#  Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
# """

# input_prompt3 = """
# You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
# your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
# the job description. First the output should come as percentage and then keywords missing and last final thoughts.
# """

# if submit1:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(input_prompt1,pdf_content,input_text)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")

# elif submit3:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(input_prompt3,pdf_content,input_text)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")




from dotenv import load_dotenv
load_dotenv()
import base64
import streamlit as st
import os
import io
import PyPDF2
from PIL import Image
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = 'AIzaSyATZ0NDoTweYu3S3KQBlLBo0PljHvViK30'  # Replace with your API key
genai.configure(api_key=GOOGLE_API_KEY)

def convert_pdf_to_image(pdf_file):
    """Convert PDF to base64 encoded text content"""
    try:
        # Read PDF content
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text_content = ""
        
        # Extract text from all pages
        for page in pdf_reader.pages:
            text_content += page.extract_text()

        # Create a simple representation
        pdf_parts = [
            {
                "mime_type": "text/plain",
                "data": base64.b64encode(text_content.encode('utf-8')).decode()
            }
        ]
        return pdf_parts, text_content
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None, None

def get_gemini_response(input_prompt, pdf_content, job_desc):
    """Get response from Gemini model"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([
            input_prompt,
            f"Resume Content: {pdf_content}",
            f"Job Description: {job_desc}"
        ])
        return response.text
    except Exception as e:
        return f"Error in generating response: {str(e)}"

# Streamlit UI
def main():
    st.set_page_config(page_title="ATS Resume Expert", layout="wide")
    
    # Header and description
    st.title("🎯 ATS Resume Analyzer")
    st.markdown("""
    Upload your resume and job description to get:
    - Detailed resume analysis
    - Match percentage
    - Improvement suggestions
    """)

    # Input sections
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Upload Resume")
        uploaded_file = st.file_uploader("Upload your resume (PDF format only)", type=["pdf"])
        
        if uploaded_file:
            st.success("Resume uploaded successfully!")

    with col2:
        st.subheader("💼 Job Description")
        job_description = st.text_area(
            "Paste the job description here",
            height=200,
            key="job_desc"
        )

    # Analysis prompts
    resume_analysis_prompt = """
    As an experienced Technical Human Resource Manager, analyze this resume against the job description.
    Provide a detailed evaluation covering:
    1. Overall profile alignment
    2. Key strengths matching the role
    3. Areas where the candidate excels
    4. Potential areas for improvement
    5. Technical skills assessment
    6. Experience relevance
    
    Format your response in clear sections with bullet points where appropriate.
    """

    match_analysis_prompt = """
    As an ATS (Applicant Tracking System) expert, analyze this resume against the job description.
    Provide the following in order:
    1. MATCH PERCENTAGE: [X]%
    2. MATCHING KEYWORDS: [List all matching keywords found]
    3. MISSING KEYWORDS: [List important keywords not found in resume]
    4. RECOMMENDATIONS: [Specific suggestions to improve the match]
    5. FINAL THOUGHTS: [Brief overall assessment]
    
    Start with the match percentage as a number, then provide detailed analysis in the sections above.
    """

    # Analysis buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        analyze_button = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)
    with col2:
        match_button = st.button("📊 Check Match %", type="primary", use_container_width=True)
    
    # Process and display results
    if uploaded_file is not None and (analyze_button or match_button):
        with st.spinner("Analyzing your resume..."):
            # Reset the file pointer to the beginning
            uploaded_file.seek(0)
            
            # Convert PDF to text content
            pdf_parts, text_content = convert_pdf_to_image(uploaded_file)
            
            if text_content:
                if analyze_button:
                    st.subheader("📋 Detailed Analysis")
                    response = get_gemini_response(resume_analysis_prompt, text_content, job_description)
                    st.markdown(response)
                    
                elif match_button:
                    st.subheader("🎯 Match Analysis")
                    response = get_gemini_response(match_analysis_prompt, text_content, job_description)
                    
                    # Try to extract percentage for progress bar
                    try:
                        percentage = int(''.join(filter(str.isdigit, response.split('%')[0])))
                        st.progress(percentage / 100)
                        st.metric("Match Percentage", f"{percentage}%")
                    except:
                        pass
                        
                    st.markdown(response)
    
    # Error handling
    elif analyze_button or match_button:
        if not uploaded_file:
            st.error("Please upload your resume first!")
        if not job_description:
            st.warning("Please provide the job description for better analysis.")

if __name__ == "__main__":
    main()
