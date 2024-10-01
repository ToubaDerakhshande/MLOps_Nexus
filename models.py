#(Abdi)
import joblib
import pandas as pd


selected_features = [
    'mean radius', 'mean perimeter', 'mean area', 'mean concavity', 'mean concave points',
    'worst radius', 'worst perimeter', 'worst area', 'worst concavity', 'worst concave points'
]


def load_model():
    with open('model.pkl', 'rb') as f:
        model = joblib.load(f)
    return model

model = load_model()


def predict(features):
    
    input_df = pd.DataFrame([features])[selected_features]

    
    prediction = model.predict(input_df)
    
    return prediction[0]
