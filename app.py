from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load trained model
with open("model.pkl", "rb") as f:
    saved = pickle.load(f)

model = saved["model"]
le_gender = saved["le_gender"]
le_cluster = saved["le_cluster"]
le_duration = saved["le_duration"]
le_improvement = saved["le_improvement"]
le_med = saved["le_med"]
le_risk = saved["le_risk"]

clusters = {
    "Cardiovascular": ["chest pain", "palpitations", "shortness of breath", "swelling legs", "fainting", "tightness chest"],
    "Respiratory": ["cough", "wheezing", "throat pain", "runny nose", "sinus pressure", "breathlessness", "sputum"],
    "Neurological": ["dizziness", "headache", "numbness", "tingling", "memory issues", "tremors", "imbalance", "confusion"],
    "Gastrointestinal": ["vomiting", "diarrhea", "constipation", "stomach pain", "bloating", "acid reflux", "nausea"],
    "Musculoskeletal": ["knee pain", "hand ache", "back pain", "shoulder pain", "joint stiffness", "muscle cramps", "swelling joints"],
    "Dermatological": ["rash", "itching", "hair fall", "acne", "dry skin", "eczema", "skin redness"],
    "Systemic": ["fever", "chills", "fatigue", "weakness", "body pain", "night sweats"],
    "ENT": ["ear pain", "hearing loss", "ringing ears", "blocked nose", "sore throat", "hoarseness"],
    "Endocrine/Metabolic": ["excess thirst", "weight loss", "weight gain", "sweating", "cold intolerance"]
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        age = request.form.get("age")
        gender = request.form.get("gender")
        return render_template("symptoms.html", age=age, gender=gender)
    return render_template("user_info.html")


# 🔥 THIS ROUTE WAS MISSING — NOW FIXED
@app.route("/symptoms", methods=["POST"])
def symptoms():
    age = request.form.get("age")
    gender = request.form.get("gender")
    return render_template("symptoms.html", age=age, gender=gender)


@app.route("/medication", methods=["POST"])
def medication():
    age = request.form.get("age")
    gender = request.form.get("gender")
    symptoms = request.form.getlist("symptoms")

    return render_template("medication.html",
                           age=age,
                           gender=gender,
                           symptoms=",".join(symptoms))


@app.route("/result", methods=["POST"])
def result():
    age = int(request.form.get("age"))
    gender = request.form.get("gender")
    symptoms = request.form.get("symptoms").split(",")
    duration = request.form.get("duration")
    medication_taken = request.form.get("medication_taken")
    improvement = request.form.get("improvement") if medication_taken == "yes" else "no_change"

    # Detect cluster
    cluster = "Systemic"
    for c, s_list in clusters.items():
        for user_sym in symptoms:
            for db_sym in s_list:
                if user_sym.replace("_", " ") in db_sym:
                    cluster = c
                    break

    # Normalize gender
    gender = "F" if gender == "female" else "M"

    duration_map = {
        "<24h": "<24h",
        "1-3d": "1-3 days",
        "4-7d": "4-7 days",
        "1-2w": "1-2 weeks",
        ">2w": ">1 month"
    }

    duration_fixed = duration_map[duration]

    X = [[
        age,
        le_gender.transform([gender])[0],
        le_cluster.transform([cluster])[0],
        len(symptoms),
        le_duration.transform([duration_fixed])[0],
        le_med.transform([medication_taken])[0],
        le_improvement.transform([improvement])[0]
    ]]

    risk = le_risk.inverse_transform(model.predict(X))[0]

    return render_template("result.html",
                           age=age,
                           gender=gender,
                           symptoms=symptoms,
                           cluster=cluster,
                           duration=duration_fixed,
                           medication_taken=medication_taken,
                           improvement=improvement,
                           risk=risk)


if __name__ == "__main__":
    app.run(debug=True)
