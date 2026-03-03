import random
import pandas as pd

# -------------------------------
# 1. Define clusters and symptoms
# -------------------------------

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

# Severity weights by cluster (for risk calculation)
cluster_weights = {
    "Cardiovascular": 3,
    "Respiratory": 3,
    "Neurological": 2,
    "Gastrointestinal": 2,
    "Musculoskeletal": 1,
    "Dermatological": 1,
    "Systemic": 2,
    "ENT": 1,
    "Endocrine/Metabolic": 2
}

# Duration categories (Option B)
durations = ["<24h", "1-3 days", "4-7 days", "1-2 weeks", "2-4 weeks", ">1 month"]
duration_weights = {
    "<24h": 1,
    "1-3 days": 2,
    "4-7 days": 3,
    "1-2 weeks": 4,
    "2-4 weeks": 5,
    ">1 month": 6
}

# Improvement options
improvements = ["improved", "no_change", "worsened"]

# Medication taken
medication_options = ["yes", "no"]

# -------------------------------
# 2. Generate dataset
# -------------------------------
num_samples = 5000
data = []

for _ in range(num_samples):
    age = random.randint(10, 80)
    gender = random.choice(["M", "F"])
    
    # pick 1 cluster randomly
    cluster = random.choice(list(clusters.keys()))
    
    # pick 1-6 symptoms from that cluster
    symptom_count = random.randint(1, min(6, len(clusters[cluster])))
    symptoms = random.sample(clusters[cluster], symptom_count)
    
    # duration
    duration = random.choice(durations)
    
    # medication and improvement
    medication_taken = random.choice(medication_options)
    improvement = random.choice(improvements)
    
    # Calculate risk score
    score = cluster_weights[cluster] + duration_weights[duration]
    if medication_taken == "yes" and improvement == "no_change":
        score += 2
    elif medication_taken == "yes" and improvement == "worsened":
        score += 3
    elif medication_taken == "no" and improvement == "worsened":
        score += 4
    
    # Assign risk level
    if score <= 6:
        risk_level = "Low"
    elif score <= 9:
        risk_level = "Moderate"
    else:
        risk_level = "High"
    
    # Append row
    data.append({
        "age": age,
        "gender": gender,
        "cluster": cluster,
        "symptom_count": symptom_count,
        "symptoms": ",".join(symptoms),
        "duration": duration,
        "medication_taken": medication_taken,
        "improvement": improvement,
        "risk_level": risk_level
    })

# -------------------------------
# 3. Save to CSV
# -------------------------------
df = pd.DataFrame(data)
df.to_csv("symptom_dataset.csv", index=False)
print("Dataset generated successfully: symptom_dataset.csv")
