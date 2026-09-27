import joblib
import pandas as pd

# Load model
model = joblib.load("../models/world_cup_result_model.pkl")

# Load feature list
feature_columns = joblib.load("../models/feature_columns.pkl")

print("Model loaded successfully!")
print("Classes:", model.classes_)
print("Number of features:", len(feature_columns))

# Test using the first test-row from our feature dataset
df = pd.read_csv("../data/team_features.csv")

sample = df.iloc[-1]

X = pd.DataFrame([{
    column: sample[column]
    for column in feature_columns
}])

# Prediction probabilities
probabilities = model.predict_proba(X)[0]

print("\n==============================")
print("MATCH PREDICTION TEST")
print("==============================")

for team_result, probability in zip(model.classes_, probabilities):
    print(f"{team_result}: {probability * 100:.2f}%")

prediction = model.predict(X)[0]

print("\nPredicted result:", prediction)

print("\nTest match:")
print(f"{sample['home_team']} vs {sample['away_team']}")