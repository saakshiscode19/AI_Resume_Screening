from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import db, ResumeHistory
import google.generativeai as genai
import os
import pickle
import sys
from dotenv import load_dotenv

# Fix ImportError: Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import resume parser
from model.resume_parser import extract_text_from_resume

app = Flask(__name__)

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume_history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

if not GEMINI_API_KEY:
    raise ValueError("❌ Gemini API key not found! Set 'GEMINI_API_KEY' in a .env file.")

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Load trained resume screening model
model_path = os.path.join(os.path.dirname(__file__), '../model/trained_model.pkl')
try:
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
except FileNotFoundError:
    raise ValueError("❌ Trained model not found! Make sure 'trained_model.pkl' exists in the 'model' folder.")

# Initialize Gemini model
gemini_model = genai.GenerativeModel("gemini-1.5-pro")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        selected_category = request.form["category"]
        uploaded_file = request.files["resume"]

        if not uploaded_file or uploaded_file.filename == "":
            return render_template("index.html", error="❌ Please upload a resume file.")

        try:
            resume_text = extract_text_from_resume(uploaded_file)
            prediction = model.predict([resume_text])[0]
            fit = prediction == selected_category

            # Save to DB
            history = ResumeHistory(
                filename=uploaded_file.filename,
                predicted_category=prediction,
                selected_category=selected_category,
                fit=fit
            )
            db.session.add(history)
            db.session.commit()

            if fit:
                prompt = f"Provide 5 interview questions for a {selected_category} role."
                response = gemini_model.generate_content(prompt)
                questions = response.text.strip() if response else "No questions generated."
                return render_template("result.html", fit=True, category=selected_category, questions=questions)

            else:
                prompt = f"Suggest improvements for a resume applying to a {selected_category} role."
                response = gemini_model.generate_content(prompt)
                suggestions = response.text.strip() if response else "No suggestions generated."
                return render_template("result.html", fit=False, category=selected_category, suggestions=suggestions)

        except Exception as e:
            return render_template("result.html", error=f"❌ Error: {str(e)}")

    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    history = ResumeHistory.query.order_by(ResumeHistory.timestamp.desc()).all()
    total = len(history)
    correct = sum(1 for h in history if h.predicted_category == h.selected_category)
    accuracy = (correct / total * 100) if total > 0 else 0
    return render_template("dashboard.html", history=history, accuracy=round(accuracy, 2))


if __name__ == "__main__":
    app.run(debug=True)
