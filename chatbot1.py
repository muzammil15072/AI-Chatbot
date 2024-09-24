import google.generativeai as genai
import streamlit as st

# API configuration
GOOGLE_API_KEY = "AIzaSyCHTh8GXsX21s9wdpdMSF4BW3vtwcEdWbI"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get chatbot response
def get_chatbot_response(user_input):
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Streamlit page configurations
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #e6eef1;
    }
    .chat-box {
        max-width: 700px;
        margin: auto;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #cce5ff;
        color: #004085;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: left;
    }
    .bot-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: left;
    }
    .chat-header {
        text-align: center;
        color: #333;
    }
    .send-button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .send-button:hover {
        background-color: #0069d9;
    }
    .stop-button {
        background-color: #f44336;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 10px;
    }
    .stop-button:hover {
        background-color: #e53935;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1 class='chat-header'>🤖 King Chatbot 🤖</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Powered by Google Gemini Model</p>", unsafe_allow_html=True)
st.write("---")

# Initialize chat history and process running state
if "history" not in st.session_state:
    st.session_state.history = []

if "is_running" not in st.session_state:
    st.session_state.is_running = False  # Track if the bot is generating a response

# Function to render chat messages
def display_chat():
    st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
    for chat in st.session_state.history:
        if chat["is_user"]:
            st.markdown(f"<div class='user-message'><strong>You:</strong> {chat['message']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-message'><strong>AI:</strong> {chat['message']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Main chat input area
def main():
    # Always display Stop button if the chatbot is processing
    if st.session_state.is_running:
        if st.button("Stop", key="stop_button"):
            st.session_state.is_running = False  # Stop the process when button is clicked

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("You:", key="input", placeholder="Type your message here...", label_visibility="hidden")
        submit_button = st.form_submit_button("Send")

        if submit_button and user_input:
            st.session_state.is_running = True  # Set running state to True when process starts

            # Store user's message
            st.session_state.history.append({"message": user_input, "is_user": True})

            # Get chatbot response only if not stopped
            if st.session_state.is_running:
                bot_response = get_chatbot_response(user_input)
                st.session_state.history.append({"message": bot_response, "is_user": False})

            st.session_state.is_running = False  # Reset running state after process completes

    # Display chat history
    if st.session_state.history:
        display_chat()

# Footer with credits
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 14px;'>"
    "Powered by Streamlit • Built with King ❤️ </p>",
    unsafe_allow_html=True
)

if __name__ == "__main__":
    main()
