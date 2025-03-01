import streamlit as st
import requests
import json
import os

# Set page config
st.set_page_config(
    page_title="Ollama Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# File path for saving chat history
CHAT_HISTORY_FILE = "chat_history.json"

# Custom CSS for better UI
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .stTextArea > div > div > textarea {
        background-color: #f0f2f6;
    }
    .main {
        padding: 2rem;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .bot-message {
        background-color: #f5f5f5;
    }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Function to load chat history from a file
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as file:
                data = file.read()
                return json.loads(data) if data.strip() else []  # Check if file is empty
        except (json.JSONDecodeError, ValueError):
            return []  # Return empty list if JSON is corrupted
    return []

# Function to save chat history to a file
def save_chat_history():
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(st.session_state.messages, file, indent=4)

# Initialize session state for chat messages
if 'messages' not in st.session_state:
    st.session_state.messages = load_chat_history()

def get_available_models():
    """Fetch available models from Ollama"""
    try:
        response = requests.get('http://localhost:11434/api/tags')
        if response.status_code == 200:
            models = response.json()
            return [model['name'] for model in models['models']]
        return []
    except:
        return []

# def chat_with_ollama(): # message, model
#     """Send a message to Ollama and get the response"""
#     try:
#         response = requests.post(
#             'http://localhost:11434/api/generate',
#             json={
#                 "model": st.session_state.selected_model,
#                 "prompt": format_chat_history(), # Send full conversation history
#                 "stream": False
#             }
#         )
#         if response.status_code == 200:
#             return response.json().get('response', 'No response from the model.')
#         return "Error: Unable to get response from the model."
#     except Exception as e:
#         return f"Error: {str(e)}"

# 🔥 Why This Works
# ✅ Shorter responses → Faster processing
# ✅ Avoids unnecessary long answers
# ✅ Speeds up inference time

def chat_with_ollama():
    """Send chat history to Ollama and stream responses correctly."""
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": st.session_state.selected_model,
                "prompt": format_chat_history(),
                "stream": True  # ✅ Enable streaming
            },
            stream=True  # ✅ Stream response as it's generated
        )

        response_text = ""  # ✅ Stores full response
        message_placeholder = st.empty()  # ✅ Creates an empty space to update text dynamically

        # ✅ Correctly process each JSON chunk
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)  # Parse JSON
                        response_text += data.get("response", "")  # Extract text

                        # ✅ Update the placeholder dynamically (no duplication)
                        message_placeholder.markdown(f"**AI:** {response_text}")
                    except json.JSONDecodeError:
                        continue  # Ignore malformed JSON chunks

        return response_text  # Return full response after streaming
    except Exception as e:
        return f"Error: {str(e)}"

def format_chat_history():
    """Format chat history so Ollama can remember context"""
    history = ""
    for message in st.session_state.messages:
        role = "User" if message["role"] == "user" else "AI"
        history += f"{role}: {message['content']}\n"
    return history + "\nAI:"

# Sidebar for model selection
st.sidebar.title("🤖 Ollama Chat Settings")
available_models = get_available_models()
if available_models:
    st.session_state.selected_model = st.sidebar.selectbox(
        "Select Model",
        available_models,
        index=0
    )
else:
    st.sidebar.error("No models found. Please make sure Ollama is running.")
    st.session_state.selected_model = None

st.sidebar.markdown("---")
st.sidebar.markdown("""
### How to use:
1. Make sure Ollama is running locally.
2. Select a model from the dropdown.
3. Type your message and press Enter.
4. Wait for the AI to respond.
""")

# Main chat interface
st.title("🤖 Ollama Chat")

# Display chat messages
chat_container = st.container()
for message in st.session_state.messages:
    with chat_container:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div><strong>You:</strong></div>
                <div>{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div><strong>AI:</strong></div>
                <div>{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)



# Chat input
if st.session_state.selected_model:
    with st.form(key='chat_form'):
        user_input = st.text_area("Type your message:", key="chat_input", height=100)
        submit_button = st.form_submit_button("Send")
        
        if submit_button and user_input.strip():
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get AI response
            with st.spinner("AI is thinking..."):
                ai_response = chat_with_ollama() # user_input, st.session_state.selected_model
                
            # Add AI response to chat history
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

            # Save chat history to file
            save_chat_history()
            
            # Force a rerun to update the chat
            st.rerun()
else:
    st.warning("Please make sure Ollama is running and select a model to start chatting.")
