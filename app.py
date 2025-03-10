import streamlit as st

# Set up Streamlit app
st.set_page_config(
    page_title="AI Debugger",
    page_icon="🤖",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("🔍 AI Debugger Navigation")
page = st.sidebar.radio(
    "Go to",
    ("🏠 Home", "📊 Prediction", "🤖 Chatbot", "📢 Explainability & Bias")
)

# Hide default Streamlit navigation menu
hide_default_format = """
       <style>
       [data-testid="stSidebarNav"] {display: none;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# Load the selected page
if page == "🏠 Home":
    from pages import home
    home.show()
elif page == "📊 Prediction":
    from pages import prediction
    prediction.show()
elif page == "🤖 Chatbot":
    from pages import chatbot
    chatbot.show()
elif page == "📢 Explainability & Bias":
    from pages import explainability_bias
    explainability_bias.show()

# Footer
st.sidebar.markdown("---")
st.sidebar.write("© 2025 AI Debugger | Developed by Utsav Singhal")