import streamlit as st
import requests
import json
import os
import pickle
from streamlit_chat import message  # مكتبة لتحسين عرض الرسائل

# 🔹 إعداد الصفحة
st.set_page_config(
    page_title="Ollama Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 📌 ملف تخزين المحادثات
CHAT_HISTORY_FILE = "chat_history.pkl"

# 🔥 تحسين طريقة تحميل وحفظ المحادثات باستعمال pickle
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "rb") as file:
                return pickle.load(file)
        except Exception:
            return []
    return []

def save_chat_history():
    with open(CHAT_HISTORY_FILE, "wb") as file:
        pickle.dump(st.session_state.messages, file)

# 🔥 تهيئة الرسائل
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# 🔥 دالة لجلب الموديلات المتاحة من Ollama
def get_available_models():
    try:
        response = requests.get('http://localhost:11434/api/tags')
        if response.status_code == 200:
            models = response.json()
            return [model['name'] for model in models['models']]
        return []
    except:
        return []

# 🔥 تحسين طريقة إرسال واستقبال الرسائل من Ollama باستعمال Streaming
def chat_with_ollama():
    """Send chat history to Ollama and stream responses dynamically."""
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": st.session_state.selected_model,
                "prompt": format_chat_history(),
                "stream": True
            },
            stream=True
        )

        response_text = ""  
        message_placeholder = st.empty()  

        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)  
                        chunk = data.get("response", "")  
                        response_text += chunk  

                        # ✅ تحديث النص بدون الحاجة لإعادة عرض كل شيء
                        message_placeholder.markdown(f"**AI:** {response_text}")
                        st.session_state.messages[-1]["content"] = response_text  
                    except json.JSONDecodeError:
                        continue  

        return response_text  
    except Exception as e:
        return f"Error: {str(e)}"

# 🔥 تحسين طريقة تمرير المحادثة للـ AI باش يفهم السياق مزيان
def format_chat_history():
    """Format chat history for better context."""
    history = "\n".join([f"{'User' if msg['role'] == 'user' else 'AI'}: {msg['content']}" for msg in st.session_state.messages[-5:]])
    return history + "\nAI:"

# 🔥 إضافة اختيار الموديل في الـ Sidebar
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

# 🔥 تحسين عرض المحادثة باستعمال `streamlit_chat`
st.title("🤖 Ollama Chat")

# ✅ عرض الرسائل بطريقة محسنة
for i, msg in enumerate(st.session_state.messages):
    is_user = msg["role"] == "user"
    message(msg["content"], is_user=is_user, key=str(i))  

# 🔥 إضافة إدخال المستخدم
if st.session_state.selected_model:
    with st.form(key="chat_form"):
        user_input = st.text_area("Type your message:", key="chat_input", height=100)
        submit_button = st.form_submit_button("Send")
        
        if submit_button and user_input.strip():
            # ✅ إضافة رسالة المستخدم
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # ✅ إضافة رسالة AI فارغة ليتم تحديثها ديناميكياً
            st.session_state.messages.append({"role": "assistant", "content": ""})

            # ✅ طلب الرد من Ollama
            with st.spinner("AI is thinking..."):
                ai_response = chat_with_ollama()

            # ✅ حفظ المحادثة
            save_chat_history()
            
            # ✅ تحديث الواجهة
            st.rerun()
else:
    st.warning("Please make sure Ollama is running and select a model to start chatting.")
