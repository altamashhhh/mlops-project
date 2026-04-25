# check_model.py
import pickle
import numpy as np

vectorizer = pickle.load(open('models/vectorizer.pkl', 'rb'))
model = pickle.load(open('models/model.pkl', 'rb'))

print(f"Vectorizer features: {len(vectorizer.get_feature_names_out())}")
print(f"Model classes: {model.classes_}")
print(f"Model params: {model.get_params()}")

# Simple test
test_reviews = [
    "this movie was absolutely amazing and wonderful",
    "terrible movie, worst film ever, completely bad",
    "great acting, loved every moment of it"
]

for review in test_reviews:
    vec = vectorizer.transform([review])
    pred = model.predict(vec)
    proba = model.predict_proba(vec)
    print(f"\nReview: {review}")
    print(f"Prediction: {pred[0]} | Probability: {proba}")