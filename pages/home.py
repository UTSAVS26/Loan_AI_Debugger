import streamlit as st

def show():
    """
    Display the Home UI for Loan AI Debugger.
    """

    # 📌 Title & Logo Placement
    col1, col2 = st.columns([0.8, 0.2])  # 80% title, 20% logo

    with col1:
        st.title("🏦 Loan AI Debugger: Smart Loan Approval Analysis")

    with col2:
        st.image("assets/logo.png", width=100)  # Adjust width to make logo small

    # 🎯 Introduction
    st.markdown("""
        **Welcome to Loan AI Debugger!**  
        This tool helps analyze and debug loan approval decisions made by machine learning models.  
        Whether you're a **banking professional, data scientist, or loan officer**, this tool ensures **fair, explainable, and accurate** loan approvals. 🚀  
    """)

    # 🔍 **What is Loan AI Debugger?**
    st.subheader("🔍 What is Loan AI Debugger?")
    st.markdown("""
    This AI-powered tool enables you to:
    
    - **📊 Predict Loan Approvals** using machine learning.  
    - **📢 Understand AI decisions** with explainability tools.  
    - **⚖️ Detect Bias** in loan approvals across demographics.  
    - **🛠️ Debug Loan Approval Models** for better accuracy.  
    """)

    # 🎯 **Why Use Loan AI Debugger?**
    st.subheader("🎯 Why Use This Tool?")
    st.markdown("""
    - **🚀 Fast & Reliable**: Instant loan approval predictions.  
    - **📈 Optimize Model Performance**: Identify patterns in approvals/rejections.  
    - **⚖️ Ensure Fair Lending**: Reduce bias in loan approvals.  
    - **🔍 Transparent AI Decisions**: Explain why loans were approved or rejected.  
    """)

    # 🔹 **How It Works**
    st.subheader("🛠️ How It Works")
    st.markdown("""
    1. **Make Predictions**: Enter loan applicant details and get predictions.  
    2. **Analyze Decisions**: Use explainability tools to see how AI decides.  
    3. **Detect Bias**: Check if approvals vary based on demographics.  
    4. **Improve Models**: Train better AI models for accurate decisions.  
    """)

    # 🌟 **What is Nebius AI Studio?**
    st.subheader("🌟 What is Nebius AI Studio?")
    st.markdown("""
    **[Nebius AI Studio](https://studio.nebius.com/)** is a powerful cloud-based AI development platform that enables users to **train, deploy, and monitor** machine learning models efficiently.  
    It provides tools for:
    
    - **🔍 AI Model Training & Debugging**: Build and fine-tune ML models in the cloud.  
    - **📊 Scalable AI Inference**: Deploy models for real-time predictions.  
    - **⚡ Bias Detection & Explainability**: Identify bias and understand AI decisions.  
    - **🔧 Cloud-Based Performance Optimization**: Leverage GPU & TPU acceleration.  

    **How is it used in Loan AI Debugger?**  
    - Nebius AI Studio is used for **training and deploying ML models** for loan approval predictions.  
    - It allows for **fast, scalable AI inference**, ensuring real-time loan predictions.  
    - It helps integrate **explainability & bias detection** to ensure **fair and transparent** loan approvals.  
    """)

    # ✨ Footer
    st.markdown("---")
    st.write("📌 **Loan AI Debugger** | Developed by Utsav Singhal | © 2025")