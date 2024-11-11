# TalentTrack Project

## Overview
TalentTrack is a data-driven job and career assistance platform built with **Python** and **Streamlit**. It enables users to access job listings, check resume scores, and predict career paths based on their skills and experience. The project leverages machine learning and web scraping, providing valuable insights and recommendations for job seekers and employers.

## Features
- **Resume Screening**: Analyzes resumes to assign a score, helping users improve their profiles.
- **Job Search**: Allows users to find relevant jobs based on location and skills.
- **Career Path Prediction**: Uses machine learning to suggest potential career trajectories based on user profiles.
- **User Management**: New and returning users can log in, store data, and access personalized features.

## File Structure

```plaintext
TalentTrack/
│
├── assets/                       # Static assets (e.g., images, CSS files)
├── data/                         # Data files for ML models and additional datasets
├── pages/                        # Streamlit page scripts for navigation
│   ├── About.py                  # About page
│   ├── Find-Jobs.py              # Job search functionality
│   ├── Login.py                  # User login
│   ├── New-User.py               # New user registration
│   ├── Prediction.py             # Career path prediction page
│   ├── Resume-score-Checker.py   # Resume scoring feature
│   ├── __init__.py               # Initializes pages as a package
│   ├── chennai.csv               # Job listings in Chennai
│   ├── datasci-45410-6655c180fd9 # Dataset for data science job listings
│   ├── kol.csv                   # Job listings in Kolkata
│   ├── mumbai.csv                # Job listings in Mumbai
│
├── Home.py                       # Main home page of the application
├── LICENSE                       # License file
├── Resume Screening.ipynb        # Notebook for resume screening model
├── UpdatedResumeDataSet.csv      # Dataset for training the resume screening model
├── careerPredictionModel.ipynb   # Notebook for career path prediction model
├── clf.pkl                       # Pickle file for the classification model
├── packages.txt                  # Package dependencies
├── requirements.txt              # Required Python libraries
├── tfidf.pkl                     # Pickle file for TF-IDF vectorizer
└── weights.pkl                   # Model weights file
```

git clone https://github.com/yourusername/TalentTrack.git
cd TalentTrack

python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

Resources
Krish Naik - YouTube: Great tutorials on machine learning and deep learning concepts.
Streamlit Documentation: Official Streamlit documentation for building web applications.
LinkedIn: Connect with industry professionals for guidance and insights.

Usage
Login/Register: Use the app to create an account or log in as an existing user.
Resume Screening: Upload a resume to receive feedback and a score to improve it.
Job Search: Filter jobs based on location and skills.

Career Prediction: Get suggestions for career advancement based on your skills and experience.

License
This project is licensed under the MIT License - see the LICENSE file for details.
