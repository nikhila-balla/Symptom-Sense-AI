import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle

# -----------------------------
# 1. Load Dataset
# -----------------------------
df = pd.read_csv("symptom_dataset.csv")

# -----------------------------
# 2. Encode categorical features
# -----------------------------
le_gender = LabelEncoder()
le_cluster = LabelEncoder()
le_duration = LabelEncoder()
le_improvement = LabelEncoder()
le_med = LabelEncoder()
le_risk = LabelEncoder()

df['gender_enc'] = le_gender.fit_transform(df['gender'])
df['cluster_enc'] = le_cluster.fit_transform(df['cluster'])
df['duration_enc'] = le_duration.fit_transform(df['duration'])
df['improvement_enc'] = le_improvement.fit_transform(df['improvement'])
df['medication_enc'] = le_med.fit_transform(df['medication_taken'])
df['risk_enc'] = le_risk.fit_transform(df['risk_level'])

# -----------------------------
# 3. Select features and target
# -----------------------------
X = df[['age','gender_enc','cluster_enc','symptom_count','duration_enc','medication_enc','improvement_enc']]
y = df['risk_enc']

# -----------------------------
# 4. Split data
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -----------------------------
# 5. Train RandomForest
# -----------------------------
clf = RandomForestClassifier(n_estimators=200, random_state=42)
clf.fit(X_train, y_train)

# -----------------------------
# 6. Evaluate
# -----------------------------
acc = clf.score(X_test, y_test)
print(f"Model Accuracy: {acc:.3f}")

# -----------------------------
# 7. Save model and encoders
# -----------------------------
with open("model.pkl", "wb") as f:
    pickle.dump({
        "model": clf,
        "le_gender": le_gender,
        "le_cluster": le_cluster,
        "le_duration": le_duration,
        "le_improvement": le_improvement,
        "le_med": le_med,
        "le_risk": le_risk
    }, f)

print("Model and encoders saved as model.pkl")
