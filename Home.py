# import streamlit as st
# import time

# # Header
# # st.header('Aim🔎Seeker', divider='rainbow')

# st.markdown("""
#     <div style="text-align:center;">
#         <h2>Aim🔎Seeker</h2>
#     </div>
# """, unsafe_allow_html=True)
# st.header('🔎', divider='rainbow')

# # Images
# col1, col2, col3 = st.columns(3)

# with col1:
#     st.image("./assets/Career _Isometric.png", use_column_width=True)

# with col2:
#     st.image("./assets/career.png", use_column_width=True)

# with col3:
#     st.image("./assets/Career _Outline.png", use_column_width=True)

# # Call to Action
# st.markdown("""
#     <div style="text-align:center; text-shadow: 3px 1px 2px purple;">
#       <h2>Ready to Shape Your Career?</h2>
#     </div>
# """, unsafe_allow_html=True)
# # st.header(':blue[_FutureForge_] :green[is] :red[Advanced and Unique] :crown:')
# st.page_link("pages/Find-Jobs.py",  icon="🛄")
# st.page_link("pages/Predction.py", icon="📌")
# # Introduction
# st.markdown("""
#     <div style="text-align:center; text-shadow: 3px 1px 2px purple;">
#       <h2>How to Use Aim🔎Seeker</h2>
#       <p>This platform helps you in finding the right career path and job opportunities based on your skills and preferences.</p>
#     </div>
# """, unsafe_allow_html=True)
# st.page_link("pages/New-User.py", icon="👩🏻‍🎓")
# st.page_link("pages/Resume-score-Checker.py", icon="📋")
# st.page_link("pages/About.py", icon="ℹ️")
# # Explanation

# st.markdown("""
#     <div style="text-align:center; text-shadow: 3px 1px 2px purple;">
#     <p><i><u> **Step 1:** Begin by uploading your CV/Resume and confirming your domain expertise.</u></i></p><br>
#    <p><i><u> **Step 2:** Once your domain is confirmed, you can search for companies relevant to your expertise.</u></i></p><br>
#     <p><i><u>**Step 3:** If you're a new user, complete all fields and confirm your domain to access the platform's features.</u></i></p>
#     </div>
# """, unsafe_allow_html=True)

# html3="""

#     <div style="color:yellow; margin:80px; text-align:center;">
#       Developed with 🎮🕹️👾 by <a href=https://github.com/Tushar-CYL>Tushar</a>
#       <a href=https://github.com/Tushar-CYL>Aritra</a>
#       <a href=https://github.com/Tushar-CYL>Anuj</a>
#       <a href=https://github.com/Tushar-CYL>Sunil</a>
#       <a href=https://github.com/Tushar-CYL>Rahul</a>
#     </div>
#       """
      
# st.markdown(html3,unsafe_allow_html=True)
# # st.write("""
# #     **Step 1:** Begin by uploading your CV/Resume and confirming your domain expertise.
    
# #     **Step 2:** Once your domain is confirmed, you can search for companies relevant to your expertise.
    
# #     **Step 3:** If you're a new user, complete all fields and confirm your domain to access the platform's features.
# # """)

# # Navigation Links
# # st.page_link("homea.py", label="Home", icon="🏠")





import streamlit as st
import time

st.set_page_config(
    page_title="Aim🔎Seeker",  # Title of the web app
    page_icon="🔎",           # Icon in the browser tab
    layout="wide"             # Use a wide layout
)

def streamlit_navbar():
    # Custom CSS for the navbar
    st.markdown("""
    <style>
    .navbar {
        display: flex;
        justify-content: space-around;
        background-color: #f1f1f1;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .navbar-item {
        text-decoration: none;
        color: #333;
        padding: 10px 15px;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }
    .navbar-item:hover {
        background-color: #e1e1e1;
    }
    .active {
        background-color: #6a11cb;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create a custom navbar using columns
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.page_link("Home.py", label="🏠 Home")
    
    with col2:
        st.page_link("pages/Find-Jobs.py", label="💼 Find Jobs")
    
    with col3:
        st.page_link("pages/Predction.py", label="📊 Predictions")
    
    with col4:
        st.page_link("pages/New-User.py", label="👥 New User")
    
    with col5:
        st.page_link("pages/Resume-score-Checker.py", label="📝 Resume Score")
    
    with col6:
        st.page_link("pages/About.py", label="ℹ️ About")

def main():
    # Add the navbar at the top of your page
    streamlit_navbar()
    
    # Markdown for header
    st.markdown("""
        <div style="text-align:center;">
            <h2>Aim🔎Seeker</h2>
        </div>
    """, unsafe_allow_html=True)
    st.header('🔎', divider='rainbow')
    
    # Images
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("./assets/Career _Isometric.png", use_column_width=True)
    with col2:
        st.image("./assets/career.png", use_column_width=True)
    with col3:
        st.image("./assets/Career _Outline.png", use_column_width=True)
    
    # Call to Action
    st.markdown("""
        <div style="text-align:center; text-shadow: 3px 1px 2px purple;">
          <h2>Ready to Shape Your Career?</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
        <div style="text-align:center;  white;">
          <h2>How to Use Aim🔎Seeker</h2>
          <p>This platform helps you in finding the right career path and job opportunities based on your skills and preferences.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Steps Explanation
    st.markdown("""
        <div style="text-align:center;  white;">
        <p><i><u> **Step 1:** Begin by uploading your CV/Resume and confirming your domain expertise.</u></i></p><br>
       <p><i><u> **Step 2:** Once your domain is confirmed, you can search for companies relevant to your expertise.</u></i></p><br>
        <p><i><u>**Step 3:** If you're a new user, complete all fields and confirm your domain to access the platform's features.</u></i></p>
        </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div style="color:yellow; margin:80px; text-align:center;">
          Developed with 🎮🕹️👾 by 
          <a href=https://github.com/Tushar-CYL>Tushar</a>
          <a href=https://github.com/Tushar-CYL>Aritra</a>
          <a href=https://github.com/Tushar-CYL>Anuj</a>
          <a href=https://github.com/Tushar-CYL>Sunil</a>
          <a href=https://github.com/Tushar-CYL>Rahul</a>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
