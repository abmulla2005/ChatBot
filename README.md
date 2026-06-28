# ChatBot

# 🤖 LangGraph Chatbot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatbot-aa2ezrr5ev7anzqwcdy2cx.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.0.20+-green.svg)](https://github.com/langchain-ai/langgraph)

> An intelligent chatbot powered by LangGraph and Streamlit, featuring persistent conversations and a modern UI.

---

## ✨ Features

- **🧠 Stateful Conversations** - Maintains context across multiple chat sessions
- **💾 Persistent Storage** - Each conversation gets a unique UUID for easy retrieval
- **🎨 Clean UI** - Beautiful, responsive interface built with Streamlit
- **⚡ Real-time Responses** - Instant feedback with streaming capabilities
- **📚 Multi-session Management** - Start new chats or resume previous ones anytime
- **🔒 Secure & Private** - No data logging; your conversations stay private

---

## 🚀 Quick Start

### Try It Live
👉 [**Launch the Chatbot**](https://chatbot-aa2ezrr5ev7anzqwcdy2cx.streamlit.app/)

### Run Locally

```bash
# Clone the repository
git clone https://github.com/abmulla2005/ChatBot.git
cd ChatBot

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **LangGraph** | Conversation flow management & state handling |
| **Streamlit** | Interactive web interface |
| **Python 3.9+** | Core programming language |
| **UUID** | Unique conversation identifiers |

---

## 📂 Project Structure

```
ChatBot/
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .gitignore           # Git ignore file
```

---

## 🎯 How It Works

1. **Start a Chat** - Click "New Chat" to generate a unique session ID
2. **Send Messages** - Type your message and press Enter
3. **AI Responds** - LangGraph processes your input and generates a response
4. **Switch Context** - Select any previous conversation from the sidebar
5. **Continue Talking** - The AI remembers context within each session

---

## 🔧 Configuration

The chatbot uses:
- **LangGraph** for conversation state management
- **Streamlit's session state** for UI persistence
- **No external API keys required** - Perfect for testing and local development

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Abid Mulla**
- GitHub: [@abmulla2005](https://github.com/abmulla2005)

---

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) for LangGraph
- [Streamlit](https://streamlit.io/) for the amazing UI framework

---

*Built with ❤️ using LangGraph and Streamlit*
