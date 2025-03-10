import streamlit as st
import pandas as pd
import numpy as np
import traceback
from utils.model_utils import preprocess_input, load_model_and_encoders

# Load the trained model and encoders
model, label_encoders = load_model_and_encoders()

def show():
    """
    Display the Prediction UI in Streamlit.
    """
    st.title("🔮 AI Model Prediction")
    st.write("Enter details below to get a loan prediction.")

    # Debug mode (Commented out for live deployment)
    # debug_mode = st.sidebar.checkbox("Enable Debug Mode", value=False)
    
    # if debug_mode and model is not None and hasattr(model, 'feature_names_in_'):
    #     st.sidebar.subheader("Model Information")
    #     st.sidebar.write(f"Model Type: {type(model).__name__}")
    #     st.sidebar.write(f"Expected Features: {', '.join(model.feature_names_in_)}")
        
    #     st.sidebar.subheader("Label Encoders")
    #     for col, encoder in label_encoders.items():
    #         st.sidebar.write(f"{col}: {', '.join(encoder.classes_)}")

    # Create input fields in a grid layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        married = st.selectbox("Married", ["Yes", "No"])
    
    with col2:
        dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
        education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    
    with col3:
        self_employed = st.selectbox("Self Employed", ["Yes", "No"])
        applicant_income = st.number_input("Applicant Income", min_value=0, step=500)

    col4, col5 = st.columns(2)
    
    with col4:
        coapplicant_income = st.number_input("Coapplicant Income", min_value=0, step=500)
    
    with col5:
        loan_amount = st.number_input("Loan Amount", min_value=0, step=500)

    loan_term = st.selectbox("Loan Term (Months)", ["12", "24", "36", "48", "60", "120", "180", "240", "360"])
    credit_history = st.selectbox("Credit History", ["0", "1"])
    property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

    # Predict button
    if st.button("🔍 Predict Loan Approval"):
        user_data = {
            "gender": gender,
            "married": married,
            "dependents": dependents,
            "education": education,
            "self_employed": self_employed,
            "applicant_income": applicant_income,
            "coapplicant_income": coapplicant_income,
            "loan_amount": loan_amount,
            "loan_amount_term": loan_term,
            "credit_history": credit_history,
            "property_area": property_area,
        }

        try:
            # Debug mode - show input data (Commented out for live)
            # if debug_mode:
            #     st.subheader("Debug: Input Data")
            #     st.write(user_data)
            
            # Preprocess input
            processed_input = preprocess_input(user_data, label_encoders)
            
            # Debug mode - show processed data (Commented out for live)
            # if debug_mode:
            #     st.subheader("Debug: Processed Input")
            #     st.write(f"Shape: {processed_input.shape}")
            #     st.write(processed_input)
            
            # Predict using model
            prediction = model.predict(processed_input)

            # Display the result
            st.subheader("📌 Prediction Result")
            if prediction[0] == 1:
                st.success("✅ Loan Approved!")
            else:
                st.error("❌ Loan Rejected!")
                
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")
            # Debug mode - show error traceback (Commented out for live)
            # if debug_mode:
            #     st.error("Detailed error traceback:")
            #     st.code(traceback.format_exc())