from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# ======================
# DATABASE MODELS
# ======================

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    class_level = db.Column(db.String(50))
    interest = db.Column(db.String(100))
    location = db.Column(db.String(100))

class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    field = db.Column(db.String(100))
    experience = db.Column(db.Integer)
    location = db.Column(db.String(100))
    bio = db.Column(db.Text)

# ======================
# CAREER ENGINE
# ======================

def recommend_career(interest):
    mapping = {
        "Math": "Data Scientist / AI Engineer",
        "Biology": "Biotechnology / Medical Research",
        "Computers": "Software Developer / Cyber Security Expert",
        "Physics": "Space Scientist / Research Scientist"
    }
    return mapping.get(interest, "Explore STEM Careers")

def match_mentor(interest):
    return Mentor.query.filter_by(field=interest).first()

# ======================
# ROUTES
# ======================

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        class_level = request.form["class_level"]
        interest = request.form["interest"]
        location = request.form["location"]

        student = Student(
            name=name,
            email=email,
            class_level=class_level,
            interest=interest,
            location=location
        )

        db.session.add(student)
        db.session.commit()

        career = recommend_career(interest)
        mentor = match_mentor(interest)

        return render_template("dashboard.html",
                               student=student,
                               career=career,
                               mentor=mentor)

    return render_template("index.html")

@app.route("/mentors")
def mentors():
    all_mentors = Mentor.query.all()
    return render_template("mentors.html", mentors=all_mentors)

@app.route("/rolemodels")
def rolemodels():
    return render_template("rolemodels.html")

@app.route("/awareness")
def awareness():
    return render_template("awareness.html")

# ======================
# RUN
# ======================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Insert default mentors (only once)
        if Mentor.query.count() == 0:
            m1 = Mentor(name="Dr. Anjali Sharma", field="Math", experience=10,
                        location="Bangalore",
                        bio="AI Researcher working in Data Science.")
            m2 = Mentor(name="Dr. Priya Rao", field="Biology", experience=8,
                        location="Chennai",
                        bio="Biotechnology Scientist and Researcher.")
            m3 = Mentor(name="Meera Iyer", field="Computers", experience=6,
                        location="Hyderabad",
                        bio="Software Engineer in Cyber Security.")
            db.session.add_all([m1, m2, m3])
            db.session.commit()

    app.run(debug=True)