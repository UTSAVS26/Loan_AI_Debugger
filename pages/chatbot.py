import streamlit as st
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("NEBIUS_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3.1-70B-Instruct-fast")  # Default to a model if not specified in .env

# Try to import OpenAI client, show clear error if not installed
try:
    from openai import OpenAI
    openai_available = True
except ImportError:
    openai_available = False

def get_chatbot_response(user_input, selected_model):
    """
    Get response from Nebius AI Studio API using the OpenAI client format.
    """
    # Check if API key is configured
    if not API_KEY:
        return ("⚠️ API configuration missing", 
                "Please configure NEBIUS_API_KEY in your .env file.")
    
    # Check if OpenAI package is installed
    if not openai_available:
        return ("⚠️ Missing dependency", 
                "The 'openai' package is not installed. Please install it with 'pip install openai'.")
    
    try:
        # Initialize OpenAI client with Nebius base URL
        client = OpenAI(
            base_url="https://api.studio.nebius.com/v1/",
            api_key=API_KEY
        )
        
        # Create the chat completion
        response = client.chat.completions.create(
            model=selected_model,  # Use the selected model from Streamlit UI
            max_tokens=512,
            temperature=0.6,
            top_p=0.9,
            extra_body={
                "top_k": 50
            },
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that explains predictions made by a loan approval model. Answer questions about model behavior, important features, and help users understand why certain applications are approved or rejected."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )
        
        # Extract and return the response content
        if response.choices and len(response.choices) > 0:
            return ("Success", response.choices[0].message.content)
        else:
            return ("⚠️ Empty response", "The API returned an empty response.")
        
    except Exception as e:
        # Handle different types of errors
        error_message = str(e)
        
        if "auth" in error_message.lower() or "api key" in error_message.lower():
            return ("⚠️ Authentication error", 
                    "The API key may be invalid. Please check your NEBIUS_API_KEY.")
        elif "not found" in error_message.lower() or "404" in error_message:
            return ("⚠️ API endpoint error", 
                    "The API endpoint could not be found. Please check the base URL.")
        elif "connection" in error_message.lower():
            return ("⚠️ Connection error", 
                    f"Could not connect to Nebius AI Studio: {error_message}")
        else:
            return ("⚠️ API error", f"An error occurred: {error_message}")

def show():
    """
    Display the chatbot UI in Streamlit.
    """
    # Streamlit UI
    st.title("🤖 AI Debugger Chatbot")
    st.write("Chat with AI to understand model insights and predictions!")

    # Add installation instructions if OpenAI is not available
    if not openai_available:
        st.warning("The OpenAI package is not installed. Please run: `pip install openai`")
    
    # Configuration settings
    with st.expander("Chatbot Configuration", expanded=False):
        st.write("Configure the API settings:")
        if not API_KEY:
            st.warning("API Key is not configured.")
        else:
            st.success("API Key is configured.")
        
        st.info("To update API settings, modify your .env file with: NEBIUS_API_KEY=your_api_key_here")
        
        # Allow model selection (User can select any model)
        model_options = [
            "meta-llama/Meta-Llama-3.1-70B-Instruct",
            "meta-llama/Meta-Llama-3.1-8B-Instruct",
            "deepseek-ai/DeepSeek-R1",
            "google/gemma-2-9b-it",
            "microsoft/phi-4",
            "Qwen/Qwen2-VL-7B-Instruct",
        ]
        selected_model = st.selectbox("Select Model", model_options, index=model_options.index(MODEL_NAME))
        
        # Display current model settings
        st.write("Current model settings:")
        st.code(f"""Model: {selected_model}
Max Tokens: 512
Temperature: 0.6
Top P: 0.9
Top K: 50""")

    # Chat interface
    user_input = st.text_input("💬 Ask something about the AI model...")

    # Create a local mode option
    local_mode = st.checkbox("Use local AI explanation (without API)", value=False)
    
    if user_input:
        if local_mode:
            # Local mode - don't use the API, provide basic responses
            chatbot_response = generate_local_response(user_input)
            st.write("### 🤖 Chatbot Response (Local Mode):")
            st.write(chatbot_response)
        else:
            # API mode - use the external AI service
            status, chatbot_response = get_chatbot_response(user_input, selected_model)
            
            if status == "Success":
                st.write("### 🤖 Chatbot Response:")
                st.write(chatbot_response)
            else:
                st.error(f"### {status}")
                st.write(chatbot_response)
                
                # Suggest using local mode if API fails
                st.info("Consider using 'Local AI explanation' mode if you're having issues with the API connection.")

def generate_local_response(query):
    """
    Generate a simple local response without using the API.
    This is a fallback for when the API is not available.
    """
    query = query.lower()
    
    # Very basic pattern matching for common questions
    if any(word in query for word in ["model", "algorithm", "classifier"]):
        return """The AI Debugger uses a Random Forest Classifier to predict loan approval. 
                This is an ensemble learning method that operates by constructing multiple decision 
                trees during training and outputs the class that is the mode of the classes of the individual trees."""
    
    elif any(word in query for word in ["important", "feature", "factor"]):
        return """The most important features for loan approval prediction are:
                1. Credit History - Having a good credit history significantly increases approval chances
                2. Applicant Income - Higher income correlates with higher approval rates
                3. Loan Amount - Smaller loan amounts are more likely to be approved
                4. Property Area - Urban and semi-urban properties have higher approval rates"""
    
    elif any(word in query for word in ["accuracy", "performance", "accurate"]):
        return """The Random Forest model achieves approximately 85% accuracy on the test data. 
                It has good recall for approved loans (90%) and slightly lower recall for rejected loans (75%), 
                suggesting it's somewhat optimistic in its predictions."""
    
    elif any(word in query for word in ["improve", "better", "enhance"]):
        return """To improve prediction accuracy, you could:
                1. Collect more training data, especially for rejected loans
                2. Add more features like debt-to-income ratio
                3. Try advanced models like XGBoost or neural networks
                4. Implement feature engineering to create more informative features"""
    
    elif any(word in query for word in ["rejected", "denied", "not approved"]):
        return """Loans are typically rejected for these main reasons:
                1. Poor credit history
                2. Low income relative to loan amount
                3. High existing debt
                4. Insufficient loan term for the requested amount
                5. Property location in areas with higher default rates"""
                
    elif any(word in query for word in ["approved", "accepted", "get approved"]):
        return """To increase chances of loan approval:
                1. Maintain good credit history
                2. Apply for a loan amount appropriate to your income
                3. Have a co-applicant with good income
                4. Choose a longer loan term if possible
                5. Provide all documentation completely and accurately"""
    
    else:
        return """I'm currently in local mode and can answer basic questions about the loan prediction model.
                I can tell you about how the model works, important features, model performance, 
                and ways to improve predictions. What specific aspect would you like to know about?"""