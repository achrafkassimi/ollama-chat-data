# 🤖 Ollama Chat data 

Ollama Chat is a **conversational AI web app** built using **Streamlit** that allows users to interact with local AI models. The app maintains conversation history in memory and saves it to a JSON file to **persist context** across sessions.  

---

## 🚀 Features  
✅ **Supports multiple AI models** (React Native, Python, Node.js)  
✅ **Context Retention** – The AI remembers variables and previous messages  
✅ **Saves Chat History** – Persists conversation in `chat_history.json`  
✅ **User-Friendly UI** – Styled chat bubbles with an interactive layout  
✅ **Fast & Lightweight** – Runs locally with minimal setup  

---

## 🛠️ Installation  

### **1️⃣ Prerequisites**  
- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running locally
- Streamlit  

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/achrafkassimi/ollama-chat-data.git
cd ollama-chat-data
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the App**
```bash
streamlit run app_streamlit.py
```
or
```bash
streamlit run app_streamlit.py --server.address=127.0.0.1 --server.enableCORS=false --server.enableXsrfProtection=false
```

---

## ⚙️ Configuration  

- **Select AI Model**: Choose a model from the sidebar dropdown.  
- **Enter Messages**: Type your message in the text area and hit "Send".  
- **Chat Memory**: The AI remembers previous messages, including variables (e.g., `A = 12`).  

---

## 📝 How it Works  

1️⃣ The **chat history** is stored in `st.session_state.messages`  
2️⃣ Every new message is **added to memory** and sent to the AI  
3️⃣ The AI receives **full conversation history** with each request  
4️⃣ Chat history is **saved to `chat_history.json`** for persistence  
5️⃣ When restarted, the app **loads previous conversations**  

---

## 📂 Project Structure  

```
📆 ollama-chat-data
 ├📋 app_streamlit.py   # Main Streamlit app
 ├📋 chat_history.json  # Stores chat history
 ├📋 requirements.txt   # Python dependencies
 └📋 README.md          # Project documentation
```

---

## 🔧 Troubleshooting  

**💡 Ollama is not responding?**  
➡ Ensure Ollama is **running locally** (`http://localhost:11434`).  

**💡 "JSONDecodeError" when starting?**  
➡ Delete `chat_history.json` and restart:  
```bash
rm chat_history.json
streamlit run app_streamlit.py
```

**💡 Model selection dropdown is empty?**  
➡ Make sure **Ollama is running** and serving models.  

---

## 🛠️ Technologies Used  
- **Python** 🐍  
- **Streamlit** 🎨  
- **Ollama AI** 🤖  
- **JSON for storage** 📄  

---

## 🎯 Future Improvements  
- ✅ **Add Chat Reset Button**  
- ✅ **Support for multiple users**  
- ✅ **Improve UI with better message formatting**  
- 🛠️ **Enable live streaming of AI responses** (upcoming)  

---

## 📩 Contact  
📧 Email: achraf.kassimi.1995@gmail.com
🔗 LinkedIn: [achraf.kassimi](https://linkedin.com/in/kassimi-achraf)  
💻 GitHub: [achraf.kassimi](https://github.com/achrafkassimi)  

---

**🚀 Enjoy chatting with Ollama AI!**

