🧠 AI Resume Screening Web App
This project is a web-based AI-driven resume screening system that helps recruiters or hiring teams automatically assess resume suitability based on job categories and suggests improvements or interview questions using Google Gemini.


📂 Project Structure

AI_Resume_Screening/
│
├── webapp/
│   ├── app.py
│   ├── models.py
│   ├── templates/
│   │   ├── index.html
│   │   └── result.html
│   ├── static/
│   └── .env.example
│
├── model/
│   ├── resume_parser.py
│   ├── train_dummy_model.py
│   └── trained_model.pkl
│
├── .gitignore
├── README.md


🚀 Features
Upload and parse resume files (PDF/DOCX)

Predict the job category suitability using an ML model

If suitable, provide interview questions using Google Gemini

If not suitable, suggest resume improvements

Tracks resume screening history using SQLite

Dashboard to monitor predictions and accuracy


🛠️ Tech Stack
Python

Flask

SQLite (via SQLAlchemy)

scikit-learn (ML model)

Google Gemini API (via google.generativeai)

dotenv for managing API keys securely


📈 Dashboard
Access /dashboard to view past predictions and accuracy of the model.

⚠️ Important Notes
Do not push .env to GitHub (already ignored via .gitignore)

You can improve the ML model with a better training dataset

Make sure you have a stable internet connection to call Gemini APIs

















