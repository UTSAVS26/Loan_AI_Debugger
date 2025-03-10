import streamlit as st
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3.1-70B-Instruct-fast")  # Default model

# Try to import OpenAI client, show clear error if not installed
try:
    from openai import OpenAI
    openai_available = True
except ImportError:
    openai_available = False

def get_chatbot_response(user_input, selected_model, api_key):
    """
    Get response from Nebius AI Studio API using the OpenAI client format.
    """
    # Check if API key is provided
    if not api_key:
        return ("⚠️ API configuration missing", "Please enter your Nebius API Key.")
    
    if not openai_available:
        return ("⚠️ Missing dependency", "The 'openai' package is not installed. Please install it with 'pip install openai'.")
    
    try:
        # Initialize OpenAI client with Nebius base URL
        client = OpenAI(
            base_url="https://api.studio.nebius.com/v1/",
            api_key=api_key
        )
        
        # Create the chat completion
        response = client.chat.completions.create(
            model=selected_model,
            max_tokens=512,
            temperature=0.6,
            top_p=0.9,
            extra_body={"top_k": 50},
            messages=[
                {"role": "system", "content": "You are an AI assistant that explains predictions made by a loan approval model."},
                {"role": "user", "content": user_input}
            ]
        )
        
        if response.choices and len(response.choices) > 0:
            return ("Success", response.choices[0].message.content)
        else:
            return ("⚠️ Empty response", "The API returned an empty response.")
    
    except Exception as e:
        error_message = str(e)
        if "auth" in error_message.lower() or "api key" in error_message.lower():
            return ("⚠️ Authentication error", "Invalid API key. Please check and re-enter.")
        elif "not found" in error_message.lower() or "404" in error_message:
            return ("⚠️ API endpoint error", "Invalid API endpoint. Check the base URL.")
        elif "connection" in error_message.lower():
            return ("⚠️ Connection error", f"Could not connect to Nebius AI Studio: {error_message}")
        else:
            return ("⚠️ API error", f"An error occurred: {error_message}")

def show():
    """
    Display the chatbot UI in Streamlit.
    """
    st.title("🤖 AI Debugger Chatbot")
    st.write("Chat with AI to understand model insights and predictions!")
    
    if not openai_available:
        st.warning("The OpenAI package is not installed. Please run: `pip install openai`")
    
    # API Key Input
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    api_key = st.text_input("Enter your Nebius API Key:", type="password", value=st.session_state.api_key)
    if api_key:
        st.session_state.api_key = api_key
    
    with st.expander("Chatbot Configuration", expanded=False):
        st.write("Configure the API settings:")
        
        if not st.session_state.api_key:
            st.warning("API Key is not configured. Please enter your API key above.")
        else:
            st.success("API Key is configured.")
        
        model_options = [
            "meta-llama/Meta-Llama-3.1-70B-Instruct",
            "meta-llama/Meta-Llama-3.1-8B-Instruct",
            "deepseek-ai/DeepSeek-R1",
            "google/gemma-2-9b-it",
            "microsoft/phi-4",
            "Qwen/Qwen2-VL-7B-Instruct",
        ]
        selected_model = st.selectbox("Select Model", model_options, index=model_options.index(MODEL_NAME))
        
        st.write("Current model settings:")
        st.code(f"""Model: {selected_model}
Max Tokens: 512
Temperature: 0.6
Top P: 0.9
Top K: 50""")
    
    user_input = st.text_input("💬 Ask something about the AI model...")
    local_mode = st.checkbox("Use local AI explanation (without API)", value=False)
    
    if user_input:
        if local_mode:
            chatbot_response = generate_local_response(user_input)
            st.write("### 🤖 Chatbot Response (Local Mode):")
            st.write(chatbot_response)
        else:
            status, chatbot_response = get_chatbot_response(user_input, selected_model, st.session_state.api_key)
            if status == "Success":
                st.write("### 🤖 Chatbot Response:")
                st.write(chatbot_response)
            else:
                st.error(f"### {status}")
                st.write(chatbot_response)
                st.info("Consider using 'Local AI explanation' mode if you're having API issues.")