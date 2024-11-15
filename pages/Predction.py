import streamlit as st
import docx2txt
import fitz  # PyMuPDF for PDF text extraction
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the trained classifier and TfidfVectorizer
clf = pickle.load(open('clf.pkl', 'rb'))
tfidf = pickle.load(open('tfidf.pkl', 'rb'))

category_mapping = {
    0: "Advocate", 1: "Arts", 2: "Automation Testing", 3: "Blockchain",
    4: "Business Analyst", 5: "Civil Engineer", 6: "Data Science", 7: "Database",
    8: "DevOps Engineer", 9: "DotNet Developer", 10: "ETL Developer",
    11: "Electrical Engineering", 12: "HR", 13: "Hadoop", 14: "Health and fitness",
    15: "Android Developer", 16: "Mechanical Engineer", 17: "Network Security Engineer",
    18: "Operations Manager", 19: "PMO", 20: "Python Developer", 21: "SAP Developer",
    22: "Sales", 23: "Testing", 24: "Web Designing", 25: "Law Enforcement",
    26: "Logistics", 27: "Real Estate", 28: "Hospitality", 29: "Information Technology",
    30: "Insurance", 31: "Finance", 32: "Marketing", 33: "Healthcare", 34: "Education"
}

def extract_text_from_docx(uploaded_file):
    """Extracts text from a DOCX file."""
    return docx2txt.process(uploaded_file)

def extract_text_from_pdf(uploaded_file):
    """Extracts text from a PDF file stream."""
    text = ""
    pdf_document = fitz.open("pdf", uploaded_file.read())  # Pass binary content instead of a path
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")
    return text

def filter_relevant_text(text):
    """Filters relevant information based on keywords and sections commonly found in resumes."""
    lines = text.split('\n')
    relevant_lines = []
    capture = False

    for line in lines:
        if re.search(r"(experience|education|skills|projects|achievements|certifications)", line, re.IGNORECASE):
            capture = True
        elif re.search(r"(dear|sincerely|regards|contact|phone|email|linkedin)", line, re.IGNORECASE):
            capture = False

        if capture:
            relevant_lines.append(line)

    return "\n".join(relevant_lines)

def main():
    st.title(":blue[Upload] :green[your] :red[resume]")
    uploaded_file = st.file_uploader(":red[Upload a resume:]", key="resume_uploader", type=['pdf', 'docx'])

    if uploaded_file is not None:
        try:
            # Extract text based on file type
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = extract_text_from_docx(uploaded_file)
            
            # Display filtered relevant text
            relevant_text = filter_relevant_text(resume_text)
            # st.write("**Relevant Text from Resume:**")
            # st.text_area("Filtered Text", relevant_text, height=300)

            # Process the relevant text for prediction
            input_features = tfidf.transform([relevant_text])
            prediction_id = clf.predict(input_features)[0]

            # Map prediction to category
            category_name = category_mapping.get(prediction_id, "Unknown")
            st.header(":red[Predicted Category:]")
            st.markdown(f"**{category_name}**")

        except UnicodeDecodeError:
            st.write(":red[Error: Unable to read the file. Please ensure it is in a readable format.]")

if __name__ == "__main__":
    main()
