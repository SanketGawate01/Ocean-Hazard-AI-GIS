import joblib
import os
import re

# Get the absolute path to the model file so it doesn't crash when running uvicorn
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ocean_hazard_lr_model.pkl")

# Load the model into memory once when the module is imported
try:
    ml_pipeline = joblib.load(MODEL_PATH)
    print("✅ ML Model loaded successfully into backend.")
except Exception as e:
    ml_pipeline = None
    print(f"❌ Error loading ML model: {e}")

def clean_text(text: str) -> str:
    """Exact cleaning function ported from the Jupyter Notebook."""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"&\w+;|<.*?>", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"\brt\b", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def calculate_severity(category: str, confidence: float) -> str:
    """
    Rule-based severity assessment (Phase 1 Project Spec Requirement).
    """
    if category == "Storm / Cyclone":
        return "CRITICAL" if confidence > 0.85 else "HIGH"
    elif category == "Oil Spill" or category == "Marine Pollution":
        return "HIGH" if confidence > 0.75 else "MEDIUM"
    elif category == "Coastal Flooding":
        return "HIGH" if confidence > 0.80 else "MEDIUM"
    elif category == "High Waves / Rough Sea":
        return "MEDIUM" if confidence > 0.70 else "LOW"
    return "LOW"

def get_hazard_prediction(description: str):
    """
    Main function to be called by the FastAPI router.
    """
    # Fallback just in case the model failed to load
    if ml_pipeline is None:
        return {"predicted_category": "Marine Pollution", "confidence": 0.5, "severity": "LOW"}
    
    # 1. Clean the incoming text
    cleaned_text = clean_text(description)
    
    # 2. Predict the class
   # 1. Clean the incoming text
    cleaned_text = clean_text(description)
    
    # 2. Predict the class
    predicted_class = ml_pipeline.predict([cleaned_text])[0]
    
    # ---> ADD THESE TWO LINES TO FIX THE NAMING MISMATCH <---
    if predicted_class == "Flooding":
        predicted_class = "Coastal Flooding"
    # --------------------------------------------------------
    
    # 3. Get the probability for the predicted class
    probabilities = ml_pipeline.predict_proba([cleaned_text])[0]
    confidence_score = round(float(max(probabilities)), 4)
    
    # 4. Calculate severity
    severity = calculate_severity(predicted_class, confidence_score)
    
    return {
        "predicted_category": predicted_class,
        "confidence": confidence_score,
        "severity": severity
    }
