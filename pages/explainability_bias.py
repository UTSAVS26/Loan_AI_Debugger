import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.inspection import permutation_importance
from utils.model_utils import load_model_and_encoders

# Load model and encoders
model, label_encoders = load_model_and_encoders()

def show():
    """
    Display the Explainability & Bias Analysis UI in Streamlit.
    """
    st.title("📢 Model Explainability & Bias Analysis")
    st.write("Understand how the AI model makes decisions and check for potential biases.")

    # 🔍 Feature Importance (Fast Alternative)
    st.subheader("📊 Feature Importance")

    try:
        # Ensure model has feature names
        if not hasattr(model, "feature_names_in_"):
            st.error("Model does not have 'feature_names_in_' attribute.")
            return

        feature_names = model.feature_names_in_

        # Use built-in feature importance if available (for tree-based models)
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
        else:
            # Use permutation importance (works for all models)
            sample_input = np.random.rand(100, len(feature_names))  # Generate 100 random inputs
            sample_output = model.predict(sample_input)
            result = permutation_importance(model, sample_input, sample_output, n_repeats=10, random_state=42)
            importances = result.importances_mean

        # Create DataFrame for visualization
        importance_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
        importance_df = importance_df.sort_values(by="Importance", ascending=False)

        # Plot the feature importance
        fig, ax = plt.subplots()
        ax.barh(importance_df["Feature"], importance_df["Importance"], color="skyblue")
        ax.set_xlabel("Importance Score")
        ax.set_title("Feature Importance")
        plt.gca().invert_yaxis()  # Flip order for better visualization
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Could not calculate feature importance: {e}")

    # ⚖️ Bias Detection Section
    st.subheader("⚖️ Bias Detection")
    st.write("Check if the model has biases in gender, income, or location-based predictions.")

    if st.button("🔎 Analyze Bias"):
        try:
            bias_results = detect_bias(model, label_encoders)
            st.write(bias_results)
        except Exception as e:
            st.error(f"Error detecting bias: {e}")

def detect_bias(model, label_encoders):
    """
    Dummy function to simulate bias detection.
    """
    bias_report = {
        "Gender Bias": "No strong gender bias detected.",
        "Income Bias": "Slight preference for higher incomes in approval.",
        "Location Bias": "Urban applicants have a higher chance of approval."
    }
    return bias_report