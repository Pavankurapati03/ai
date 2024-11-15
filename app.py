import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai  

# Load environment variables from .env file
load_dotenv()

# Set up Google Gemini-Pro API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("API key is missing. Please check your .env file and set GOOGLE_API_KEY.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# Configure Streamlit page settings
st.set_page_config(
    page_title="DebugMate",
    page_icon="🔍",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Custom CSS styling for the title and sidebar
st.markdown(
    """
    <style>
    .custom-title {
        font-size: 46px;
        text-align: center;
        font-weight: bold;
        font-family: Montserrat;
        background: -webkit-linear-gradient(rgb(188, 12, 241), rgb(212, 4, 4));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display Main Title
st.markdown("<p class='custom-title'>DebugMate</p>", unsafe_allow_html=True)


# Text area for code input
user_code = st.text_area("Enter your code here...", height=200)

# Button to trigger code review
if st.button("Review my code →"):
    if not GOOGLE_API_KEY:
        st.error("API key is missing. Unable to proceed.")
    elif not user_code.strip():
        st.warning("Please enter some code before clicking 'Review my code →'.")
    else:
        # Show loading spinner
        with st.spinner("Reviewing your code..."):
            try:
                # Initialize the generative model
                model = genai.GenerativeModel(f"models/gemini-1.5-flash")
                
                # Send the user code for review
                chatbot = model.start_chat(history=[])
                response = chatbot.send_message(f"You are an expert software engineer with extensive knowledge in various programming languages. Review the following code thoroughly for bugs, errors, and potential improvements. Please also identify the programming language used in the code and provide detailed explanations for any issues you find. Offer suggestions to improve the code where applicable:\n{user_code}")

                
                # Display the AI-generated response
                st.subheader("Code Review")
                st.write("Bug Report:")
                st.write(response.text)  # Display AI response
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")