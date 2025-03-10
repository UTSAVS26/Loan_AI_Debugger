import pickle
import pandas as pd
import numpy as np

# Paths to stored model and encoders
MODEL_PATH = "assets/data/trained_model.pkl"
ENCODER_PATH = "assets/data/label_encoders.pkl"

def load_model_and_encoders():
    """
    Load the trained model and label encoders.
    """
    model, label_encoders = None, {}

    # Load the trained model
    try:
        with open(MODEL_PATH, "rb") as model_file:
            model = pickle.load(model_file)
    except FileNotFoundError:
        print(f"⚠️ Warning: Model file not found at {MODEL_PATH}")

    # Load label encoders
    try:
        with open(ENCODER_PATH, "rb") as encoder_file:
            label_encoders = pickle.load(encoder_file)
    except FileNotFoundError:
        print(f"⚠️ Warning: Encoder file not found at {ENCODER_PATH}")

    return model, label_encoders

# Load model and encoders at runtime
model, label_encoders = load_model_and_encoders()

def preprocess_input(input_data, label_encoders):
    """
    Preprocess user input to match model expectations.
    Converts categorical values using label encoders and ensures numerical values are in proper format.
    """
    try:
        # Convert input dictionary to DataFrame
        df = pd.DataFrame([input_data])
        
        # Ensure column names are lowercase for consistency
        df.columns = [col.lower() for col in df.columns]
        
        # Process categorical columns
        categorical_cols = ["gender", "married", "dependents", "education", "self_employed", "property_area"]
        for col in categorical_cols:
            if col in df.columns:
                # Convert the value to string in case it's not already
                df[col] = df[col].astype(str)
                
                # Check if the column has a corresponding encoder
                if col in label_encoders:
                    # Create a safe transformation function that handles unknown values
                    def safe_transform(value, encoder, default=0):
                        if value in encoder.classes_:
                            return encoder.transform([value])[0]
                        else:
                            print(f"⚠️ Unknown value '{value}' for '{col}', using default.")
                            return default
                    
                    # Apply the transformation to each value individually
                    df[col] = df[col].apply(lambda x: safe_transform(x, label_encoders[col]))
        
        # Convert numeric columns
        numeric_cols = ["applicant_income", "coapplicant_income", "loan_amount", "loan_amount_term", "credit_history"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        # Fill missing values
        df.fillna(0, inplace=True)
        
        # Ensure we have the right format for the model
        # If model has feature_names_in_ attribute (sklearn 1.0+), use it to align columns
        if hasattr(model, 'feature_names_in_'):
            expected_cols = [col.lower() for col in model.feature_names_in_]
            
            # Add missing columns with zeros
            for col in expected_cols:
                if col not in df.columns:
                    df[col] = 0
            
            # Reorder columns to match the model's expectations
            df = df[expected_cols]
        
        # Convert to numpy array for prediction
        return df.values
        
    except Exception as e:
        print(f"❌ Error in preprocessing: {str(e)}")
        raise  # Re-raise to see detailed error in the UI

def predict_loan_status(input_data):
    """
    Predict loan status based on user input.
    """
    if model is None:
        return "⚠️ Model not loaded. Check if the model file exists."

    try:
        processed_data = preprocess_input(input_data, label_encoders)
        if processed_data is None:
            return "⚠️ Invalid input data."

        prediction = model.predict(processed_data)
        return "✅ Approved" if prediction[0] == 1 else "❌ Rejected"

    except Exception as e:
        return f"❌ Error in prediction: {str(e)}"